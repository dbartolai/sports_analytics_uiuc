import numpy as np
import kagglehub 
import sqlite3 as sq
from flask import Flask, jsonify

### FIND ALL OF THE GAMES BY A CERTAIN TEAM IN THE REGULAR SEASON, AND USE THAT TO DETERMINE PLAYOFF PERFORMANCE
### USE REGULAR SEASON GAMES UP TO A SPECIFIC POINT TO DETERMINE ANY REGULAR SEASON GAME AT SAID POINT

def max_game_id(cursor, year):
    year = year%100
    if year < 10:
        year = '0' + str(year)
    else:
        year = str(year)
    statement = f'SELECT game_id FROM game WHERE game_id Like \'002{year}%\' ORDER BY game_id DESC'
    cursor.execute(statement)
    max_game_id = cursor.fetchone()
    return(max_game_id)

def get_regular_season_games(cursor, year):
    statement = f'SELECT game_id, team_abbreviation_home, pts_home, wl_home, wl_away, pts_away, team_abbreviation_away FROM game WHERE season_id = 2{year} ORDER BY game_id'
    cursor.execute(statement)
    season_games = cursor.fetchall()
    return season_games

def get_results_by_game_id(cursor, game_id):
    statement = f'SELECT game_id, team_abbreviation_home, pts_home, wl_home, wl_away, pts_away, team_abbreviation_away FROM game WHERE game_id = \'{game_id}\''
    cursor.execute(statement)
    # result = [game_id, away, away score, home score, home]
    game_info = cursor.fetchone()
    result = [game_info[0], game_info[6], game_info[5], game_info[2], game_info[1]]
    return result

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

def home_stats_leading_up_to_game(cursor, year, game_id):
    team_name = get_results_by_game_id(cursor, game_id)[4]
    games_list = get_team_games_regular_season(cursor, team_name, year)
    stats = np.zeros(13).astype(int)
    num_of_games = 0
    for game in games_list:
        if game[0] < game_id:
            num_of_games += 1
            if game[1]:
                game_stats = np.array(get_stats_by_game_id_away(cursor, game[0])).astype(float)
            else:
                game_stats = np.array(get_stats_by_game_id_home(cursor, game[0])).astype(float)
            game_stats = game_stats[1:14:1]
            stats += game_stats.astype(int)

    return stats/num_of_games

def home_record_before_game(cursor, year, game_id):
    team_name = get_results_by_game_id(cursor, game_id)[4]
    games_list = get_team_games_regular_season(cursor, team_name, year)
    record = np.zeros(4) #[WINS, LOSSES, PPG Scored, PPG Allowed]
    num_of_games = 0
    for game in games_list:
        if game[0] < game_id:
            num_of_games += 1
            game_result = get_results_by_game_id(cursor, game[0])
            game_result = game_result[2:4:1]
            if game[1]:              
                if game_result[0] > game_result[1]:
                    record[0] += 1
                else:
                    record[1] += 1
                record[2] += game_result[0]
                record[3] += game_result[1]
            else:
                if game_result[1] > game_result[0]:
                    record[0] += 1
                else:
                    record[1] += 1
                record[2] += game_result[1]
                record[3] += game_result[0]
    record[2] /= num_of_games
    record[3] /= num_of_games
    return record

def away_stats_leading_up_to_game(cursor, year, game_id):
    team_name = get_results_by_game_id(cursor, game_id)[1]
    games_list = get_team_games_regular_season(cursor, team_name, year)
    stats = np.zeros(13).astype(int)
    num_of_games = 0
    for game in games_list:
        if game[0] < game_id:
            num_of_games += 1
            if game[1]:
                game_stats = np.array(get_stats_by_game_id_away(cursor, game[0])).astype(float)
            else:
                game_stats = np.array(get_stats_by_game_id_home(cursor, game[0])).astype(float)
            game_stats = game_stats[1:14:1]
            stats += game_stats.astype(int)

    return stats/num_of_games
         
