import mysql.connector
import random
import new_db_test
class DatabaseManager:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="HSR"
        )
        self.cursor = self.conn.cursor()

    def insert_or_update_save_char(self, user_id, item_type, item_id):
        try:
            # Verifica se o registro já existe
            query = '''
                SELECT id, quantidade FROM save_char
                WHERE user_id = %s AND character_id = %s AND item_type = %s
            '''
            self.cursor.execute(query, (user_id, item_id, item_type))
            result = self.cursor.fetchone()

            if result:
                # Atualiza o registro existente
                save_char_id, quantidade = result
                new_quantidade = quantidade + 1
                update_query = '''
                    UPDATE save_char SET quantidade = %s
                    WHERE id = %s
                '''
                self.cursor.execute(update_query, (new_quantidade, save_char_id))
            else:
                # Insere um novo registro
                insert_query = '''
                    INSERT INTO save_char (user_id, character_id, quantidade, jade, item_type)
                    VALUES (%s, %s, %s, %s, %s)
                '''
                self.cursor.execute(insert_query, (user_id, item_id, 1, 0, item_type))

            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def realizar_consulta_aleatoria(self, tabela, quantidade, user_id):
        try:
            # Constrói a consulta SQL com base na tabela e na quantidade especificada
            query = f"SELECT id, nome FROM {tabela} ORDER BY RAND() LIMIT {quantidade}"

            # Executa a consulta
            self.cursor.execute(query)

            # Obtém todos os resultados da consulta
            resultados = self.cursor.fetchall()

            # Insere ou atualiza os itens na tabela save_char
            for linha in resultados:
                item_id, item_nome = linha
                self.insert_or_update_save_char(user_id, tabela.split('_')[1], item_id)
                print(f"Item retirado: {item_nome}")

        except mysql.connector.Error as e:
            print(f"Erro ao executar a consulta SQL: {e}")

    def escolher_operacao(self, user_id):
        try:
            while True:
                # Mostra opções para o usuário
                print("\nOpções disponíveis:")
                print("1. Realizar pull aleatório de gacha_ff (1 item)")
                print("2. Realizar pull aleatório de gacha_ff (10 itens)")
                print("3. Realizar pull aleatório de gacha_arma (1 item)")
                print("4. Realizar pull aleatório de gacha_arma (10 itens)")
                print("5. Realizar pull aleatório de gacha_base (1 item)")
                print("6. Realizar pull aleatório de gacha_base (10 itens)")
                print("7. Sair do programa")

                # Solicita ao usuário que escolha uma opção
                escolha = int(input("Escolha o número correspondente à operação que deseja executar: "))

                if escolha == 1:
                    self.realizar_consulta_aleatoria("gacha_ff", 1, user_id)
                elif escolha == 2:
                    self.realizar_consulta_aleatoria("gacha_ff", 10, user_id)
                elif escolha == 3:
                    self.realizar_consulta_aleatoria("gacha_arma", 1, user_id)
                elif escolha == 4:
                    self.realizar_consulta_aleatoria("gacha_arma", 10, user_id)
                elif escolha == 5:
                    self.realizar_consulta_aleatoria("gacha_base", 1, user_id)
                elif escolha == 6:
                    self.realizar_consulta_aleatoria("gacha_base", 10, user_id)
                elif escolha == 7:
                    print("Encerrando o programa...")
                    break
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")

        except ValueError:
            print("Por favor, digite um número válido para a escolha da operação.")

        except Exception as e:
            print(f"Ocorreu um erro: {e}")

# Conectar ao banco de dados MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="HSR"
)

# Verificar se a conexão foi bem sucedida
if conexao.is_connected():
    print('Conexão ao banco de dados MySQL estabelecida.')

    # Cria um cursor para executar operações SQL
    cursor = conexao.cursor()

    # Chama a função para escolher a operação
    db_manager = DatabaseManager()
    user_id = 1  # Substitua pelo ID do usuário correto
    db_manager.escolher_operacao(user_id)

    # Fecha o cursor e a conexão
    cursor.close()
    conexao.close()
