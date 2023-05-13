from bs4 import BeautifulSoup
import requests
from functools import reduce
import pandas as pd
import json
from database.main import add_team_info
#worlds_path_prefix = 'World%20Championship%2020'

# list with sufix of links to League of Legends Worlds
years_sufix = ['World%20Championship%2020'+str(i)+"/" for i in range(16, 23)]

# Constants
HEADER = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
BASE_URL = "https://gol.gg/"

LINKS = {"match_list": "https://gol.gg/tournament/tournament-matchlist/",
         "teams_rank": "https://gol.gg/tournament/tournament-ranking/"}


def get_teams_info_by_year(championship_sufix:str):
    # Teams table
    url = LINKS["teams_rank"] + championship_sufix

    page = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(page.content, "html.parser")
    tabelas = soup.find_all('table')
    tabela_teams = tabelas[0].find_all('tr')
    del tabela_teams[0]

    teams_list = []

    for i in tabela_teams:
        list_cols = i.find_all('td')
        if list_cols[0].text == '\xa0':
            continue

        # 0 : Time
        # 1 : winrate
        # 2 : wins
        # 3 : loses
        # 4 : game_duration
        # 5 : GDM
        
        link_team = list_cols[0].find('a')['href']
        team_name = list_cols[0].text
        team_wins = list_cols[4].text
        year_champ = url[-5:-1]

        teams_list.append([link_team, team_name, team_wins, year_champ])
    
    return teams_list



# comandos para teste e output am json

#transformando a lista de listas em um dicionário e salvando em um json

#funções de escrita JSON
def save_teams_info(teams_list:list, save_name:str):
    dicionario_de_times = dict()
    for item in teams_list:
        dicionario_de_times[item[1]] = {'link': item[0], 'wins': item[2], 'year': item[3]}  

    with open(f'data/{save_name}.json', 'w') as f:
        json.dump(dicionario_de_times, f, indent=4)

def save_players_info(players_list:list):
    try:
        dicionario_de_jogadores = get_all_players_info()
        for name, id, season in players_list:
            if id in dicionario_de_jogadores.keys():
                seasons = list(set(dicionario_de_jogadores[id]['season'] + [season]))
                dicionario_de_jogadores[id]['season'] = seasons
            else:
                dicionario_de_jogadores[id] = {'name': name, 'season': [season]}
    except:
        dicionario_de_jogadores = dict()
        for name, id, season in players_list:
            dicionario_de_jogadores[id] = {'name': name, 'season': [season]}

    with open(f'data/players.json', 'w') as f:
        json.dump(dicionario_de_jogadores, f, indent=3)


#funções de leitura JSON
def get_team_info(file_name:str, team_name:str):
    with open(f'data/{file_name}.json', 'r') as f:
        dicionario_de_times = json.load(f)
    
    return dicionario_de_times[team_name]

def get_player_info(player_name:str):
    with open(f'data/players.json', 'r') as f:
        dicionario_de_jogadores = json.load(f)
    
    return dicionario_de_jogadores[player_name]

def get_all_teams_info(file_name:str):
    with open(f'data/{file_name}.json', 'r') as f:
        dicionario_de_times = json.load(f)
    
    return dicionario_de_times

def get_all_players_info():
    with open(f'data/players.json', 'r') as f:
        dicionario_de_jogadores = json.load(f)
    
    return dicionario_de_jogadores

############################################
# Funções para obter informações de jogadores
def get_players(team_year_url:str, team_name:str, year:str):
    page = requests.get(team_year_url, headers=HEADER)
    soup = BeautifulSoup(page.content, 'html.parser')

    linhas_jogadores = soup.find_all('table')[-1].find_all('tr')

    del linhas_jogadores[0]

    if len(linhas_jogadores) > 5:
        del linhas_jogadores[0]

    temp_list = []
    counter = 0
    for linha in linhas_jogadores:
        if counter == 5:
            continue
        tds = linha.find_all('td')
        temp_list.append([team_name, year, tds[0].text.strip(), 
                        tds[1].text.replace(u'\xa0', ''), tds[1].find('a')['href']])
        counter += 1

    return temp_list


def get_players_id(link_table_of_players:str):
    page = requests.get(link_table_of_players, headers=HEADER)
    soup = BeautifulSoup(page.content, 'html.parser')

    linhas_jogadores = soup.find_all('table')[-1].find_all('tr')

    del linhas_jogadores[0]

    temp_list = []
    for row in linhas_jogadores:
        columns = row.find_all('td')
        player_name = columns[0].text.strip()
        player_id = columns[0].find('a')['href'].split('/')[2]
        season = columns[0].find('a')['href'].split('/')[3]
        temp_list.append([player_name, player_id, season])


    return temp_list



# lista_de_jogadores = get_players_id('https://gol.gg/players/list/season-S11/split-ALL/tournament-ALL/')
# save_players_info(lista_de_jogadores)




list_teams_test = get_teams_info_by_year(years_sufix[-1])
for time in list_teams_test:
    link = time[0]
    nome_time = time[1]
    wins = int(time[2])
    year = time[3]

    add_team_info(nome_time, link, wins, year)





