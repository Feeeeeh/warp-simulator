import mysql.connector

# essa classe cria o database e salva os dados do usuario
class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        self.create_db()
        self.conn.database = "HSR"

    def create_db(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('CREATE DATABASE IF NOT EXISTS HSR')
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
                    nome VARCHAR(255),
                    quantidade INT,
                    jade INT,
                    FOREIGN KEY (user_id) REFERENCES login(id),
                    UNIQUE(user_id, nome) -- faz com que cada usuario tenha entradas unicas
                )
            ''')
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def insert_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO login (nome, senha) VALUES ('debug', '000')
            ''')

            cursor.execute('''
                INSERT INTO gacha_ff (nome) VALUES
                ('qiqi'), ('firefly1'), ('firefly2'), ('firefly3'), ('firefly4'),
                ('lixo1'), ('lixo2'), ('lixo3'), ('lixo4'), ('lixo5'),
                ('lixo6'), ('lixo7'), ('lixo8'), ('lixo9'), ('lixo10'),
                ('lixo11'),('lixo12'),('lixo13'),('lixo14'),('lixo15'),
                ('lixo16'),('lixo17'),('lixo18'),('lixo19'),('lixo20'),
                ('lixo21'),('lixo22'),('lixo23'),('lixo24'),('lixo25'),
                ('lixo26'),('lixo27'),('lixo28'),('lixo29'),('lixo30'),
                ('lixo31'),('lixo32'),('lixo33'),('lixo34'),('lixo35')
            ''')
            cursor.execute('''
                INSERT INTO gacha_arma (nome) VALUES
                ('qiqi'), ('arma1'), ('arma2'), ('arma3'), ('arma4'),
                ('lixo1'), ('lixo2'), ('lixo3'), ('lixo4'), ('lixo5'),
                ('lixo6'), ('lixo7'), ('lixo8'), ('lixo9'), ('lixo10'),
                ('lixo11'),('lixo12'),('lixo13'),('lixo14'),('lixo15'),
                ('lixo16'),('lixo17'),('lixo18'),('lixo19'),('lixo20'),
                ('lixo21'),('lixo22'),('lixo23'),('lixo24'),('lixo25'),
                ('lixo26'),('lixo27'),('lixo28'),('lixo29'),('lixo30')
            ''')
            cursor.execute('''
                INSERT INTO gacha_base (nome) VALUES
                ('qiqi'), ('base1'), ('base2'), ('base3'), ('base4'),
                ('lixo1'), ('lixo2'), ('lixo3'), ('lixo4'), ('lixo5'),
                ('lixo6'), ('lixo7'), ('lixo8'), ('lixo9'), ('lixo10'),
                ('lixo11'),('lixo12'),('lixo13'),('lixo14'),('lixo15'),
                ('lixo16'),('lixo17'),('lixo18'),('lixo19'),('lixo20'),
                ('lixo21'),('lixo22'),('lixo23'),('lixo24'),('lixo25'),
                ('lixo26'),('lixo27'),('lixo28'),('lixo29'),('lixo30')
            ''')
            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

# exemplo de uso
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.create_tables()
    db_manager.insert_data()
    print("ta feito chefe")
