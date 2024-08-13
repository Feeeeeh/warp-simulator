import tkinter as tk
from ttkbootstrap import Style, Frame, Button, Notebook, LabelFrame, Label
from PIL import ImageTk, Image
from gif_loader import AnimatedGif
import mysql.connector
import random, pygame, sys


class WarpSimulator:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        self.root.title("Warp Simulator")
        self.root.geometry("1100x500")
        root.resizable(False, False)
        
        self.style = Style(theme='darkly')
        self.style.configure('custom.TNotebook', tabposition="wn", padding=[5, 5])
        self.style.configure('TNotebook.Tab', width=15)

        # um frame principal, que vai ter dois frames dentro
        main_frame = Frame(root)
        main_frame.pack(fill='both', expand=True)

        # um frame pra colocar o notebook
        notebook_frame = Frame(main_frame)
        notebook_frame.pack(side='left', fill='both', expand=True)

        # o notebook
        self.notebook = Notebook(notebook_frame, style='custom.TNotebook')
        self.notebook.pack(expand=True, fill='both')
        
        self.image_references = [] # o tkinter precisa de todas as imagens que ele vai usar
                                   # em uma lista para que elas se mantenham na tela
        
        
        # um random.choice irá pegar um item aleatório dessa lista caso você tenha tirado um personagem 5 estrelas padrão
        self.standard_possible_results = [
            "imagens/bronya_pull.png", "imagens/clara_pull.png", "imagens/gepard_pull.png", 
            "imagens/himeko_pull.png", "imagens/welt_pull.png", "imagens/yanqing_pull.png", "imagens/bailu_pull.png"
        ]
        
        # um dicionario pra conseguir tirar do mesmo lugar o caminho da imagem, e o que ela representa
        self.mapping = {
            "imagens/bronya_pull.png": "Bronya",
            "imagens/clara_pull.png": "Clara",
            "imagens/gepard_pull.png": "Gepard",
            "imagens/himeko_pull.png": "Himeko",
            "imagens/welt_pull.png": "Welt",
            "imagens/yanqing_pull.png": "Yanqing",
            "imagens/bailu_pull.png": "Bailu",
            "imagens/firefly_pull.png": "Firefly",
            "imagens/firefly_cone.png": "Cone",
            "imagens/qiqi_pull.png": "Qiqi",
            "imagens/lixo_lc.png": "Lixo"
        }

        
        # get_data_from_db é uma função que vai dar um fetchall filtrado pelo nome do database, que é mandado como parâmetro
        self.db_conn = self.connect_to_database()
        self.firefly_pulls = self.get_data_from_db("gacha_ff")
        self.cone_pulls = self.get_data_from_db("gacha_arma")
        self.standard_pulls = self.get_data_from_db("gacha_base")

        self.fila = [] # fila dos itens que você pegou, é necessario para pegar item por item na tela que mostra os resultados
        self.current_10x_index = 0 # usado pra pegar a posição dos itens na fila

        self.create_tabs() # cria as três abas do notebook
 
        # cria o frame da direita que mostra suas informações e inventário
        self.right_frame = Frame(main_frame, width=200)
        self.right_frame.pack(side='right', fill='y')
        self.right_frame.pack_propagate(False)

        # pega e mostra o nome do usuario que está logado
        cursor = self.db_conn.cursor()
        query = "SELECT nome FROM login WHERE id = %s"
        cursor.execute(query, (self.user_id,))
        result = cursor.fetchone()
        if result:
            name = result[0]
            texto = f"User Name: {name}"
        else:
            texto = "No user found with the given ID."
        label = tk.Label(self.right_frame, text=texto)
        label.pack(pady=20)

        # atualiza o frame da direita com as informações do usuario
        self.update_right_frame()

        pygame.mixer.init() # inicia o mixer de som do pygame, usado mais tarde no codigo

    def update_right_frame(self):
        inventory = self.get_user_inventory()
    
        # ordem do display dos itens no seu inventário
        self.item_order = ["Firefly", "Cone", "Himeko", "Bronya", "Clara", "Gepard", "Welt", "Yanqing", "Bailu", "Qiqi", "Lixo"]
        ordered_inventory = sorted(inventory, key=lambda item: self.item_order.index(item[0]) if item[0] in self.item_order else len(self.item_order))
    
        # pega o valor total de jade, somando todos os valores dos itens pra mostrar seu gasto total
        total_jade = sum(item[2] for item in ordered_inventory)
        total_jade_label = Label(self.right_frame, text=f"Jades Gastas: {total_jade}", bootstyle="warning, inverse", font=("Arial", 12, "bold"))
        total_jade_label.pack(pady=(5, 15), fill='x')
    
        # limpa o frame pra atualizar sem erros
        for widget in self.right_frame.winfo_children():
            widget.destroy()
    
    
        # nome do usuario no topo
        cursor = self.db_conn.cursor()
        query = "SELECT nome FROM login WHERE id = %s"
        cursor.execute(query, (self.user_id,))
        result = cursor.fetchone()
        if result:
            name = result[0]
            username_text = f"{name}"
        else:
            username_text = "No user found with the given ID."
    
        username_label = Label(self.right_frame, text=username_text, bootstyle="info, inverse", font=("Arial", 14, "bold"))
        username_label.pack(pady=(10, 5), fill='x')
    
    
        # mostra os itens do seu inventário em uma grid organizada
        if ordered_inventory:  # só mostra o inventário se ele existe (pra caso de contas novas que ainda não tem itens)
            inventory_frame = Frame(self.right_frame)
            inventory_frame.pack(fill="both", expand=True, padx=10)
    
            row, col = 0, 0
            for item in ordered_inventory:
                item_frame = LabelFrame(inventory_frame, text=item[0], bootstyle="primary", padding=5, width=90, height=50)
                item_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
                item_label = Label(item_frame, text=f"Qty: {item[1]}", justify='center')
                item_label.pack(anchor='center')
    
                col += 1
                if col > 1:  # começa a colocar os itens na proxima linha depois de 2 itens, pra melhor display
                    col = 0
                    row += 1


    def connect_to_database(self): # conexão basica com o database
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="HSR"
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def get_data_from_db(self, table_name): # pegar data do database
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(f"SELECT nome FROM {table_name}")
            results = cursor.fetchall()
            return [row[0] for row in results]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    # cria as abas mandando todos os parametros necessarios
    def create_tabs(self):
        self.create_tab("imagens/firefly_banner.png", "imagens/firefly_icon.png", lambda: self.pull1x(self.firefly_pulls), lambda: self.pull10x(self.firefly_pulls))
        self.create_tab("imagens/cone_banner.png", "imagens/cone_icon.png", lambda: self.pull1x(self.cone_pulls), lambda: self.pull10x(self.cone_pulls))
        self.create_standard_tab("imagens/Stellar_Warp.png", lambda: self.pull1x(self.standard_pulls), lambda: self.pull10x(self.standard_pulls))

    # criador basico de aba
    def create_tab(self, banner_image_path, icon_path, pull1x_command, pull10x_command):
        tab = Frame(self.notebook, width=200, height=200)
        img = ImageTk.PhotoImage(Image.open(icon_path))
        self.image_references.append(img)
        self.notebook.add(tab, padding=10, image=img, compound="center")
        banner_image = ImageTk.PhotoImage(Image.open(banner_image_path))
        self.image_references.append(banner_image)
        tk.Label(tab, image=banner_image).pack()
        self.create_buttons(tab, pull1x_command, pull10x_command)

    # memsa coisa mas fiz essa separado pelo resize da imagem, tinha varias formas mais otimizadas de fazer
    def create_standard_tab(self, banner_image_path, pull1x_command, pull10x_command):
        tab = Frame(self.notebook, width=200, height=200)
        img = ImageTk.PhotoImage(Image.open("imagens/base_icon.png"))
        self.image_references.append(img)
        self.notebook.add(tab, padding=10, image=img, compound="center")
        warp = Image.open(banner_image_path)
        warp_resized = warp.resize((700, 387))
        warp_image = ImageTk.PhotoImage(warp_resized)
        self.image_references.append(warp_image)
        tk.Label(tab, image=warp_image).pack()
        self.create_buttons(tab, pull1x_command, pull10x_command)

    # cria 2 botões, esperando um parametro de comando
    # fiz assim pois as 3 abas usam comandos diferentes pros botões
    def create_buttons(self, tab, pull1x_command, pull10x_command):
        frame = Frame(tab, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        button1 = Button(tab, bootstyle="dark", text="Warp 1x", command=pull1x_command)
        button10 = Button(tab, bootstyle="dark", text="Warp 10x", command=pull10x_command)
        button1.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)
        button10.pack(in_=frame, anchor='s', side='right', fill="both", expand=True)
        

    def mapear_item(self, nome):
        return self.mapping.get(nome, "Unknown") # unknown nesse caso é um valor default, caso não consiga achar o valor ele vai ser unknown


    # salvar o que o usuario conseguiu nos seus respectivos dados na database
    def save_result_to_db(self, results):
        # garante que os resultados estão sempre em lista, só pra evitar possiveis erros
        if not isinstance(results, list):
            results = [results]

        for result in results:
            result_mapped = self.mapear_item(result) # mapeia o valor, já que ele recebe o caminho do arquivo e não o que ele representa
            try:
                cursor = self.db_conn.cursor()
                cursor.execute('''
                    SELECT quantidade FROM save_char WHERE user_id = %s AND nome = %s
                ''', (self.user_id, result_mapped))
                row = cursor.fetchone()

                if row: # caso já tenha algo naquela linha ele da update nela
                    new_quantity = row[0] + 1
                    new_jade = 160 * new_quantity # multiplica a quantidade do item por 160, visto que cada item vale 160 jades
                    cursor.execute('''
                        UPDATE save_char SET quantidade = %s, jade = %s
                        WHERE user_id = %s AND nome = %s
                    ''', (new_quantity, new_jade, self.user_id, result_mapped))
                    
                else: # se não tiver, só adiciona
                    cursor.execute('''
                        INSERT INTO save_char (user_id, nome, quantidade, jade)
                        VALUES (%s, %s, %s, %s)
                    ''', (self.user_id, result_mapped, 1, 160))

                self.db_conn.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")

        self.update_right_frame()
        # e atualiza seu inventario



    def pull1x(self, gacha): # 1 tentativa no gacha
        print("1 pull")
        
        
        # "gacha" é a lista que foi mandada quando o botão foi criado
        # aquela que foi pega do database com a função get_data_from_db
        resultado = random.choice(gacha) 
        if resultado in ['base1', 'base2', 'base3', 'base4']:
            resultado = random.choice(self.standard_possible_results)
        elif resultado in ["firefly1", "firefly2", "firefly3", "firefly4"]:
            resultado = "imagens/firefly_pull.png"
        elif resultado in ['arma1', 'arma2', 'arma3', 'arma4']:
            resultado = "imagens/firefly_cone.png"
        elif resultado == "qiqi":
            resultado = "imagens/qiqi_pull.png"
        else:
            resultado = "imagens/lixo_lc.png"
            
        print(resultado)
        self.save_result_to_db(resultado)  # manda o que o usuario tirou no gacha pra database
        self.gacha_gif(resultado)

    def pull10x(self, x): # 10 tentativas no gacha
        print("10 pulls")
        self.fila = [random.choice(x) for _ in range(10)] # mesma logica do 1x mas repete 10 vezes, jogando em uma lista
        self.fila = [random.choice(self.standard_possible_results) if item in ['base1', 'base2', 'base3', 'base4']
                     else "imagens/firefly_cone.png" if item in ['arma1', 'arma2', 'arma3', 'arma4']
                     else "imagens/firefly_pull.png" if item in ["firefly1","firefly2","firefly3","firefly4"]
                     else "imagens/qiqi_pull.png" if item == "qiqi"
                     else "imagens/lixo_lc.png" for item in self.fila]
        print(self.fila)
        self.save_result_to_db(self.fila)  # manda o que o usuario tirou no gacha pra database
        self.current_10x_index = 0 # index que vai ser usado pra passar de item por item
        self.gacha_gif(self.fila) # proxima função

    # cria uma nova janela mostrando a animação do gacha
    def gacha_gif(self, resultado):
        new_window = tk.Toplevel(self.root) # toplevel cria uma nova janela como filha da que você usou como parametro
        new_window.resizable(False, False) # evita que a janela seja redimensionada pelo usuario
        
        if "imagens/qiqi_pull.png" in resultado:
            gif_path = "imagens/qiqi.gif" # mostra o gif especial da qiqi
            
        elif "imagens/firefly_pull.png" in resultado or "imagens/firefly_cone.png" in resultado or any(item in resultado for item in self.standard_possible_results):
            gif_path = "imagens/5_estrelas.gif" # mostra o gif especial de 5 estrelas
            
        else:
            gif_path = "imagens/3_estrelas.gif" # gif de quando você não tira 5 estrelas algum
            
        gif = AnimatedGif(new_window, gif_path, loop=False, on_complete=lambda: self.show_result(new_window, resultado))
        gif.pack()
        # obrigado usuario Flutterguy135 do stackoverflow pelo gif loader que funciona perfeitamente :)

        # toca o audio do gacha
        self.play_audio("imagens/pull_songv3.mp3")

    def show_result(self, window, result):
        if isinstance(result, str):
            result_image_path = result  # pro caso de ter usado o 1x, que retorna uma string e não uma lista
            self.create_result_window(window, result_image_path)
        else:
            if self.current_10x_index < len(result): # checa se o index é menor que o tamano da lista
                result_image_path = result[self.current_10x_index] # usa o valor do index pra pegar a posição do item na lista
                self.create_result_window(window, result_image_path)
                self.current_10x_index += 1 # aumenta 1 no index
            else:
                self.close_all_windows() # caso ele for igual ou maior, mata todas as janelas

    def create_result_window(self, window, image_path): # a janela que mostra o que você pegou, após o gif do gacha
        result_window = tk.Toplevel(window)
        result_image = ImageTk.PhotoImage(Image.open(image_path)) # image_path é aquele item unico que foi tirado da lista usando o valor do index 
        
        img_frame = Frame(result_window, width=600, height=300) # frame pra imagem
        img_frame.pack(fill="both", expand=True)
        img_frame.propagate(False) # evita que o frame e a janela aumentem de tamanho caso a imagem seja maior que o frame 
        
        label = tk.Label(img_frame, image=result_image) # coloca a imagem no frame
        label.pack()
        self.image_references.append(result_image) # joga a imagem praquela lista que faz com que a imagem se mantenha na tela
        
        # frame e botão pra passar pra proxima imagem
        frame = Frame(result_window, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        next_button = Button(result_window, bootstyle="light", text="Next", command=lambda: self.proximo(label)) # proxima função
        next_button.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)

        # audio de resultado por ter pego um item
        self.play_audio("imagens/result_song.mp3") 

    def proximo(self, label):
        if self.current_10x_index < len(self.fila): # mesma logica do index e do tamanho da fila ja mostrados
            result_image_path = self.fila[self.current_10x_index]
            new_image = ImageTk.PhotoImage(Image.open(result_image_path))
            self.image_references.append(new_image)
            label.config(image=new_image)
            self.current_10x_index += 1

            # o audio toca todo novo item pra ter um feedback auditivo no caso de itens repetidos
            self.play_audio("imagens/result_song.mp3") 
        else:
            self.close_all_windows() 

    def close_all_windows(self):
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy() # mata todas as janelas filhas de outra

    def play_audio(self, audio_path): # toca um audio, o caminho é dado como parametro
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
    def get_user_inventory(self): # pega o inventario do usuario da database pra mostrar no aplicativo
        try:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                SELECT nome, quantidade, jade FROM save_char WHERE user_id = %s
            ''', (self.user_id,))
            rows = cursor.fetchall()
            return rows
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []


# faz com que o aplicativo só rode caso ele tenha recebido dois parametros
# nesse caso, o nome do script e o id do usuario que vem do gacha_login
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main_test.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    root = tk.Tk()
    app = WarpSimulator(root, user_id)
    root.mainloop()
    
# sys.argv é a lista dos argumentos que você usa pra rodar um arquivo python
# exemplo: python manage.py runserver
# sys.argv[0] seria manage.py
# no caso desse programa, sys.argv[1] é o id do usuario que foi passado quando
# o aplicativo foi iniciado como um subprocesso do gacha_login