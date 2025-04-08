import numpy as np
from bs4 import BeautifulSoup
import html5lib as html
import requests
import json
from backend.linreg import *

file = open("weights.json", "r")
data = json.load(file)

HOME_WEIGHTS = data['W']
AWAY_WEIGHTS = data['V']
HOME_INT = data['b']
AWAY_INT = data['a']




url = 'https://www.basketball-reference.com/leagues/NBA_2025.html#per_game-team'
r = requests.get(url)
content = r.text


soup = BeautifulSoup(content, 'html5lib').find_all('table')

table = soup[4].find_all('tr')

team_lookup = {
    'Atlanta Hawks' : 'ATL',
    'Boston Celtics' : 'BOS',
    'Brooklyn Nets' : 'BKN',
    'Charlotte Hornets' : 'CHA',
    'Chicago Bulls' : 'CHI',
    'Cleveland Cavaliers' : 'CLE',
    'Dallas Mavericks' : 'DAL',
    'Denver Nuggets' : 'DEN',
    'Detroit Pistons' : 'DET',
    'Golden State Warriors' : 'GSW',
    'Houston Rockets' : 'HOU',
    'Indiana Pacers' : 'IND',
    'Los Angeles Clippers' : 'LAC',
    'Los Angeles Lakers' : 'LAL',
    'Memphis Grizzlies' : 'MEM',
    'Miami Heat' : 'MIA',
    'Milwaukee Bucks' : 'MIL',
    'Minnesota Timberwolves' : 'MIN',
    'New Orleans Pelicans' : 'NOP',
    'New York Knicks' : 'NYK',
    'Oklahoma City Thunder' : 'OKC',
    'Orlando Magic' : 'ORL',
    'Philadelphia 76ers' : 'PHI',
    'Phoenix Suns' : 'PHX',
    'Portland Trail Blazers' : 'POR',
    'Sacramento Kings' : 'SAC',
    'San Antonio Spurs' : 'SAS',
    'Toronto Raptors' : 'TOR',
    'Utah Jazz' : 'UTA',
    'Washington Wizards' : 'WAS'
}

team_stats = {}
average_stats = np.zeros(16)

for team in team_lookup:
    team_symbol = team_lookup[team]
    team_stats[team_symbol] = np.zeros(16) # [win_pct, ppgf, ppga, fgm, fga, 3pm, 3pa, ftm, fta, oreb, dreb, ast, stl, blk, tov, pf]

for i in range(31):
    if i < 30:
        stat_soup = table[i+1]
        team_symbol = team_lookup[stat_soup.find('a').get_text()]
        team_data = stat_soup.find_all('td')
        team_data_parsed = [] # [team, gp, min, fgm, fga, fg%, 3pm, 3pa, 3p%, 2p, 2pa, 2p%, ftm, fta, ft%, oreb, dreb, reb, ast, stl, blk, tov, pf, pts] (length = 24)
        for data in team_data:
            team_data_parsed.append(data.get_text())
        team_stats[team_symbol][3] = team_data_parsed[3]
        team_stats[team_symbol][4] = team_data_parsed[4]
        team_stats[team_symbol][5] = team_data_parsed[6]
        team_stats[team_symbol][6] = team_data_parsed[7]
        team_stats[team_symbol][7] = team_data_parsed[12]
        team_stats[team_symbol][8] = team_data_parsed[13]
        team_stats[team_symbol][9] = team_data_parsed[15]
        team_stats[team_symbol][10] = team_data_parsed[16]
        team_stats[team_symbol][11] = team_data_parsed[18]
        team_stats[team_symbol][12] = team_data_parsed[19]
        team_stats[team_symbol][13] = team_data_parsed[20]
        team_stats[team_symbol][14] = team_data_parsed[21]
        team_stats[team_symbol][15] = team_data_parsed[22]
    else:
        stat_soup = table[i+1]
        team_data = stat_soup.find_all('td')
        team_data_parsed = [] # [team, gp, min, fgm, fga, fg%, 3pm, 3pa, 3p%, 2p, 2pa, 2p%, ftm, fta, ft%, oreb, dreb, reb, ast, stl, blk, tov, pf, pts] (length = 24)
        for data in team_data:
            team_data_parsed.append(data.get_text())
        average_stats[3] = team_data_parsed[3]
        average_stats[4] = team_data_parsed[4]
        average_stats[5] = team_data_parsed[6]
        average_stats[6] = team_data_parsed[7]
        average_stats[7] = team_data_parsed[12]
        average_stats[8] = team_data_parsed[13]
        average_stats[9] = team_data_parsed[15]
        average_stats[10] = team_data_parsed[16]
        average_stats[11] = team_data_parsed[18]
        average_stats[12] = team_data_parsed[19]
        average_stats[13] = team_data_parsed[20]
        average_stats[14] = team_data_parsed[21]
        average_stats[15] = team_data_parsed[22]
        average_stats = average_stats[3:16]

east_record_table = soup[0].find_all('tr')
west_record_table = soup[1].find_all('tr')

for i in range(30):
    if i < 15:
        record_soup = east_record_table[i+1]
    else:
        record_soup = west_record_table[i-14]
    team_symbol = team_lookup[record_soup.find('a').get_text()]
    team_record_data = record_soup.find_all('td')
    team_record_data_parsed = []
    for record_data in team_record_data:
        team_record_data_parsed.append(record_data.get_text())
    team_stats[team_symbol][0] = team_record_data_parsed[2]
    team_stats[team_symbol][1] = float(team_record_data_parsed[4])/100
    team_stats[team_symbol][2] = float(team_record_data_parsed[5])/100

range_of_stats = [23.25,  36.75,  16.25, 29.125, 28.5,   36.5,   17.875, 23.875, 23.375, 14, 13.75,  17.625, 20.25 ]

for team in team_stats:
    stats = team_stats[team]
    normalized_stats = stats[3:16]
    normalized_stats = np.subtract(normalized_stats, average_stats)
    normalized_stats = np.divide(normalized_stats, range_of_stats)
    normalized_stats += 0.5
    stats = np.array(stats)
    normalized_stats = np.array(normalized_stats)
    team_stats[team] = np.concatenate((stats[0:3], normalized_stats))    


def projections(W, V, b, a):

    home_symbol = input('Home Team: ')
    away_symbol = input('Away Team: ')

    home_stats = team_stats[home_symbol]
    away_stats = team_stats[away_symbol]

    X = np.concatenate((home_stats, away_stats))

    home_projection = np.dot(W, X) + b

    away_projection = np.dot(V, X) + a
    print('Home Stats: ', home_stats)
    print('Away Stats: ', away_stats)
    print('Predicted Home Points: ', home_projection)
    print('Predicted Away Points: ', away_projection)
    if home_projection>away_projection:
        print('Predicted Spread (Home): ', away_projection-home_projection)
    else:
        print('Predicted Spread (Home): +', away_projection-home_projection)
    print('Predicted Total Pts: ', home_projection+away_projection)


    return




projections(HOME_WEIGHTS, AWAY_WEIGHTS, HOME_INT, AWAY_INT)