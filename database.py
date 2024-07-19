import mariadb
import sys
import mysql.connector
import _random
# Estabelece a conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Lucas_nascimento"
)

# Cria um cursor para executar operações SQL
cursor = conexao.cursor()

# Verificar se a conexão foi bem sucedida
if conexao.is_connected():
    print('Conexão ao banco de dados MySQL estabelecida.')



consulta = "SELECT * FROM gacha_ff ORDER BY RAND() LIMIT 1"
consulta2 = "SELECT * FROM gacha_ff ORDER BY RAND() LIMIT 10"

# Executa a consulta
cursor.execute(consulta)

# Obtém todos os resultados da consulta
resultados = cursor.fetchall()

# Imprime os resultados
for linha in resultados:
    print(linha)

# Fecha o cursor e a conexão
cursor.close()
conexao.close()


#pip install mysql-connector-python