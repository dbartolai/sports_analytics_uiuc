import numpy as np
import kagglehub 
import sqlite3 as sq
from flask import Flask, jsonify
from numpy import random as r

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




def compile_and_scale_features(cursor, year, game_id, ranges, averages, stats, records):
    results = get_results_by_game_id(cursor, game_id) 
    home_team = results[1]                
    away_team = results[4]

    X_1 = records[home_team]
    home_games = X_1[0] + X_1[1]
    home_win_pct = np.array([X_1[0]/home_games])
    home_ppg_for_adjusted = np.array([X_1[2]/100])
    home_ppg_against_adjusted = np.array([X_1[3]/100])
    X_2 = stats[home_team]
    X_2_norm = np.subtract(X_2, averages)
    X_2_norm = np.divide(X_2_norm, ranges)
    X_2_norm += 0.5
    X_3 = stats[away_team]
    X_3_norm = np.subtract(X_3, averages)
    X_3_norm = np.divide(X_3_norm, ranges)
    X_3_norm += 0.5
    X_4 = records[away_team]
    away_games = X_4[0] + X_4[1]
    away_win_pct = np.array([X_4[0]/away_games])
    away_ppg_for_adjusted = np.array([X_4[2]/100])
    away_ppg_against_adjusted = np.array([X_4[3]/100])
    return np.concatenate([home_win_pct, home_ppg_for_adjusted, home_ppg_against_adjusted, 
                           X_2_norm,
                           X_3_norm,
                           away_win_pct, away_ppg_for_adjusted, away_ppg_against_adjusted]) #LENGTH = 32




def update_record_dict(cursor, records, game_id):
    results = get_results_by_game_id(cursor, game_id) # [game_id, home, home score, away score, away]
    home_team = results[1]                
    away_team = results[4]

    home_total_pts_for = (records[home_team][2])*(records[home_team][0] + records[home_team][1])
    records[home_team][2] = (home_total_pts_for + results[2])/(records[home_team][0] + records[home_team][1] + 1)

    home_total_pts_against = (records[home_team][3])*(records[home_team][0] + records[home_team][1])
    records[home_team][3] = (home_total_pts_against + results[3])/(records[home_team][0] + records[home_team][1] + 1)

    away_total_pts_for = (records[away_team][2])*(records[away_team][0] + records[away_team][1])
    records[away_team][2] = (away_total_pts_for + results[3])/(records[away_team][0] + records[away_team][1] + 1)

    away_total_pts_against = (records[away_team][3])*(records[away_team][0] + records[away_team][1])
    records[away_team][3] = (away_total_pts_against + results[2])/(records[away_team][0] + records[away_team][1] + 1)
    if results[2] > results[3]:
        records[home_team][0]+=1
        records[away_team][1]+=1
    else:
        records[home_team][1]+=1
        records[away_team][0]+=1

def games_played(records, team):
    return records[team][1] + records[team][2]

def update_stats_dict(cursor, stats, records, game_id):
    results = get_results_by_game_id(cursor, game_id) 
    home_team = results[1]                
    away_team = results[4]

    home_games_played = games_played(records, home_team)
    away_games_played = games_played(records, away_team)

    home_stats = stats[home_team]
    away_stats = stats[away_team]

    home_stats = np.multiply(home_stats, home_games_played)
    away_stats = np.multiply(away_stats, away_games_played)

    home_stats += get_stats_by_game_id_home(cursor, game_id)[1:14]
    away_stats += get_stats_by_game_id_away(cursor, game_id)[1:14]

    home_stats /= (home_games_played + 1)
    away_stats /= (away_games_played + 1)





#PREDICTS THE Y VALUE (home pts, away pts)
def f(X, W, b): 
    output = np.dot(X, W)
    return output + b



#Execute gradient descent algorithm given clean data
def J(X, Y, W, m, b):
    J = 0
    for i in range(m-30):
        J += (Y[i] - f(X[i], W, b))*(Y[i] - f(X[i], W, b))
    return J/(2*m)

def dJ_dw(X, Y, W, m, b):
    dJ_dw = np.zeros(32)
    for i in range(m-30):
        dJ_dw += np.multiply(X[i], (f(X[i], W, b) - Y[i]))
    return np.divide(dJ_dw, m)

