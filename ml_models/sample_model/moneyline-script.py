import os
import pandas as pd
import numpy as np
import requests
import nflreadpy as nfl
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import GridSearchCV

# -----------------------------
# Data Loading
# -----------------------------
def load_nfl_data(start=2016, end=2025):
    """Load all NFL datasets for the given range of seasons."""
    print("Loading data...")
    team_stats = nfl.load_team_stats(list(range(start, end + 1))).to_pandas()
    schedules = nfl.load_schedules(seasons=list(range(start, end + 1))).to_pandas()
    return team_stats, schedules


# -----------------------------
# Data Cleaning
# -----------------------------
def clean_team_stats(df_ts):
    """Clean and simplify team stats dataframe."""
    print("Cleaning team stats...")
    df_ts = df_ts[df_ts["season_type"] == "REG"].copy()
    df_ts["def_tackles"] = df_ts["def_tackles_solo"] + df_ts["def_tackles_with_assist"]
    df_ts["fumbles"] = (
        df_ts["sack_fumbles"]
        + df_ts["rushing_fumbles"]
        + df_ts["receiving_fumbles"]
    )

    remove_cols = [
        'passing_2pt_conversions', 'punt_returns', 'punt_return_yards', 'kickoff_returns',
        'kickoff_return_yards', 'fg_made', 'fg_att', 'fg_missed', 'fg_blocked', 'fg_long',
        'fg_made_0_19', 'fg_made_20_29', 'fg_made_30_39', 'fg_made_40_49', 'fg_made_50_59',
        'fg_made_60_', 'fg_missed_0_19', 'fg_missed_20_29', 'fg_missed_30_39', 'fg_missed_40_49',
        'fg_missed_50_59', 'fg_missed_60_', 'fg_made_list', 'fg_missed_list', 'fg_blocked_list',
        'fg_made_distance', 'fg_missed_distance', 'fg_blocked_distance', 'pat_made', 'pat_att',
        'pat_missed', 'pat_blocked', 'pat_pct', 'gwfg_made', 'gwfg_att', 'gwfg_missed', 'gwfg_blocked',
        'gwfg_distance', 'def_safeties', 'misc_yards', 'fumble_recovery_own', 'fumble_recovery_yards_own',
        'fumble_recovery_opp', 'fumble_recovery_yards_opp', 'fumble_recovery_tds', 'sack_yards_lost',
        'sack_fumbles_lost', 'timeouts', 'passing_air_yards', 'passing_yards_after_catch',
        'rushing_fumbles_lost', 'rushing_2pt_conversions', 'targets', 'receiving_fumbles_lost',
        'receiving_air_yards', 'receiving_yards_after_catch', 'season_type', 'receiving_2pt_conversions',
        'special_teams_tds', 'def_tackles_solo', 'def_tackles_with_assist', 'def_tackle_assists',
        'def_tackles_for_loss_yards', 'def_sack_yards', 'def_interception_yards', 'def_tds',
        'rushing_fumbles', 'receiving_fumbles', 'sack_fumbles', 'def_fumbles'
    ]
    return df_ts.drop(remove_cols, axis=1, errors='ignore')


def clean_schedules(df_schedules):
    """Prepare schedule data with win/loss labels."""
    print("Processing schedules...")
    df = df_schedules[df_schedules["game_type"] == "REG"].copy()
    is_home_first = df["home_team"] < df["away_team"]

    df["team"] = np.where(is_home_first, df["home_team"], df["away_team"])
    df["opponent_team"] = np.where(is_home_first, df["away_team"], df["home_team"])
    score_team = np.where(is_home_first, df["home_score"], df["away_score"])
    score_opponent = np.where(is_home_first, df["away_score"], df["home_score"])
    df["is_team_win"] = (score_team > score_opponent).astype(int)

    return df[["season", "week", "team", "opponent_team", "is_team_win"]]

