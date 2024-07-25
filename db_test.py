import mysql.connector

def login():
    # Solicita o nome de usuário e a senha
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")

    # Conecta ao banco de dados
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="HSR"
    )
    cursor = conn.cursor()

    # Verifica se o usuário e a senha estão corretos
    cursor.execute('SELECT id FROM login WHERE nome = %s AND senha = %s', (username, password))
    user = cursor.fetchone()

    # Fecha a conexão com o banco de dados
    conn.close()

    if user:
        print("Login bem-sucedido!")
        return user[0]  # Retorna o ID do usuário
    else:
        print("Nome de usuário ou senha incorretos. Tente novamente.")
        return None

def mapear_item(nome):
    if nome in ['firefly1', 'firefly2', 'firefly3', 'firefly4']:
        return 'firefly'
    elif nome in ['arma1', 'arma2', 'arma3', 'arma4']:
        return 'arma'
    elif nome in ['base1', 'base2', 'base3', 'base4']:
        return 'base'
    elif nome in ['lixo1', 'lixo2', 'lixo3', 'lixo4', 'lixo5', 'lixo6', 'lixo7', 'lixo8', 'lixo9', 'lixo10', 'lixo11']:
        return 'lixo'
    else:
        return nome

def realizar_consulta_aleatoria(tabela, quantidade, cursor):
    try:
        # Constrói a consulta SQL com base na tabela e na quantidade especificada
        query = f"SELECT nome FROM {tabela} ORDER BY RAND() LIMIT {quantidade}"

        # Executa a consulta
        cursor.execute(query)

        # Obtém todos os resultados da consulta
        resultados = cursor.fetchall()

        # Mapeia os nomes dos itens para as categorias desejadas
        resultados_mapeados = [(mapear_item(resultado[0]),) for resultado in resultados]

        # Retorna os resultados mapeados
        return resultados_mapeados

    except mysql.connector.Error as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        return []

def salvar_resultados(usuario_id, resultados, cursor, conexao):
    try:
        for resultado in resultados:
            nome = resultado[0]

            # Verifica se o item já existe na tabela save_char para o usuário
            cursor.execute('''
                SELECT quantidade FROM save_char WHERE user_id = %s AND nome = %s
            ''', (usuario_id, nome))
            item = cursor.fetchone()

            if item:
                # Atualiza a quantidade existente
                nova_quantidade = item[0] + 1
                cursor.execute('''
                    UPDATE save_char
                    SET quantidade = %s
                    WHERE user_id = %s AND nome = %s
                ''', (nova_quantidade, usuario_id, nome))
            else:
                # Insere um novo item
                cursor.execute('''
                    INSERT INTO save_char (user_id, nome, quantidade, jade)
                    VALUES (%s, %s, %s, %s)
                ''', (usuario_id, nome, 1, 10))  # Ajuste conforme necessário
        conexao.commit()

        # Exibe os resultados no terminal
        print("Resultados salvos:")
        for resultado in resultados:
            print(resultado[0])

    except mysql.connector.Error as e:
        print(f"Erro ao salvar os resultados: {e}")

def escolher_operacao(conexao, cursor, usuario_id):
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
                resultados = realizar_consulta_aleatoria("gacha_ff", 1, cursor)
                salvar_resultados(usuario_id, resultados, cursor, conexao)
            elif escolha == 2:
                resultados = realizar_consulta_aleatoria("gacha_ff", 10, cursor)
                salvar_resultados(usuario_id, resultados, cursor, conexao)
            elif escolha == 3:
                resultados = realizar_consulta_aleatoria("gacha_arma", 1, cursor)
                salvar_resultados(usuario_id, resultados, cursor, conexao)
            elif escolha == 4:
                resultados = realizar_consulta_aleatoria("gacha_arma", 10, cursor)
                salvar_resultados(usuario_id, resultados, cursor, conexao)
            elif escolha == 5:
                resultados = realizar_consulta_aleatoria("gacha_base", 1, cursor)
                salvar_resultados(usuario_id, resultados, cursor, conexao)
            elif escolha == 6:
                resultados = realizar_consulta_aleatoria("gacha_base", 10, cursor)
                salvar_resultados(usuario_id, resultados, cursor, conexao)
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

    # Chama a função de login
    usuario_id = login()

    if usuario_id:
        # Chama a função para escolher a operação
        escolher_operacao(conexao, cursor, usuario_id)

    # Fecha o cursor e a conexão
    cursor.close()
    conexao.close()
