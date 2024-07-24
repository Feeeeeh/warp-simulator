import tkinter as tk
from ttkbootstrap import Style, Frame, Button, Notebook
from PIL import ImageTk, Image
from gif_loader import AnimatedGif
import mysql.connector
import random

class WarpSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Warp Simulator")
        self.root.geometry("800x500")
        root.resizable(False, False)
        
        self.style = Style(theme='darkly')
        self.style.configure('custom.TNotebook', tabposition="wn", padding=[5, 5])
        self.style.configure('TNotebook.Tab', width=15)

        self.notebook = Notebook(style='custom.TNotebook')
        self.notebook.pack(expand=True, fill='both')
        
        self.image_references = []

        self.db_conn = self.connect_to_database()
        self.firefly_pulls = self.get_data_from_db("gacha_ff")
        self.cone_pulls = self.get_data_from_db("gacha_arma")
        self.standard_pulls = self.get_data_from_db("gacha_base")

        self.image_mappings = self.create_image_mappings()

        self.fila = []
        self.current_10x_index = 0

        self.create_tabs()

    def connect_to_database(self):
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

    def get_data_from_db(self, table_name):
        try:
            cursor = self.db_conn.cursor()
            cursor.execute(f"SELECT nome FROM {table_name}")
            results = cursor.fetchall()
            return [row[0] for row in results]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

    def create_image_mappings(self):
        return {
            'qiqi' : 'imagens/qiqi_pull.png',
            'firefly1': 'imagens/firefly_pull.png',
            'firefly2': 'imagens/firefly_pull.png',
            'firefly3': 'imagens/firefly_pull.png',
            'firefly4': 'imagens/firefly_pull.png',
            'arma1': 'imagens/firefly_cone.png',
            'arma2': 'imagens/firefly_cone.png',
            'arma3': 'imagens/firefly_cone.png',
            'arma4': 'imagens/firefly_cone.png',
            'base1': 'imagens/welt_pull.png',
            'base2': 'imagens/welt_pull.png',
            'base3': 'imagens/welt_pull.png',
            'base4': 'imagens/welt_pull.png'
        }

    def create_tabs(self):
        self.create_tab("Firefly", "imagens/firefly_banner.png", lambda: self.pull1x(self.firefly_pulls), lambda: self.pull10x(self.firefly_pulls))
        self.create_tab("Light Cone", "imagens/cone_banner.png", lambda: self.pull1x(self.cone_pulls), lambda: self.pull10x(self.cone_pulls))
        self.create_standard_tab("Standard", "imagens/Stellar_Warp.png", lambda: self.pull1x(self.standard_pulls), lambda: self.pull10x(self.standard_pulls))

    def create_tab(self, title, banner_image_path, pull1x_command, pull10x_command):
        tab = Frame(self.notebook, width=200, height=200)
        img = ImageTk.PhotoImage(Image.open("imagens/firefly_icon.jpg"))
        self.image_references.append(img)
        self.notebook.add(tab, text=title, padding=10, image=img, compound="center")
        banner_image = ImageTk.PhotoImage(Image.open(banner_image_path))
        self.image_references.append(banner_image)
        tk.Label(tab, image=banner_image).pack()
        self.create_buttons(tab, pull1x_command, pull10x_command)

    def create_standard_tab(self, title, banner_image_path, pull1x_command, pull10x_command):
        tab = Frame(self.notebook, width=200, height=200)
        self.notebook.add(tab, text=title, padding=10)
        warp = Image.open(banner_image_path)
        warp_resized = warp.resize((700, 387))
        warp_image = ImageTk.PhotoImage(warp_resized)
        self.image_references.append(warp_image)
        tk.Label(tab, image=warp_image).pack()
        self.create_buttons(tab, pull1x_command, pull10x_command)

    def create_buttons(self, tab, pull1x_command, pull10x_command):
        frame = Frame(tab, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        button1 = Button(tab, bootstyle="dark", text="Warp 1x", command=pull1x_command)
        button10 = Button(tab, bootstyle="dark", text="Warp 10x", command=pull10x_command)
        button1.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)
        button10.pack(in_=frame, anchor='s', side='right', fill="both", expand=True)

    def pull1x(self, x):
        print("1 pull")
        resultado = random.choice(x)
        print(resultado)
        self.show_gif_and_result(resultado)

    def pull10x(self, x):
        print("10 pulls")
        self.fila = [random.choice(x) for _ in range(10)]
        print(self.fila)
        self.current_10x_index = 0
        self.show_gif_and_result(self.fila)

    def show_gif_and_result(self, resultado):
        new_window = tk.Toplevel(self.root)
        new_window.resizable(False, False)
        gif_path = "imagens/qiqi.gif" if "qiqi" in resultado else "imagens/5_estrelas.gif" if "firefly" in resultado else "imagens/3_estrelas.gif"
  
        gif = AnimatedGif(new_window, gif_path, loop=False, on_complete=lambda: self.show_result(new_window, resultado))
        gif.pack()

    def show_result(self, window, result):
        if isinstance(result, str):
            result_image_path = self.image_mappings.get(result, "imagens/placeholder_image.png")
            self.create_result_window(window, result_image_path)
        else:
            if self.current_10x_index < len(result):
                result_image_path = self.image_mappings.get(result[self.current_10x_index], "imagens/placeholder_image.png")
                self.create_result_window(window, result_image_path)
                self.current_10x_index += 1
            else:
                self.close_all_windows()

    def create_result_window(self, window, image_path):
        result_window = tk.Toplevel(window)
        result_image = ImageTk.PhotoImage(Image.open(image_path))
        
        img_frame = Frame(result_window, width=600, height=300)
        img_frame.pack(fill="both", expand=True)
        img_frame.propagate(False)
        
        label = tk.Label(img_frame, image=result_image)
        label.pack()
        self.image_references.append(result_image)
        
        frame = Frame(result_window, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        
        next_button = Button(result_window, bootstyle="light", text="Next", command=lambda: self.proximo(result_window, label))
        next_button.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)

    def proximo(self, result_window, label):
        if self.current_10x_index < len(self.fila):
            result_image_path = self.image_mappings.get(self.fila[self.current_10x_index], "imagens/placeholder_image.png")
            new_image = ImageTk.PhotoImage(Image.open(result_image_path))
            self.image_references.append(new_image)
            label.config(image=new_image)
            self.current_10x_index += 1
        else:
            self.close_all_windows()

    def close_all_windows(self):
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy()

def main():
    root = tk.Tk()
    app = WarpSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