# -----------------------------
# Feature Engineering
# -----------------------------
def compute_rolling_averages(df_ts):
    """Compute rolling averages for each team up to each week."""
    print("Computing rolling averages...")
    df_sorted = df_ts.sort_values(by=["season", "week"])
    stat_cols = [col for col in df_sorted.columns if col not in ["season", "week", "team", "opponent_team", "score", "opponent_score"]]

    rolling = df_sorted.groupby("team")[stat_cols].transform(lambda x: x.expanding().mean().shift(1))
    base = df_sorted[["season", "week", "team", "opponent_team"]].reset_index(drop=True)
    rolling.index = base.index

    df_std = pd.concat([base, rolling], axis=1)
    df_std.fillna(0, inplace=True)
    return df_std

def create_matchup_differentials(df_std, df_schedules_final):
    """Compute differential features between team and opponent."""
    print("Creating matchup differentials...")
    df_opp = df_std.copy().rename(columns={"team": "opponent_match_key", "opponent_team": "team_match_check"})

    df = pd.merge(
        df_std, df_opp,
        left_on=["season", "week", "opponent_team"],
        right_on=["season", "week", "opponent_match_key"],
        suffixes=("_team", "_opp"),
        how="inner"
    )

    team_a_margin = (df["def_interceptions_team"] + df["def_fumbles_forced_team"]) - (df["passing_interceptions_team"] + df["fumbles_team"])
    team_b_margin = (df["def_interceptions_opp"] + df["def_fumbles_forced_opp"]) - (df["passing_interceptions_opp"] + df["fumbles_opp"])

    df["d_touchdowns"] = (df["passing_tds_team"] + df["rushing_tds_team"]) - (df["passing_tds_opp"] + df["rushing_tds_opp"])
    df["d_sacks_suffered"] = df["sacks_suffered_opp"] - df["sacks_suffered_team"]
    df["d_passing_epa"] = df["passing_epa_team"] - df["passing_epa_opp"]
    df["d_passing_cpoe"] = df["passing_cpoe_team"] - df["passing_cpoe_opp"]
    df["d_rushing_yards"] = df["rushing_yards_team"] - df["rushing_yards_opp"]
    df["d_receiving_epa"] = df["receiving_epa_team"] - df["receiving_epa_opp"]
    df["d_tackles_for_loss"] = df["def_tackles_for_loss_team"] - df["def_tackles_for_loss_opp"]
    df["d_sacks"] = df["def_sacks_team"] - df["def_sacks_opp"]
    df["d_qb_hits"] = df["def_qb_hits_team"] - df["def_qb_hits_opp"]
    df["d_fg_pct"] = df["fg_pct_team"] - df["fg_pct_opp"]
    df["d_turnover_margin"] = team_a_margin - team_b_margin

    df = pd.merge(df, df_schedules_final, on=["season", "week", "team", "opponent_team"], how="inner")
    return df

# -----------------------------
# Model Training
# -----------------------------
def train_model(df_std_matchups):
    """Train and evaluate logistic regression model."""
    print("Training model...")
    df = df_std_matchups[[c for c in df_std_matchups.columns if c.startswith("d_") or c in ["season", "week", "is_team_win", "team", "opponent_team"]]].copy()

    y = df["is_team_win"]
    X_cols = [c for c in df.columns if c.startswith("d_") or c in ["season", "week"]]
    X = df[X_cols]

    train_seasons = df["season"].unique()[:-2]
    test_seasons = df["season"].unique()[-2:-1]

    X_train, y_train = X[X["season"].isin(train_seasons)].copy(), y[X["season"].isin(train_seasons)].copy()
    X_test, y_test = X[X["season"].isin(test_seasons)].copy(), y[X["season"].isin(test_seasons)].copy()

    X_train.drop(columns=["season", "week"], inplace=True)
    X_test.drop(columns=["season", "week"], inplace=True)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    grid = GridSearchCV(
        LogisticRegression(solver="liblinear", random_state=1),
        [{"C": [0.00004], "penalty": ["l1", "l2"]}],
        scoring="roc_auc", cv=5, n_jobs=-1
    )
    grid.fit(X_train_scaled, y_train)
    model = grid.best_estimator_

    print(f"Best C: {grid.best_params_['C']}")
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    y_pred = (y_pred_proba > 0.5).astype(int)

    print(classification_report(y_test, y_pred))
    print(f"AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")

    return model, scaler, X_train.columns


