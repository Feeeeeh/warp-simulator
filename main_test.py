import tkinter as tk
from ttkbootstrap import Style, Frame, Button, Notebook
from PIL import ImageTk, Image
from gif_loader import AnimatedGif
import random
import mysql.connector
import db_test

class WarpSimulator:
    def __init__(self, root):
        # cria a janela, seta um titulo e o tamanho dela
        self.root = root
        self.root.title("Warp Simulator")
        self.root.geometry("800x500")

        # Estiliação da janela no estilo darkly na biblioteca ttkbootstrap
        self.style = Style(theme='darkly')
        self.style.configure('custom.TNotebook', tabposition="wn", padding=[5, 5])
        self.style.configure('TNotebook.Tab', width=15)

        # Notebook para trocar entre abas
        self.notebook = Notebook(style='custom.TNotebook')
        self.notebook.pack(expand=True, fill='both')
        self.image_references = [] # lista com a referencia das imagens, é necessario pra imagem se manter no loop principal, se não ela é criada e jogada fora

        # Itens do gacha
        self.firefly_pulls = ["imagens/firefly_pull.png", "imagens/bailu_pull.png", "imagens/himeko_pull.png","imagens/welt_pull.png","imagens/yanqing_pull.png","imagens/clara_pull.png","imagens/bronya_pull.png",
                              "imagens/gepard_pull.png","imagens/qiqi_pull.png"]

        self.fila = [] #lista do que você tirou no gacha
        self.current_10x_index = 0  # index que irá aumentar de 1 em 1 para pegar os itens da lista um por vez

        # Conectar ao banco de dados MySQL
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hsr"
        )

        # Verificar se a conexão foi bem sucedida
        if self.conexao.is_connected():
            print('Conexão ao banco de dados MySQL estabelecida.')
            self.cursor = self.conexao.cursor()
        else:
            print('Erro ao conectar ao banco de dados MySQL.')

        self.create_tabs()

    def create_tabs(self): #cria as abas do notebook
        self.create_tab("Firefly", "imagens/firefly_banner.png", self.pull1x, self.pull10x)
        self.create_tab("Light Cone", "imagens/cone_banner.png", self.pull1x, self.pull10x)
        self.create_standard_tab("Standard", "imagens/Stellar_Warp.png", self.pull1x, self.pull10x)

    def create_tab(self, title, banner_image_path, pull1x_command, pull10x_command): # tab da firefly e light cone por enquanto
        tab = Frame(self.notebook, width=200, height=200)
        self.notebook.add(tab, text=title, padding=10)
        banner_image = ImageTk.PhotoImage(Image.open(banner_image_path))
        self.image_references.append(banner_image)
        tk.Label(tab, image=banner_image).pack()
        self.create_buttons(tab, pull1x_command, pull10x_command)

    def create_standard_tab(self, title, banner_image_path, pull1x_command, pull10x_command): # tab standard
        tab = Frame(self.notebook, width=200, height=200)
        self.notebook.add(tab, text=title, padding=10)
        warp = Image.open(banner_image_path)
        warp_resized = warp.resize((700, 387)) # resize da imagem do standard, ela era muito grande
        warp_image = ImageTk.PhotoImage(warp_resized)
        self.image_references.append(warp_image)
        tk.Label(tab, image=warp_image).pack()
        self.create_buttons(tab, pull1x_command, pull10x_command)

    def create_buttons(self, tab, pull1x_command, pull10x_command): #cria a base dos botões, recebe argumentos pra mudar o comando dos botões 
        frame = Frame(tab, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        button1 = Button(tab, bootstyle="dark", text="Warp 1x", command=pull1x_command)
        button10 = Button(tab, bootstyle="dark", text="Warp 10x", command=pull10x_command)
        button1.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)
        button10.pack(in_=frame, anchor='s', side='right', fill="both", expand=True)

    def pull1x(self): # 1 tentativa de gacha
        print("1 pull")
        resultado = random.choice(self.firefly_pulls)
        print(resultado)
        self.show_gif_and_result(resultado)
        db_test.escolher_operacao(1, self.cursor)  # Chama a operação de banco de dados correspondente

    def pull10x(self): # 10 tentativas de gacha
        print("10 pulls")
        self.fila = [random.choice(self.firefly_pulls) for _ in range(10)]
        print(self.fila)
        self.current_10x_index = 0  # reseta o index caso não seja a primeira vez que você está usando o comando
        self.show_gif_and_result(self.fila)
        db_test.escolher_operacao(2, self.cursor)  # Chama a operação de banco de dados correspondente

    def show_gif_and_result(self, resultado): # mostra o gif e em seguida chama a função de mostrar o resultado
        new_window = tk.Toplevel(self.root)
        gif_path = "qiqi" if "imagens/qiqi_pull.png" in resultado else "imagens/5_estrelas.gif" if "firefly1" or "firefly2" or "firefly3" or "firefly4" in resultado else "imagens/3_estrelas.gif"
  
        # chama uma classe que comprime e junta os frames do gif de forma com que ele apareça direito, sem pontos vazios
        gif = AnimatedGif(new_window, gif_path, loop=False, on_complete=lambda: self.show_result(new_window, resultado)) # não funciona sem lambda por algum motivo
        gif.pack()

    def show_result(self, window, result): # define qual imagem será mostrada na tela de resultado e envia para a função que cria a tela de resultado
        if isinstance(result, str):  # 1 pull, verifica se a variavel resultado é uma string
            result_image_path = result
            self.create_result_window(window, result_image_path)
        else:  # 10 pull, caso ela for uma lista e não uma string
            if self.current_10x_index < len(result): # enquanto aquele index lá de trás for menor que o tamanho da lista
                result_image_path = result[self.current_10x_index]
                self.create_result_window(window, result_image_path)
                self.current_10x_index += 1 # aumenta o index lá de trás
            else:
                self.close_all_windows() # caso o index seja igual ou maior que o tamanho da lista, fecha as abas

    def create_result_window(self, window, image_path): # cria a tela de resultado com a informação da função anterior
        result_window = tk.Toplevel(window)
        result_image = ImageTk.PhotoImage(Image.open(image_path)) # carrega a imagem do resultado
        
        # tentando limitar a imagem a um frame pra ela parar de mudar de tamanho, não funcionou 
        img_frame = Frame(result_window)
        img_frame.pack(fill="both",expand=True)
        
        label = tk.Label(img_frame, image=result_image) # joga a imagem na tela
        label.pack()
        self.image_references.append(result_image) # jogando a imagem pras referencias pra ela n sumir
        
        frame = Frame(result_window, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        
        next_button = Button(result_window, bootstyle="light", text="Next", command=lambda: self.proximo(result_window, label)) # botão que chama a função proximo
        next_button.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)

    def proximo(self, result_window, label): # troca para a proxima imagem
        if self.current_10x_index < len(self.fila): # checa se o index lá de trás é menor que o tamanho da lista
            result_image_path = self.fila[self.current_10x_index] # vai se referir ao item da lista baseado no index
            new_image = ImageTk.PhotoImage(Image.open(result_image_path))
            self.image_references.append(new_image)
            label.config(image=new_image) # reconfigura a imagem da label para a nova
            self.current_10x_index += 1
        else:
            self.close_all_windows()

    def close_all_windows(self):
        for window in self.root.winfo_children(): # winfo_children() se refere a todas as janelas criadas a partir de outra
            if isinstance(window, tk.Toplevel): # verifica se a variavel window é uma nova janela tk
                window.destroy() # mata as criança :) 

    def close(self):
        # Fecha o cursor e a conexão
        if self.conexao.is_connected():
            self.cursor.close()
            self.conexao.close()
            print('Conexão ao banco de dados MySQL encerrada.')
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WarpSimulator(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
    