import mysql.connector
from mysql.connector import errorcode
from new_db import DatabaseManager


# Config base pra acessar o database
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost'
}
database_name = 'hsr'

# pega a database chamada "hsr"
def database_exists(cursor, db_name):
    cursor.execute("SHOW DATABASES LIKE '%s'" % db_name)
    return cursor.fetchone()

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    if not database_exists(cursor, database_name): # se a database não existir, cria ela
        db_manager = DatabaseManager()
        db_manager.create_tables()
        db_manager.insert_data()
        print("Database criado")
    else:
        print("Acessando database") # se existir apenas segue o codigo
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Acesso negado.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database não existe.")
    else:
        print(err)
    
from login_gacha import * # roda o arquivo login_gacha