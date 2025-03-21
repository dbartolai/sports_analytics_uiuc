import numpy as np
import sqlite3 as sq
from flask import Flask, jsonify
from numpy import random as r
import json
from queue import Queue

### FIND ALL OF THE GAMES BY A CERTAIN TEAM IN THE REGULAR SEASON, AND USE THAT TO DETERMINE PLAYOFF PERFORMANCE
### USE REGULAR SEASON GAMES UP TO A SPECIFIC POINT TO DETERMINE ANY REGULAR SEASON GAME AT SAID POINT
### THIS DOCUMENT USES EFFICIENCY AND ADVANCED STATS INSTEAD OF BOX SCORE STATS

def max_game_id(cursor, year):
    year = year%100
    if year < 10:
        year = '0' + str(year)
    else:
        year = str(year)
    statement = f'SELECT game_id FROM game WHERE game_id Like \'002{year}%\' ORDER BY game_id DESC'
    cursor.execute(statement)
    max_game_id = cursor.fetchone()
    return(max_game_id)[0]

def min_game_id(year):
    return(f'002{year%100}00030')

def first_game_id(year):
    return (f'002{year%100}00001')

def get_regular_season_games(cursor, year):
    statement = f'SELECT game_id, team_abbreviation_home, pts_home, wl_home, wl_away, pts_away, team_abbreviation_away FROM game WHERE season_id = 2{year} ORDER BY game_id'
    cursor.execute(statement)
    season_games = cursor.fetchall()
    return season_games

def get_results_by_game_id(cursor, game_id):
    statement = f'SELECT game_id, team_abbreviation_home, pts_home, wl_home, wl_away, pts_away, team_abbreviation_away FROM game WHERE game_id = \'{game_id}\''
    cursor.execute(statement)
    # result = [game_id, home, home score, away score, away]
    game_info = cursor.fetchone()
    try:
        result = [game_info[0], game_info[1], game_info[2], game_info[5], game_info[6]]
        return result
    except:
        pass

def get_stats_by_game_id_home(cursor, game_id):
    statement = f'SELECT game_id, fgm_home, fga_home, fg3m_home, fg3a_home, ftm_home, fta_home, oreb_home, dreb_home, ast_home, stl_home, blk_home, tov_home, pf_home FROM game WHERE game_id = \'{game_id}\''
    cursor.execute(statement)
    stats = cursor.fetchone()
    return stats

def get_stats_by_game_id_away(cursor, game_id):
    statement = f'SELECT game_id, fgm_away, fga_away, fg3m_away, fg3a_away, ftm_away, fta_away, oreb_away, dreb_away, ast_away, stl_away, blk_away, tov_away, pf_away FROM game WHERE game_id = \'{game_id}\''
    cursor.execute(statement)
    stats = cursor.fetchone()
    return stats

def get_team_names_by_year(cursor, year):
    statement = f'SELECT game_id, team_abbreviation_home, pts_home, wl_home, wl_away, pts_away, team_abbreviation_away FROM game WHERE season_id = 2{year} ORDER BY game_id'
    cursor.execute(statement)
    season_games = cursor.fetchmany(30)
    team_names = []
    for game in season_games:
        home_team = game[1]
        away_team = game[6]
        home_exists = 0
        away_exists = 0
        for name in team_names:
            if home_team == name:
                home_exists = 1
            if away_team == name:
                away_exists = 1
        if not home_exists:
            team_names.append(home_team)
        if not away_exists:
            team_names.append(away_team)
    return team_names


def get_team_games_regular_season(cursor, team, year):
    game_log = get_regular_season_games(cursor, year)
    team_games = []
    for game in game_log:
        if game[1] == team:
            team_games.append([game[0], 0])
        elif game[6] == team:
            team_games.append([game[0], 1])          
    return team_games

def get_team_results_regular_season(cursor, team, year):
    game_log = get_team_games_regular_season(cursor, team, year)
    results = []
    for game in game_log:
        game_id = game[0]
        is_away = game[1]
        results.append(get_results_by_game_id(cursor, game_id, is_away))
    return results

def get_team_stats_regular_season(cursor, team, year):
    game_log = get_team_games_regular_season(cursor, team, year)
    stats = []
    for game in game_log:
        game_id = game[0]
        is_away = game[1]
        if is_away:
            stats.append(get_stats_by_game_id_away(cursor, game_id))
        else:
            stats.append(get_stats_by_game_id_home(cursor, game_id))
    return stats



def estimate_possessions(FGA, FTA, TO, OREB):

    # Posessions = FGA + 0.44 * FTA + TO - OREB

    return FGA + 0.44*FTA + TO - OREB


def ratings(PFOR, PALLOWED, POSS):

    ORTG = PFOR/POSS
    DRTG = PALLOWED/POSS
    NET = ORTG - DRTG

    return [ORTG, DRTG, NET]


