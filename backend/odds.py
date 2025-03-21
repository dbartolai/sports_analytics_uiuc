import numpy as np
import sqlite3 as sq


def get_spread_by_game_id(cursor, game_id):
    statement = f'SELECT HomeSpread_AtClose from BettingOdds_History WHERE GAME_ID = \'{str(game_id)}\''
    cursor.execute(statement)
    spread = cursor.fetchone()
    try:
        return spread[0]
    except:
        pass

def get_ou_by_game_id(cursor, game_id):
    statement = f'SELECT Over_AtClose from BettingOdds_History WHERE GAME_ID = \'{game_id}\''
    cursor.execute(statement)
    ou = cursor.fetchone()
    try:
        return ou[0]
    except:
        pass

def get_homeML_by_game_id(cursor, game_id):
    statement = f'SELECT HomeML from BettingOdds_History WHERE GAME_ID = \'{game_id}\''
    cursor.execute(statement)
    homeML = cursor.fetchone()
    return homeML[0]

def get_awayML_by_game_id(cursor, game_id):
    statement = f'SELECT AwayML from BettingOdds_History WHERE GAME_ID = \'{game_id}\''
    cursor.execute(statement)
    awayML = cursor.fetchone()
    return awayML[0]