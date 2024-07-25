import mysql.connector

class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  
        )

    def create_db(self):
        try:
            conn_temp = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""  
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
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(100) NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gacha_arma (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(100) NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS gacha_base (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nome VARCHAR(100) NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS login (
                     id INT PRIMARY KEY AUTO_INCREMENT,
                     nome VARCHAR(100),
                     senha VARCHAR(100)
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS save_char (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT,
                    character_id INT,
                    quantidade SMALLINT NOT NULL,
                    jade SMALLINT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES login(id),
                    FOREIGN KEY (character_id) REFERENCES gacha_ff(id)
                )
            ''')
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def insert_data(self):
        try:
            cursor = self.conn.cursor()  
            cursor.execute('''
                INSERT INTO login (nome,senha) VALUES ('debug','000')                                        
            ''')


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
                                                ('arma1'),
                                                ('arma2'),
                                                ('arma3'),
                                                ('arma4'),
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
                                                ('base1'),
                                                ('base2'),
                                                ('base3'),
                                                ('base4'),
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


    def insert_user_inventory(self, user_id, item_type, item_id):
        try:
            cursor = self.conn.cursor()
            query = '''
                INSERT INTO user_inventory (user_id, item_type, item_id)
                VALUES (%s, %s, %s)
            '''
            cursor.execute(query, (user_id, item_type, item_id))
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_user_inventory(self, user_id):
        try:
            cursor = self.conn.cursor()
            query = '''
                SELECT item_type, gacha_ff.nome as item_name FROM user_inventory
                LEFT JOIN gacha_ff ON user_inventory.item_type = 'ff' AND user_inventory.item_id = gacha_ff.id
                LEFT JOIN gacha_arma ON user_inventory.item_type = 'arma' AND user_inventory.item_id = gacha_arma.id
                LEFT JOIN gacha_base ON user_inventory.item_type = 'base' AND user_inventory.item_id = gacha_base.id
                WHERE user_inventory.user_id = %s
            '''
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

# Usage example
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_db()
    db_manager.create_tables()
    db_manager.insert_data()

    # Exemplo de uso das novas funções
    db_manager.insert_user_inventory(1, 'ff', 1)
    db_manager.insert_user_inventory(1, 'arma', 2)
    db_manager.insert_user_inventory(1, 'base', 3)

    user_inventory = db_manager.get_user_inventory(1)
    for item in user_inventory:
        print(item)