def adjusted_ratings(ORTG, OpponentORTG, DRTG, OpponentDRTG):
    AdjORTG = ORTG - OpponentDRTG
    AdjDRTG = DRTG - OpponentORTG
    return [AdjDRTG, AdjORTG]

def efficiency(POSS, GP, PTS, OREB, DREB, OpponentOREB, OpponentDREB, TO, AST, FGA, FTA, ThreePM, FGM):

    # Pace = Possessions / Games Played
    Pace = POSS/GP
    # True Shooting = Points / [ 2 * (FGA + 0.44 * FTA) ]
    TS = PTS / (2 * (FGA + 0.44*FTA))
    # Effective FG% = (FGM + 0.5 * 3PM) / FGA
    eFG = (FGM + 0.5* ThreePM)/FGA
    # OREB% = OREB / [OREB + opponent DREB]
    OREBpct = OREB / (OREB + OpponentDREB)
    DREBpct = DREB / (DREB + OpponentOREB)
    # TOV% = TOV / POSS
    TOpct = TO / POSS
    # Assist to Turnover Ratio = AST / TOV
    ATR = AST / TO

    return [Pace/100, TS, eFG, OREBpct, DREBpct, TOpct, ATR]
def new_compile_and_scale_features(cursor, game_id, records):

    results = get_results_by_game_id(cursor, game_id)

    update_record_dict(cursor, records, game_id)

    # Find home and away box scores from the game
    # fgm, fga, fg3m, fg3a, ftm, fta, oreb, dreb, ast, stl, blk, tov, pf
    home_stats = get_stats_by_game_id_home(cursor, game_id)[1:14]
    away_stats = get_stats_by_game_id_away(cursor, game_id)[1:14]

    # Posessions
    home_posessions = estimate_possessions(home_stats[1], home_stats[5], home_stats[11], home_stats[6]) 
    away_posessions = estimate_possessions(away_stats[1], away_stats[5], away_stats[11], away_stats[6]) 

    # [ORTG, DRTG, NET]
    home_ratings = ratings(results[2], results[3], home_posessions)
    away_ratings = ratings(results[3], results[2], away_posessions)

    # AdjustedORTG, AdjustedDRTG
    home_adjusted_ratings = adjusted_ratings(home_ratings[0], away_ratings[0], home_ratings[1], away_ratings[1])
    home_NET = home_adjusted_ratings[0] - home_adjusted_ratings[1]
    away_adjusted_ratings = adjusted_ratings(away_ratings[0], home_ratings[0], away_ratings[1], home_ratings[1])
    away_NET = away_adjusted_ratings[0] - away_adjusted_ratings[1]

    #length: 7
    home_efficiency = efficiency(home_posessions, 1, results[2], home_stats[6], home_stats[7], away_stats[6], away_stats[7], home_stats[11], home_stats[8], home_stats[1], home_stats[5], home_stats[2], home_stats[0])
    away_efficiency = efficiency(away_posessions, 1, results[3], away_stats[6], away_stats[7], home_stats[6], home_stats[7], away_stats[11], away_stats[8], away_stats[1], away_stats[5], away_stats[2], away_stats[0])

    # X_i = [win_pct, ppg, ppga, ratings, efficiency] for home and away
    # Y_i = points scored for home and away

    return np.concatenate(([home_NET], home_efficiency, [away_NET], away_efficiency))
def update_record_dict(cursor, records, game_id):
    results = get_results_by_game_id(cursor, game_id)
    home_team = results[1]
    away_team = results[4]

    home_pts = results[2]
    away_pts = results[3]

    home_win = False

    if home_pts > away_pts: 
        home_win = True

    if records[home_team].full():
        records[home_team].get()

    if records[away_team].full():
        records[away_team].get()
    
    if home_win:
        records[home_team].put(np.array([1, 0, home_pts, away_pts]))
        records[away_team].put(np.array([0, 1, away_pts, home_pts]))
    else:
        records[home_team].put(np.array([0, 1, home_pts, away_pts]))
        records[away_team].put(np.array([1, 0, away_pts, home_pts]))


def update_stats_dict(cursor, stats, game_id, records):
    results = get_results_by_game_id(cursor, game_id) 
    home_team = results[1]                
    away_team = results[4]

    game_stats = new_compile_and_scale_features(cursor, game_id, records)

    if stats[home_team].full():
        stats[home_team].get()
        
    stats[home_team].put(game_stats[0:8])

    if stats[away_team].full():
        stats[away_team].get()

    stats[away_team].put(game_stats[8:16])



