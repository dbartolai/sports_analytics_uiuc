# This class can get all the game data for a year
# X: rows of efficiency stats from each game (home and away)
# Y: home score from each game
# Z: away score from each game
# M: score margin from each game (away - home)
# S: sportabooks spread from each game (away - home)
# W: 1 if the spread hits for home team, 0 otherwise


from scraper import *
from odds import *
import sqlite3 as sq
import numpy as np
from queue import Queue

class GameData:
    def __init__(self, year):
        self.X = []
        self.Y = []
        self.Z = []
        self.M = []
        self.S = []
        self.W = []
        self.first_id = 0
        self.last_id = 0
        self.get_data(year)

    def data_helper(self, cursor, odds, year):

        self.first_id = int(first_game_id(year))
        self.last_id = int(max_game_id(cursor, year))

        m =  self.last_id - self.first_id

        stats, records = {}, {}


        for team in get_team_names_by_year(cursor, year):
            stats[team] = Queue(maxsize=15)
            records[team] = Queue(maxsize=15)

        for game_id_int in range(self.first_id, self.last_id+1):
            game_id = '00' + str(game_id_int)

            results = get_results_by_game_id(cursor, game_id) 
            spread = get_spread_by_game_id(odds, game_id)

            #TEST
            if spread == None or results == None:
                m -= 1
                continue

            home = results[1]
            away = results[4]

            rolling_average = rolling_averages(stats, records, home, away)

            self.X.append(rolling_average)
            self.Y.append(results[2])
            self.Z.append(results[3])
            self.M.append(results[3] - results[2])
            self.S.append(spread)

            if (results[3] - results[2]) < spread: self.W.append(1)
            else: self.W.append(0)


    def get_data(self, year):
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

            data = self.data_helper(cursor, odds_cursor, year)

        except sq.Error as error:
            print('Error occurred', error)

        finally:
            if connection:
                connection.close()
                print('Connection closed')
            if odds_connection:
                odds_connection.close()
            

            return data
        

