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

# Exemplo de consulta SQL
consulta = "SELECT * FROM gacha_ff"

# Executa a consulta
cursor.execute(consulta)

# Obtém todos os resultados da consulta
resultados = cursor.fetchall()

# Imprime os resultados
for linha in resultados:
    _random
    print(linha)

# Fecha o cursor e a conexão
cursor.close()
conexao.close()


