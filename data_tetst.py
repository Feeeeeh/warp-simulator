# data_tetst.py
import mysql.connector
import sys
from login import validate_user

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

def salvar_resultados(usuario_id, resultados, cursor, conexao):
    try:
        for resultado in resultados:
            nome = resultado[0]
            cursor.execute('''
                SELECT quantidade FROM save_char WHERE user_id = %s AND nome = %s
            ''', (usuario_id, nome))
            item = cursor.fetchone()

            if item:
                nova_quantidade = item[0] + 1
                cursor.execute('''
                    UPDATE save_char
                    SET quantidade = %s
                    WHERE user_id = %s AND nome = %s
                ''', (nova_quantidade, usuario_id, nome))
            else:
                cursor.execute('''
                    INSERT INTO save_char (user_id, nome, quantidade, jade)
                    VALUES (%s, %s, %s, %s)
                ''', (usuario_id, nome, 1, 0))
        conexao.commit()
    except mysql.connector.Error as e:
        print(f"Erro ao salvar os resultados: {e}")

def realizar_consulta_aleatoria(tabela, quantidade, cursor):
    try:
        query = f"SELECT nome FROM {tabela} ORDER BY RAND() LIMIT {quantidade}"
        cursor.execute(query)
        resultados = cursor.fetchall()
        resultados_mapeados = [(mapear_item(resultado[0]),) for resultado in resultados]
        return resultados_mapeados
    except mysql.connector.Error as e:
        print(f"Erro ao executar a consulta SQL: {e}")
        return []

def escolher_operacao(choice, user_id, conn):
    try:
        cursor = conn.cursor()
        if choice == 1:
            resultados = realizar_consulta_aleatoria("gacha_ff", 1, cursor)
        elif choice == 2:
            resultados = realizar_consulta_aleatoria("gacha_ff", 10, cursor)
        elif choice == 3:
            resultados = realizar_consulta_aleatoria("gacha_arma", 1, cursor)
        elif choice == 4:
            resultados = realizar_consulta_aleatoria("gacha_arma", 10, cursor)
        elif choice == 5:
            resultados = realizar_consulta_aleatoria("gacha_base", 1, cursor)
        elif choice == 6:
            resultados = realizar_consulta_aleatoria("gacha_base", 10, cursor)

        salvar_resultados(user_id, resultados, cursor, conn)
        cursor.close()
    except mysql.connector.Error as e:
        print(f"Erro ao realizar a operação: {e}")

'''if __name__ == "__main__":
    usuario_id = int(sys.argv[1])
    
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="HSR"
    )

    if conexao.is_connected():
        print('Conexão ao banco de dados MySQL estabelecida.')
        cursor = conexao.cursor()
        escolher_operacao(conexao, cursor, usuario_id)
        cursor.close()
        conexao.close()'''
