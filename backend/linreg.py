import numpy as np
import sqlite3 as sq
from flask import Flask, jsonify
from numpy import random as r
import json
from queue import Queue
from scraper import *
from odds import *
import time

ALPHA = 0.1
N = 10000
FOLDS = 5
START_YEAR = 2017
END_YEAR = 2022



#PREDICTS THE Y VALUE (home pts, away pts)
def f(X, W, b): 
    output = np.dot(X, W)
    return output + b


#Execute gradient descent algorithm given clean data
def J(X, Y, W, m, b):
    J = 0
    for i in range(m):
        try:
            J += (Y[i] - f(X[i], W, b))*(Y[i] - f(X[i], W, b))
        except:
            print(i)
    return J/(2*m)
    

def dJ_dw(X, Y, W, m, b):
    dJ_dw = np.zeros(22)
    for i in range(m):
        dJ_dw += np.multiply(X[i], (f(X[i], W, b) - Y[i]))
    return np.divide(dJ_dw, m)

def dJ_db(X, Y, W, m, b):
    dJ_db = 0
    for i in range(m):
        dJ_db += (f(X[i], W, b) - Y[i])
    return dJ_db/m

def gradient_descent(X, Y, W, b, m):

    J_prev = 0
    for i in range(N):
        _J = J(X, Y, W, m, b)
        if abs(_J-J_prev) < 0.002: break
        _dJ_dw = dJ_dw(X, Y, W, m, b)
        _dJ_db = dJ_db(X, Y, W, m, b)
        W -= ALPHA * _dJ_dw
        b -= ALPHA * _dJ_db

    return W, b

    
def expected_val_spread(X, W, b, Y, V, a, Z, m, spreads):

    # Suppose we have $1 to place on each game within a training set, the EV
    # describes how much we are expected to win per game

    # Note I am using sportsbook spreads, which is [away score] - [home score]
    # If the Bulls beat the Pistons by 3 in Chicago, the home margin of victory is - 3
    # This aligns with my dataset

    EV = 0
    bets = 0
    for i in range(m):

        # bet_home is a boolean, describing if the model picks home to cover the book spread

        bet_home = True    


        predicted_spread = 0 - (f(X[i], W, b) - f(X[i], V, a)) # away - home
        sportsbook_spread = spreads[i]
        real_margin = 0 - (Y[i] - Z[i]) # away - home

        # If this condition holds, the model decides that the game is a tossup, and user should not place a bet
        if np.abs(predicted_spread - sportsbook_spread) < 2.5: continue
        else:
            bets += 1


        if predicted_spread > sportsbook_spread: bet_home = False

        # Now, if we bet_home, that means the real_margin (away - home) must be less than ther sportsbook_spread in order to hit
        # Standard spread odds are -110 for either side, which turns into a 1.909 (21/22) multiplier on your bet
        # In our case, you win ~ $1.91 if your bet hits, but 0 if it loses

        if bet_home and real_margin < sportsbook_spread:
            EV += 1.909

        elif not bet_home and real_margin > sportsbook_spread:
            EV += 1.909

        
    return (EV), bets


def expected_val_ou(X, W, b, Y, V, a, Z, m, OUs):
    EV = 0
    bets = 0

    for i in range(m):

        bet_over = True

        predicted_OU = (f(X[i], W, b) + f(X[i], V, a))
        sportsbook_OU = OUs[i]
        real_pts = Y[i] + Z[i]

        if np.abs(predicted_OU - sportsbook_OU) < 10.5: continue
        else: bets += 1

        if predicted_OU < sportsbook_OU: bet_over = False

        if bet_over and real_pts > sportsbook_OU:
            EV += 1.909
        elif not bet_over and real_pts < sportsbook_OU:
            EV += 1.909

    return (EV), bets





def find_coefficients_by_year_helper(odds, cursor, year, test_fold):

    X = []
    X_test = []
    Y_test = []
    Z_test = []
    spreads_test = []
    ou_test = []
    n = 0
    


    # HOME SCORE
    W = np.add(r.rand(22)*0.01, 0.05)
    b = 115
    Y = []

    #AWAY SCORE
    V = W.copy()
    a = 115
    Z = []

    max_id = max_game_id(cursor, year)
    first_id = first_game_id(year)
    
    m = int(max_id)-int(first_id)

    stats = {}
    records = {} 

    for team in get_team_names_by_year(cursor, year):
        stats[team] = Queue(maxsize=15)
        records[team] = Queue(maxsize=15)


    # PLACES DATA INTO NICE TABLES
    for game_id_int in range(int(first_id), int(max_id)+1):
        game_id = '00' + str(game_id_int)

        # result = [game_id, home, home score, away score, away]
        results = get_results_by_game_id(cursor, game_id) 
        

        spread = get_spread_by_game_id(odds, game_id)
        ou = get_ou_by_game_id(odds, game_id)

        # If any data doesn't exist, decrement number of games and skip the iteration

        if spread == None or ou == None or results == None:
            m-= 1
            continue

        home = results[1]
        away = results[4]

        
        rolling_average = rolling_averages(stats, records, home, away)
        if game_id_int % FOLDS != test_fold:
            X.append(rolling_average)
            Y.append(results[2])
            Z.append(results[3])
        else:
            X_test.append(rolling_average)
            Y_test.append(results[2])
            Z_test.append(results[3])
            spreads_test.append(spread)
            ou_test.append(ou)
            n+=1
        

        update_record_dict(cursor, records, game_id)
        update_stats_dict(cursor, stats, game_id, records)
    
    m*=0.8
    m = int(m)

    home_weights = gradient_descent(X, Y, W, b, m) 
    away_weights = gradient_descent(X, Z, V, a, m)

    home_cost = J(X_test, Y_test, home_weights[0], n, home_weights[1])
    away_cost = J(X_test, Z_test, away_weights[0], n, away_weights[1])

    spread_ev, spread_bets = expected_val_spread(X_test, home_weights[0], home_weights[1], Y_test, away_weights[0], away_weights[1], Z_test, n, spreads_test)
    OU_ev, OU_bets = expected_val_ou(X_test, home_weights[0], home_weights[1], Y_test, away_weights[0], away_weights[1], Z_test, n, ou_test)



    return home_weights, away_weights, home_cost, away_cost, spread_ev, spread_bets, OU_ev, OU_bets


