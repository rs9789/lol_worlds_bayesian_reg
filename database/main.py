import psycopg2

database = 'db_loltournament'

conn = psycopg2.connect(dbname=database, user='postgres', password='#Aluno234', host='localhost', port='5432')

print('Conectado ao banco de dados')
cursor = conn.cursor()
conn.autocommit = True

cursor.execute('''CREATE TABLE IF NOT EXISTS tb_tournament 
                    (id serial PRIMARY KEY,
                     team_name varchar(100) NOT NULL, 
                     link varchar(100) NOT NULL, 
                     wins int NOT NULL,
                     year varchar(4));''')


def get_teams_data(cursor = cursor):
    cursor.execute('SELECT * FROM tb_tournament;')
    return cursor.fetchall()

def add_team_info(team_name, link, wins, year, cursor = cursor):

    #obtém o ano do time passado no parâmetro da função para verificar a existência do dado na base
    cursor.execute(f'''SELECT year 
                       FROM tb_tournament 
                       WHERE team_name = \'{team_name}\' AND
                             year = \'{year}\';''')
    data_to_validate = cursor.fetchall()
    
    #valida se ja existe a informação de um time em determinado ano
    if data_to_validate == [] or year not in data_to_validate[0]:
        cursor.execute(f'INSERT INTO tb_tournament (team_name, link, wins, year) VALUES (\'{team_name}\', \'{link}\', {wins}, \'{year}\');')
        print('Time adicionado com sucesso')
    else:
        print('Já existe um time com esse nome e ano')



print(get_teams_data(cursor))


