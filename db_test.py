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
def escolher_operacao(opcao, cursor):
    if opcao == 1:
        realizar_consulta_aleatoria("gacha_ff", 1, cursor)
    elif opcao == 2:
        realizar_consulta_aleatoria("gacha_ff", 10, cursor)
    elif opcao == 3:
        realizar_consulta_aleatoria("gacha_arma", 1, cursor)
    elif opcao == 4:
        realizar_consulta_aleatoria("gacha_arma", 10, cursor)
    elif opcao == 5:
        realizar_consulta_aleatoria("gacha_base", 1, cursor)
    elif opcao == 6:
        realizar_consulta_aleatoria("gacha_base", 10, cursor)
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")

   

# Conectar ao banco de dados MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hsr"
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
