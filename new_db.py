import mysql.connector

class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # Coloque sua senha do MySQL aqui
        )

    def create_db(self):
        try:
            conn_temp = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""  # Coloque sua senha do MySQL aqui
            )
            cursor = conn_temp.cursor()
            cursor.execute('CREATE DATABASE IF NOT EXISTS HSR')
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if 'conn_temp' in locals():
                conn_temp.close()  # Fechar conexão temporária se estiver aberta

        # Reconectar ao banco de dados "HSR" usando a conexão principal
        try:
            self.conn.database = "HSR"
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gacha_ff (
                    nome VARCHAR(100) NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gacha_arma (
                    nome VARCHAR(100) NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gacha_base (
                    nome VARCHAR(100) NOT NULL
                )
            ''')
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def insert_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO gacha_ff (nome) VALUES ('qiqi'),
                                              ('firefly1'),
                                              ('firefly2'),
                                              ('firefly3'),
                                              ('firefly4'),
                                              ('lixo1'),
                                              ('lixo2'),
                                              ('lixo3'),
                                              ('lixo4'),
                                              ('lixo5'),
                                              ('lixo6'),
                                              ('lixo7'),
                                              ('lixo8'),
                                              ('lixo9'),
                                              ('lixo10'),
                                              ('lixo11')
            ''')
            cursor.execute('''
                INSERT INTO gacha_arma (nome) VALUES ('qiqi'),
                                                ('firefly1'),
                                                ('firefly2'),
                                                ('firefly3'),
                                                ('firefly4'),
                                                ('lixo1'),
                                                ('lixo2'),
                                                ('lixo3'),
                                                ('lixo4'),
                                                ('lixo5'),
                                                ('lixo6'),
                                                ('lixo7'),
                                                ('lixo8'),
                                                ('lixo9'),
                                                ('lixo10'),
                                                ('lixo11')
            ''')
            cursor.execute('''
                INSERT INTO gacha_base (nome) VALUES ('qiqi'),
                                                ('firefly1'),
                                                ('firefly2'),
                                                ('firefly3'),
                                                ('firefly4'),
                                                ('lixo1'),
                                                ('lixo2'),
                                                ('lixo3'),
                                                ('lixo4'),
                                                ('lixo5'),
                                                ('lixo6'),
                                                ('lixo7'),
                                                ('lixo8'),
                                                ('lixo9'),
                                                ('lixo10'),
                                                ('lixo11')
            ''')
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

# Usage example
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_db()
    db_manager.create_tables()
    db_manager.insert_data()