def dJ_db(X, Y, W, m, b):
    dJ_db = 0
    for i in range(m-30):
        dJ_db += (f(X[i], W, b) - Y[i])
    return dJ_db/m

N = 10000
def gradient_descent(X, Y, W, b, m):

    alpha = 0.1
    J_prev = 0
    for i in range(N):
        _J = J(X, Y, W, m, b)
        if abs(_J-J_prev) < 0.002: break
        if i%1000 == 0: print('Iteration: ', i, "; Cost: ",_J, "; Weights: ", W)
        _dJ_dw = dJ_dw(X, Y, W, m, b)
        _dJ_db = dJ_db(X, Y, W, m, b)
        W -= alpha * _dJ_dw
        b -= alpha * _dJ_db

    return W, b

def find_coefficients_by_year(cursor, year):

    # HOME SCORE
    X = []
    W = np.add(r.rand(32)*0.005, 0.02)
    b = 100
    Y = []

    #AWAY SCORE
    V = W.copy()
    a = 100
    Z = []

    max_id = max_game_id(cursor, year)
    min_id = min_game_id(year)
    first_id = first_game_id(year)
    
    m = int(max_id)-int(first_id)

    averages = average_stats_by_year(cursor, year)
    ranges = range_of_stats_by_year(cursor, year)

    # IDEA: MAKE MORE EFFICIENT BY STORING EACH TEAM'S MOST
    # RECENT AVERAGE STATS AND NUMBER OF GAMES PLAYED IN A TABLE. THIS WAY
    # WE DON"T ITERATE THROUGH HUNDREDS OF GAMES FOR EACH GAME.

    stats = {} # {team : stats}
    records = {} # {team : [W, L, PPGf, PPGa]}

    for team in get_team_names_by_year(cursor, year):
        stats[team] = np.zeros(13)
        records[team] = np.zeros(4)


    # PLACES DATA INTO NICE TABLES
    for game_id_int in range(int(first_id), int(max_id)+1):
        game_id = '00' + str(game_id_int)
        results = get_results_by_game_id(cursor, game_id) 
        if results == None:
            m-= 1
            continue
        home_team = results[1]                
        away_team = results[4]
        if game_id <= min_id:
            update_record_dict(cursor, records, game_id)
            home_stats = get_stats_by_game_id_home(cursor, game_id)[1:14]
            away_stats = get_stats_by_game_id_away(cursor, game_id)[1:14]
            stats[home_team] = home_stats
            stats[away_team] = away_stats
        else:
            X.append(compile_and_scale_features(cursor, year, game_id, ranges, averages, stats, records)) #LENGTH = 32
            results = get_results_by_game_id(cursor, game_id)
            Y.append(results[2]) # HOME SCORE
            Z.append(results[3]) # AWAY SCORE
            update_stats_dict(cursor, stats, records, game_id)
            update_record_dict(cursor, records, game_id)


    return gradient_descent(X, Y, W, b, m), gradient_descent(X, Z, V, a, m)


def model(cursor, start_year, end_year):
    home_weights = np.zeros(32)
    home_int = 0
    away_weights = np.zeros(32)
    away_int = 0
    num_years = 0
    for year in range(start_year, end_year):
        print(year, 'Training Begins')
        num_years += 1
        [year_home_weights, year_home_intercept], [year_away_weights, year_away_intercept] =  find_coefficients_by_year(cursor, year)
        home_weights += year_home_weights
        home_int += year_home_intercept
        away_weights += year_away_weights
        away_int += year_away_intercept
        print(year, 'Training Complete')
    home_weights = np.divide(home_weights, num_years)
    home_int /= num_years
    away_weights = np.divide(away_weights, num_years)
    away_int /= num_years
    return home_weights, home_int, away_weights, away_int


params = {}
def main():

    try: 

        connection = sq.connect('nba.sqlite')
        cursor = connection.cursor()
        print('Database connection initiated')

        query = 'select sqlite_version();'
        cursor.execute(query)
        result = cursor.fetchall()
        print('SQLite version: ', result)

        print()

        output = model(cursor, 2015, 2023)

        params['W'] = output[0]
        params['b'] = output[1]
        params['V'] = output[2]
        params['a'] = output[3]

        print(params)


        cursor.close()

    except sq.Error as error:
        print('Error occurred', error)

    finally:
        if connection:
            connection.close()
            print('Connection closed')

        return output



main()