def find_coefficients_by_year(odds, cursor, year):
    home_weights = np.zeros(22)
    away_weights = np.zeros(22)
    home_int = 0
    away_int = 0
    home_cost = 0
    away_cost = 0
    spread_ev = 0
    spread_bets = 0
    OU_ev = 0
    OU_bets = 0
    for i in range(FOLDS):  
        [fold_home_weights, fold_home_int], [fold_away_weights, fold_away_int], fold_home_cost, fold_away_cost, fold_spread_ev, fold_spread_bets, fold_OU_ev, fold_OU_bets = find_coefficients_by_year_helper(odds, cursor, year, i)
        home_weights += fold_home_weights
        away_weights += fold_away_weights
        home_int += fold_home_int
        away_int += fold_away_int
        home_cost += fold_home_cost
        away_cost += fold_away_cost
        spread_ev += fold_spread_ev
        spread_bets += fold_spread_bets
        OU_ev += fold_OU_ev
        OU_bets += fold_OU_bets


    home_weights = np.divide(home_weights, FOLDS)
    away_weights = np.divide(away_weights, FOLDS)
    home_int /= FOLDS
    away_int /= FOLDS
    home_cost /= FOLDS
    away_cost /= FOLDS
    

    return home_weights, home_int, away_weights, away_int, home_cost, away_cost, spread_ev, spread_bets, OU_ev, OU_bets
        


def model(odds, cursor, start_year, end_year):
    home_weights = np.zeros(22)
    home_int = 0
    away_weights = np.zeros(22)
    away_int = 0
    num_years = 0
    home_cost = 0
    away_cost = 0
    spread_ev = 0
    spread_bets = 0
    OU_ev = 0
    OU_bets = 0
    for year in range(start_year, end_year):
        print(year, 'Training Begins')
        num_years += 1
        year_home_weights, year_home_intercept, year_away_weights, year_away_intercept, year_home_cost, year_away_cost, year_spread_ev, year_spread_bets, year_OU_ev, year_OU_bets =  find_coefficients_by_year(odds, cursor, year)
        home_weights += year_home_weights
        home_int += year_home_intercept
        home_cost += year_home_cost
        away_weights += year_away_weights
        away_int += year_away_intercept
        away_cost += year_away_cost
        spread_ev += year_spread_ev
        spread_bets += year_spread_bets
        OU_ev += year_OU_ev
        OU_bets += year_OU_bets
    home_weights = np.divide(home_weights, num_years)
    home_int /= num_years
    home_cost /= num_years
    away_weights = np.divide(away_weights, num_years)
    away_int /= num_years
    away_cost /= num_years
    spread_ev /= spread_bets
    OU_ev /= OU_bets
    return home_weights, home_int, home_cost, away_weights, away_int, away_cost, spread_ev, spread_bets, OU_ev, OU_bets





def main():

    start = [time.localtime().tm_hour, time.localtime().tm_min]



    try: 

        connection = sq.connect('nba.sqlite')
        cursor = connection.cursor()
        print('Database connection initiated')

        odds_connection = sq.connect('odds.sqlite')
        odds_cursor = odds_connection.cursor()
        print('Odds Connection Initiated')

        query = 'select sqlite_version();'
        cursor.execute(query)
        result = cursor.fetchall()
        print('SQLite version: ', result)

        output = model(odds_cursor, cursor, START_YEAR, END_YEAR)
        params = {}

        params['W'] = str(output[0])
        params['b'] = str(output[1])
        params['V'] = str(output[3])
        params['a'] = str(output[4])
        params['home_cost'] = str(output[2])
        params['away_cost'] = str(output[5])
        params['spread_ev'] = str(output[6])
        params['spread_bets'] = str(output[7])
        params['OU_ev'] = str(output[8])
        params['OU_bets'] = str(output[9])


        file = open('./weights.json', 'w')
        json.dump(params, file, indent=4)
        file.close


        cursor.close()
        odds_cursor.close()

    except sq.Error as error:
        print('Error occurred', error)

    finally:
        if connection:
            connection.close()
            print('Connection closed')
        if odds_connection:
            odds_connection.close()

        end = [time.localtime().tm_hour, time.localtime().tm_min]
        time_elapsed = 0
        if end[0] > start[0]:
            time_elapsed += 60
        time_elapsed += (end[1] - start[1])

        print("Training complete after", time_elapsed, "minutes.")

        return output




main()

