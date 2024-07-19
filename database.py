import mysql.connector
import random

# Função para realizar uma consulta aleatória em uma tabela específica
def realizar_consulta_aleatoria(tabela, quantidade, cursor):
    try:
        # Constrói a consulta SQL com base na tabela e na quantidade especificada
        query = f"SELECT * FROM {tabela} ORDER BY RAND() LIMIT {quantidade}"

        # Executa a consulta
        cursor.execute(query)

        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()

        # Imprime os resultados
        for linha in resultados:
            print(linha)

    except mysql.connector.Error as e:
        print(f"Erro ao executar a consulta SQL: {e}")

# Função principal para escolher a operação
def escolher_operacao(conexao, cursor):
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
                realizar_consulta_aleatoria("gacha_ff", 1, cursor)
            elif escolha == 2:
                realizar_consulta_aleatoria("gacha_ff", 10, cursor)
            elif escolha == 3:
                realizar_consulta_aleatoria("gacha_arma", 1, cursor)
            elif escolha == 4:
                realizar_consulta_aleatoria("gacha_arma", 10, cursor)
            elif escolha == 5:
                realizar_consulta_aleatoria("gacha_base", 1, cursor)
            elif escolha == 6:
                realizar_consulta_aleatoria("gacha_base", 10, cursor)
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
    database="warps"
)

# Verificar se a conexão foi bem sucedida
if conexao.is_connected():
    print('Conexão ao banco de dados MySQL estabelecida.')

    # Cria um cursor para executar operações SQL
    cursor = conexao.cursor()

    # Chama a função para escolher a operação
    escolher_operacao(conexao, cursor)

    # Fecha o cursor e a conexão
    cursor.close()
    conexao.close()
