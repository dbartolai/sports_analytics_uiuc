from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
from nba_api.live.nba.endpoints import scoreboard
from dateutil import parser
import pandas
import numpy as np
from scraper import efficiency, ratings, adjusted_ratings, estimate_possessions


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

def clean_stats(team_id):
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
    games = gamefinder.get_data_frames()[0][0:15]
    
    array = games.to_numpy()
    
    # [seasonID, teamID, symbol, teamName, gameID, gameday, matchup, W/L, min, pts, fgm, fga, fg%, 3pm, 3pa, 3p%, ftm, fta, ft%, oreb, dreb, reb, ast, stl, blk, tov, pf, +/-]
    for game in array:

        all_games = leaguegamefinder.LeagueGameFinder().get_data_frames()[0]
        full_game = all_games[all_games.GAME_ID == game[4]].to_numpy()
        
        print(full_game[0][6])



    return


    

def get_stats_by_game():    
    games = get_scoreboard()['games']

    nba_teams = teams.get_teams()

    for game in games:

        home = game[1]
        away = game[2]

        print("GAME: ", game)

        home_team = [team for team in nba_teams if team['abbreviation'] == home][0]
        away_team = [team for team in nba_teams if team['abbreviation'] == away][0]

        home_id = home_team['id']
        away_id = away_team['id']

        print("HOME_ID:", home_id)
        print("AWAY_ID:", away_id)

        clean_stats(home_id)
        clean_stats(away_id)

        



# STATS OUTPUT MUST MATCH:

# HOME WIN_PCT, 
# HOME PPG / 200, 
# HOME PPGA / 200, 

# HOME STATS
    # NET
    # PACE / 100,
    # TRUE SHOOTING %,
    # EFFECTIVE FG %,
    # OREB %,
    # DREB %,
    # TURNOVER %,
    # ASSIST : TURNOVER

# AWAY STATS
    # NET
    # PACE / 100,
    # TRUE SHOOTING %,
    # EFFECTIVE FG %,
    # OREB %,
    # DREB %,
    # TURNOVER %,
    # ASSIST : TURNOVER

# AWAY WIN_PCT, 
# AWAY PPG / 200, 
# AWAY PPGA / 200, 
