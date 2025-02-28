import numpy as np
from bs4 import BeautifulSoup
import html5lib as html
import requests


HOME_WEIGHTS = [5.02124053, 16.443735, 10.91904736, 6.84824854, -7.78700208,
                1.85553683, 8.87307, 10.82672048, -12.95541701, 0.25751445,
                9.30917861, -3.65228687, 6.07029598, -0.90557146, -3.00940943,
                -2.84785016, -2.57784933, 3.4773734, 5.71445029, 4.88303566,
                -2.74230958, 1.19965877, -2.52196451, -2.600907, -3.18872132,
                5.05401038, 4.94615396, 8.98158206, -4.33296655, -7.89830281,
                8.29333624, 18.09517489]

home_int = 41.22868055278398

AWAY_WEIGHTS = [-5.92427756, 15.59732819, 29.99447984, -8.4000316, 3.3449414,
                11.14903387, -2.13582992, 4.23396469, -13.72169587, 1.57406808,
                5.36276819, -8.08246285, 3.95021134, 1.58638282, 1.5644094,
                -3.27819463, 3.31969929, 3.97400136, -9.18664699, 9.04737326,
                -2.67852692, 5.65223411, -9.29964311, 5.16713317, 3.98777983,
                0.63129273, 2.15202934, 3.10300919, -3.6420731, -0.60719005,
                13.94517924, 6.16162146]

away_int = 36.677876138936625

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


def projections(W, b, V, a):

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