def away_record_before_game(cursor, year, game_id):
    team_name = get_results_by_game_id(cursor, game_id)[1]
    games_list = get_team_games_regular_season(cursor, team_name, year)
    record = np.zeros(4) #[WINS, LOSSES, PPG Scored, PPG Allowed]
    num_of_games = 0
    for game in games_list:
        if game[0] < game_id:
            num_of_games += 1
            game_result = get_results_by_game_id(cursor, game[0])
            game_result = game_result[2:4:1]
            if game[1]:              
                if game_result[0] > game_result[1]:
                    record[0] += 1
                else:
                    record[1] += 1
                record[2] += game_result[0]
                record[3] += game_result[1]
            else:
                if game_result[1] > game_result[0]:
                    record[0] += 1
                else:
                    record[1] += 1
                record[2] += game_result[1]
                record[3] += game_result[0]
    record[2] /= num_of_games
    record[3] /= num_of_games
    return record

def average_stats_by_year(cursor, year):
    teams = get_team_names_by_year(cursor, year)
    average_stats_by_team = []
    for team in teams:
        team_stats = np.array(get_team_stats_regular_season(cursor, team, year)) # fgm, fga, 3pm, 3pa, ftm, fta, oreb, dreb, ast, stl, blk, tov, pf 
        team_stats = np.delete(team_stats, 0, axis=1)
        team_stats = team_stats.astype(float)
        team_stats = team_stats.astype(int)
        mean_team_stats = np.average(team_stats, axis=0)
        average_stats_by_team.append(mean_team_stats)
    league_averages = np.average(average_stats_by_team, axis=0)
    return league_averages

def range_of_stats_by_year(cursor, year):
    teams = get_team_names_by_year(cursor, year)
    team_maxima = []
    team_minima = []
    for team in teams:
        team_stats = np.delete(np.array(get_team_stats_regular_season(cursor, team, year)), 0, axis=1).astype(float)
        team_stats = team_stats.astype(int)
        team_maxima.append(np.max(team_stats, axis=0))
        team_minima.append(np.min(team_stats, axis=0))
    maxima = np.max(team_maxima, axis=0)
    minima = np.max(team_minima, axis=0)
    range = np.subtract(maxima, minima)
    return range




def compile_and_scale_features(cursor, year, game_id, ranges, averages):
    X_1 = home_record_before_game(cursor, year, game_id)
    home_games = X_1[0] + X_1[1]
    home_win_pct = np.array([X_1[0]/home_games])
    home_ppg_for_adjusted = np.array([X_1[2]/100])
    home_ppg_against_adjusted = np.array([X_1[3]/100])
    X_2 = home_stats_leading_up_to_game(cursor, year, game_id)
    X_2_norm = np.subtract(X_2, averages)
    X_2_norm = np.divide(X_2_norm, ranges)
    X_2_norm += 0.5
    X_3 = away_stats_leading_up_to_game(cursor, year, game_id)
    X_3_norm = np.subtract(X_3, averages)
    X_3_norm = np.divide(X_3_norm, ranges)
    X_3_norm += 0.5
    X_4 = away_record_before_game(cursor, year, game_id)
    away_games = X_4[0] + X_4[1]
    away_win_pct = np.array([X_4[0]/away_games])
    away_ppg_for_adjusted = np.array([X_4[2]/100])
    away_ppg_against_adjusted = np.array([X_4[3]/100])
    return np.concatenate([home_win_pct, home_ppg_for_adjusted, home_ppg_against_adjusted, 
                           X_2_norm,
                           X_3_norm,
                           away_win_pct, away_ppg_for_adjusted, away_ppg_against_adjusted]) #LENGTH = 32


#PREDICTS THE Y VALUE (home pts, away pts)
def f(X, W, b): 
    output = np.dot(X, W)
    return output + b


#USES GRADIENT DESCENT TO OPTIMIZE W & b
def find_coefficients_by_year(cursor, year):
    game_id_range = max_game_id(cursor, year)
    W = np.zeros(32)

    


def model(cursor):
   ranges = range_of_stats_by_year(cursor, 1997)
   print('Ranges Found')
   averages = average_stats_by_year(cursor, 1997)
   print('Averages Found')
   for i in range(10):
    game_no = 29700700 + i
    game_str = str(game_no)
    print(compile_and_scale_features(cursor, 1997, '00' + game_str, ranges, averages))



def main():

    try: 

        connection = sq.connect('game.sqlite')
        cursor = connection.cursor()
        print('Database connection initiated')

        query = 'select sqlite_version();'
        cursor.execute(query)
        result = cursor.fetchall()
        print('SQLite version: ', result)

        cursor.close()

    except sq.Error as error:
        print('Error occurred', error)

    finally:
        if connection:
            connection.close()
            print('Connection closed')



main()