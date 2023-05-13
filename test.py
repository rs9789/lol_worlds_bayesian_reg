from bs4 import BeautifulSoup
import requests
import pandas as pd
import json


links_dict = {
    'KR'  : 'https://gol.gg/tournament/tournament-ranking/LCK%20Summer%202022/',
	'CN'  : 'https://gol.gg/tournament/tournament-ranking/LPL%20Summer%202022/',
	'EUW' : 'https://gol.gg/tournament/tournament-ranking/LEC%20Summer%202022/',
	'NA'  : 'https://gol.gg/tournament/tournament-ranking/LCS%20Summer%202022/',
	'PCS' : 'https://gol.gg/tournament/tournament-ranking/PCS%20Summer%202022/',
	'VN'  : 'https://gol.gg/tournament/tournament-ranking/VCS%20Summer%202022/',
}
HEADER = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}


def save_teams_info(region:str):
    request = requests.get(links_dict[f'{region}'], headers=HEADER)
    soup = BeautifulSoup(request.content, 'html.parser')
    table_of_teams = soup.find_all('table')[0].find_all('tr')

    list_of_teams = []
    for item in table_of_teams:
        if len(item.find_all('td')) == 0:
            continue
        elif len(item.find_all('td')) > 2:
            team_name = item.find_all('td')[0].text.strip()
            team_link = item.find_all('td')[0].find('a')['href']
            team_wins = item.find_all('td')[4].text.strip()
            list_of_teams.append([team_name, team_link, region, team_wins])

    return list_of_teams


def get_team_stats(region_list:list):
    stats_list = []
    for team in region_list:
        team_name = team[0]
        team_link = 'https://gol.gg/' + team[1]
        team_wins = team[3]
        region = team[2]
        request = requests.get(team_link, headers=HEADER)
        soup = BeautifulSoup(request.content, 'html.parser')

        # index 7 is the economy stats table
        # index 10 is the aggression stats table but if region is CN the correct is 9
        if region == 'CN':
            economy = soup.find_all('table')[7].find_all('tr')
            aggression = soup.find_all('table')[9].find_all('tr')
        else:
            economy = soup.find_all('table')[7].find_all('tr')
            aggression = soup.find_all('table')[10].find_all('tr')

        try:
            gpm = economy[1].find_all('td')[1].text.strip()
            dpm = aggression[1].find_all('td')[1].text.strip()
            kpg = aggression[4].find_all('td')[1].text.strip()
            dpg = aggression[5].find_all('td')[1].text.strip()

            stats_list.append([team_name, region, gpm, dpm, kpg, dpg, team_wins])
        except:
            print(region)
    return stats_list

regions = ['KR', 'CN', 'EUW', 'NA', 'PCS', 'VN']

list_of_stats = []
for region in regions:
    teams = save_teams_info(region)
    stats = get_team_stats(teams)
    list_of_stats += stats

# print(list_of_stats)

df = pd.DataFrame(list_of_stats, columns=['team_name', 'region', 'gpm', 'dpm', 'kpg', 'dpg', 'wins'])
df.to_csv(f'teams_stats.csv', index=False)