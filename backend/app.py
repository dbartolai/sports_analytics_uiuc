from flask import Flask
from flask_cors import CORS
import boto3
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
from nba_api.live.nba.endpoints import scoreboard
from dateutil import parser
import json


def get_weights():
    file = open('weights.json')
    return json.load(file)

def get_scoreboard():

    month_lookup = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
    ]


    f = '{gameId}: {away} @ {home}'
    todays_games = []

    board = scoreboard.ScoreBoard()

    games = board.games.get_dict()
    

    for game in games:
        todays_games.append([game['gameId'], game['homeTeam']['teamTricode'], game['awayTeam']['teamTricode']])

    date = parser.parse(board.score_board_date, yearfirst=True)
    date_str = f'{month_lookup[date.month - 1]} {date.day}, {date.year}'

    output = {
        'number': len(games),
        'date': date_str,
        'games' : todays_games
    }

    return output

# This document needs to get stats for the last 15 games 

app = Flask(__name__)
CORS(app)

@app.route('/scoreboard')
def main_page():
    return get_scoreboard()





if __name__ == '__main__':
    app.run(debug=True)

