import mysql.connector
from mysql.connector import errorcode
from new_db import DatabaseManager


# Database configuration
config = {
    'user': 'root',
    'password': '',
    'host': 'localhost'
}

database_name = 'hsr'

def database_exists(cursor, db_name):
    cursor.execute("SHOW DATABASES LIKE '%s'" % db_name)
    return cursor.fetchone()

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    if not database_exists(cursor, database_name):
        db_manager = DatabaseManager()
        db_manager.create_tables()
        db_manager.insert_data()
        print("Database criado")
    else:
        print("Acessando database")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    
from login_gacha import *