# -----------------------------
# Future Predictions
# -----------------------------
def predict_future_games(df_ts_std, df_schedules_final, model, scaler, X_columns):
    """Generate win probabilities for future games."""
    print("Generating 2025 future game predictions...")
    df_future = df_schedules_final[(df_schedules_final["season"] == 2025) & (df_schedules_final["week"] > 9)].copy()

    df_latest = df_ts_std.sort_values(["season", "week"]).groupby("team").tail(1).reset_index(drop=True)
    stats_cols = [c for c in df_latest.columns if c not in ["season", "week", "opponent_team"]]
    df_latest = df_latest[stats_cols]

    X_future = pd.merge(df_future, df_latest, on="team", how="left")
    X_future = pd.merge(X_future, df_latest, left_on="opponent_team", right_on="team", suffixes=("_team", "_opp"), how="left")
    X_future.drop(columns=["team_opp"], inplace=True, errors="ignore")

    team_a_margin = (X_future["def_interceptions_team"] + X_future["def_fumbles_forced_team"]) - (X_future["passing_interceptions_team"] + X_future["fumbles_team"])
    team_b_margin = (X_future["def_interceptions_opp"] + X_future["def_fumbles_forced_opp"]) - (X_future["passing_interceptions_opp"] + X_future["fumbles_opp"])

    X_future["d_touchdowns"] = (X_future["passing_tds_team"] + X_future["rushing_tds_team"]) - (X_future["passing_tds_opp"] + X_future["rushing_tds_opp"])
    X_future["d_sacks_suffered"] = X_future["sacks_suffered_opp"] - X_future["sacks_suffered_team"]
    X_future["d_passing_epa"] = X_future["passing_epa_team"] - X_future["passing_epa_opp"]
    X_future["d_passing_cpoe"] = X_future["passing_cpoe_team"] - X_future["passing_cpoe_opp"]
    X_future["d_rushing_yards"] = X_future["rushing_yards_team"] - X_future["rushing_yards_opp"]
    X_future["d_receiving_epa"] = X_future["receiving_epa_team"] - X_future["receiving_epa_opp"]
    X_future["d_tackles_for_loss"] = X_future["def_tackles_for_loss_team"] - X_future["def_tackles_for_loss_opp"]
    X_future["d_sacks"] = X_future["def_sacks_team"] - X_future["def_sacks_opp"]
    X_future["d_qb_hits"] = X_future["def_qb_hits_team"] - X_future["def_qb_hits_opp"]
    X_future["d_fg_pct"] = X_future["fg_pct_team"] - X_future["fg_pct_opp"]
    X_future["d_turnover_margin"] = team_a_margin - team_b_margin

    X_future_final = X_future[X_columns].fillna(0)
    X_future_scaled = scaler.transform(X_future_final)

    df_future["Win_Probability"] = model.predict_proba(X_future_scaled)[:, 1]
    df_future.rename(columns={"team": "Team_A", "opponent_team": "Team_B"}, inplace=True)
    df_future.drop(columns=["is_team_win"], inplace=True, errors="ignore")

    print(df_future[["season", "week", "Team_A", "Team_B", "Win_Probability"]])
    return df_future

# -----------------------------
# Main Pipeline
# -----------------------------
def main():
    team_stats, schedules = load_nfl_data()
    df_ts = clean_team_stats(team_stats)
    df_schedules_final = clean_schedules(schedules)

    df_ts_std = compute_rolling_averages(df_ts)
    df_std_matchups = create_matchup_differentials(df_ts_std, df_schedules_final)
    model, scaler, X_columns = train_model(df_std_matchups)
    df_future = predict_future_games(df_ts_std, df_schedules_final, model, scaler, X_columns)
    print(df_future)


if __name__ == "__main__":
    main()