def rolling_averages(stats, records, home, away):


    home_temp = Queue(maxsize=15)
    home_games_checked = 0
    home_rolling_average_stats = np.zeros(8)
    
    while not stats[home].empty():
        home_stats = stats[home].get()
        home_stats_np = np.array(home_stats) 
        if home_games_checked < 5:
            for _ in range(3): home_rolling_average_stats = np.add(home_rolling_average_stats, home_stats_np)
            home_games_checked+= 1
        elif home_games_checked < 10:
            for _ in range(2): home_rolling_average_stats = np.add(home_rolling_average_stats, home_stats_np)
            home_games_checked+= 1
        else:    
            home_rolling_average = np.add(home_rolling_average_stats, home_stats_np)
            home_games_checked+= 1
        
        home_temp.put(home_stats)

    stats[home] = home_temp
    weighted_games_checked = 0
    for i in range(home_games_checked):
        if i < 5:
            weighted_games_checked += 3
        elif i < 10:
            weighted_games_checked += 2
        else :
            weighted_games_checked += 1
    if weighted_games_checked > 0: home_rolling_average_stats = np.divide(home_rolling_average_stats, weighted_games_checked)
    else: home_rolling_average_stats = np.zeros(8)

    away_temp = Queue(maxsize=15)
    away_games_checked = 0
    away_rolling_average_stats = np.zeros(8)
    
    while not stats[away].empty():
        away_stats = stats[away].get()
        away_stats_np = np.array(away_stats) 
        if away_games_checked < 5:
            for _ in range(3): away_rolling_average_stats = np.add(away_rolling_average_stats, away_stats_np)
            away_games_checked += 1
        elif away_games_checked < 10:
            for _ in range(2): away_rolling_average_stats = np.add(away_rolling_average_stats, away_stats_np)
            away_games_checked += 1
        else:    
            away_rolling_average = np.add(away_rolling_average_stats, away_stats_np)
            away_games_checked += 1
        
        away_temp.put(away_stats)

    stats[away] = away_temp
    weighted_games_checked = 0
    for i in range(away_games_checked):
        if i < 5:
            weighted_games_checked += 3
        elif i < 10:
            weighted_games_checked += 2
        else:
            weighted_games_checked += 1
    if weighted_games_checked > 0: away_rolling_average_stats = np.divide(away_rolling_average_stats, weighted_games_checked)
    else: away_rolling_average_stats = np.zeros(8)

    home_temp = Queue(maxsize=15)
    home_games_checked = 0
    home_rolling_average = np.zeros(4)
    
    while not records[home].empty():
        home_record = records[home].get()
        home_record_np = np.array(home_record) 
        if home_games_checked < 5:
            for _ in range(3): home_rolling_average = np.add(home_rolling_average, home_record_np)
            home_games_checked += 1
        elif home_games_checked < 10:
            for _ in range(2): home_rolling_average = np.add(home_rolling_average, home_record_np)
            home_games_checked += 1
        else:    
            home_rolling_average = np.add(home_rolling_average, home_record_np)
            home_games_checked += 1
        
        home_temp.put(home_record)

    records[home] = home_temp
    weighted_games_checked = 0
    for i in range(home_games_checked):
        if i < 5:
            weighted_games_checked += 3
        elif i < 10:
            weighted_games_checked += 2
        else:
            weighted_games_checked += 1
    if weighted_games_checked > 0: home_rolling_average = np.divide(home_rolling_average, weighted_games_checked)
    else: home_rolling_average = np.zeros(4)


    away_temp = Queue(maxsize=15)
    away_games_checked = 0
    away_rolling_average = np.zeros(4)
    
    while not records[away].empty():
        away_record = records[away].get()
        away_record_np = np.array(away_record) 
        if away_games_checked < 5:
            for _ in range(3): away_rolling_average = np.add(away_rolling_average, away_record_np)
            away_games_checked += 1
        elif away_games_checked < 10:
            for _ in range(2): away_rolling_average = np.add(away_rolling_average, away_record_np)
            away_games_checked += 1
        else:    
            away_rolling_average = np.add(away_rolling_average, away_record_np)
            away_games_checked += 1
        
        away_temp.put(away_record)

    records[away] = away_temp
    weighted_games_checked = 0
    for i in range(away_games_checked):
        if i < 5:
            weighted_games_checked += 3
        elif i < 10:
            weighted_games_checked += 2
        else:
            weighted_games_checked += 1
    if weighted_games_checked > 0: away_rolling_average = np.divide(away_rolling_average, weighted_games_checked)
    else: away_rolling_average = np.zeros(4)
    
    
    if (home_rolling_average[0] + home_rolling_average[1]) > 0: home_win_pct = home_rolling_average[0] / (home_rolling_average[0] + home_rolling_average[1])
    else: home_win_pct = 0
    if (away_rolling_average[0] + away_rolling_average[1]) > 0: away_win_pct = away_rolling_average[0] / (away_rolling_average[0] + away_rolling_average[1])
    else: away_win_pct = 0

    return np.concatenate(([home_win_pct], [home_rolling_average[2]/200], [home_rolling_average[3]/200], 
                          home_rolling_average_stats, away_rolling_average_stats,
                          [away_win_pct], [away_rolling_average[2]/200], [away_rolling_average[3]/200]))

