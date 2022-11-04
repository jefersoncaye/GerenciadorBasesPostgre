#encoding: utf-8
import psycopg2
import subprocess
import os

arq = open('dados.txt', 'r')
try:
    for i in arq:
        if 'HOST:' in i:
            HOST = i
        if 'DATABASE:' in i:
            DATABASE = i
        if 'USER:' in i:
            USER = i
        if 'PASSWORD:' in i:
            PASSWORD = i
        if 'CAMINHO:' in i:
            CAMINHO = i
        if 'PG_DUMP:' in i:
            PG_DUMP = i
        if 'PSQL:' in i:
            PSQL = i
        if 'DROPDB:' in i:
            DROPDB = i
        if 'CREATEDB:' in i:
            CREATEDB = i
        if 'PG_RESTORE:' in i:
            PG_RESTORE = i
except:
    raise ValueError('Alguma Variavel nao foi encontrada')
arq.close()

host= HOST[5:].strip()
database= DATABASE[9:].strip()
user= USER[5:].strip()
password= PASSWORD[9:].strip()
caminho= CAMINHO[8:].strip()
pg_dump= PG_DUMP[8:].strip()
psql= PSQL[5:].strip()
dropdb= DROPDB[7:].strip()
createdb= CREATEDB[9:].strip()
pg_restore= PG_RESTORE[11:].strip()

os.putenv('PGPASSWORD', password)

try:
    con = psycopg2.connect(host= host, database= database, user= user, password=password)
    print('Conexao Criada com Sucesso!')
except: print('Erro ao Conectar no Servidor, verifique as credenciais!')

x = 0
while(x != 4):
    x = int(input('Opcoes:\n1- Backup de uma Base\n2- Backup de TODAS Bases\n3- Restaurar Backup\n4- Sair\n: '))
    if x == 1:
        if len(caminho) == 0:
            caminho = input('Caminho Gerar Backup: ')
        baseName = input('Nome da Base: ')
        print(f'fazendo backup Base: {baseName}')
        try:
            command = (f'{pg_dump} -h apus -p 5432 -U {user} -F c {baseName} > {caminho}\\{baseName}.backup')
            subprocess.call(command, shell=True)
            print("Backup Realizado com Sucesso!")
        except: print(f"Erro ao Fazer Backup Base {baseName}, Verifique!")
    if x ==2:
        if len(caminho) == 0:
            caminho = input('Caminho Gerar Backup: ')
        cur = con.cursor()
        cur.execute("SELECT datname FROM pg_database")
        bases = cur.fetchall()
        for i in bases:
            try:
                print(f'fazendo backup Base: {i[0]}')
                command = (f'{pg_dump} -h apus -p 5432 -U {user} -F c {i[0]} > {caminho}\\{i[0]}.backup')
                subprocess.call(command, shell=True)
                print("Backup Realizado com Sucesso!")
            except: print(f"Erro ao Fazer Backup Base {i[0]}, Verifique!")
    if x == 3:
        nomeBase = input('Nome do banco a restaurar: ')
        caminhoRestauraBkp = input('Caminho arquivo .backup:')
        print(f'Restaurando backup: {caminhoRestauraBkp}')
        try:
            command = (f'{psql} -h apus -p 5432 -U {user} -d {database} -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = ' + f"'{nomeBase}'")
            subprocess.call(command, shell=True)
            print("Usuarios Desconectados!")
        except:
            print(f"Erro ao Desconectar usuarios, Verifique!")
        try:
            command = (f'{dropdb} -h apus -p 5432 -U {user} {nomeBase}')
            subprocess.call(command, shell=True)
            print("Banco Desanexado")
        except:
            print(f"Erro ao Desanexar banco, Verifique!")
        try:
            command = (f'{createdb} -h apus -p 5432 -U {user} {nomeBase}')
            subprocess.call(command, shell=True)
            print("Novo Banco Criado")
        except:
            print(f"Erro ao Criar Novo Banco, Verifique!")
        try:
            command = (f'{pg_restore} -h apus -p 5432 -U {user} -d {nomeBase} < {caminhoRestauraBkp}')
            subprocess.call(command, shell=True)
            print("Backup Restaurado!")
        except:
            print(f"Erro ao Restaurar Backup, Verifique!")
    if x == 4:
        exit()
