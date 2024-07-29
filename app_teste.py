import tkinter as tk
from ttkbootstrap import Style, Frame, Button, Notebook
from PIL import ImageTk, Image
from gif_loader import AnimatedGif
import mysql.connector
import random, pygame, sys

class WarpSimulator:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id  # Store the user ID
        self.root.title("Warp Simulator")
        self.root.geometry("1100x500")  # Increase width to accommodate the new frame
        root.resizable(False, False)
        
        self.style = Style(theme='darkly')
        self.style.configure('custom.TNotebook', tabposition="wn", padding=[5, 5])
        self.style.configure('TNotebook.Tab', width=15)

        # Create a main frame to hold the notebook and the right frame
        main_frame = Frame(root)
        main_frame.pack(fill='both', expand=True)

        # Create a frame for the notebook
        notebook_frame = Frame(main_frame)
        notebook_frame.pack(side='left', fill='both', expand=True)

        self.notebook = Notebook(notebook_frame, style='custom.TNotebook')
        self.notebook.pack(expand=True, fill='both')
        
        self.image_references = []
        
        self.standard_possible_results = [
            "imagens/firefly_pull.png", "imagens/bailu_pull.png", "imagens/bronya_pull.png", 
            "imagens/clara_pull.png", "imagens/gepard_pull.png", "imagens/himeko_pull.png", 
            "imagens/welt_pull.png", "imagens/yanqing_pull.png"
        ]
        
        self.db_conn = self.connect_to_database()
        self.firefly_pulls = self.get_data_from_db("gacha_ff")
        self.cone_pulls = self.get_data_from_db("gacha_arma")
        self.standard_pulls = self.get_data_from_db("gacha_base")

        self.fila = []
        self.current_10x_index = 0

        self.create_tabs()

        # Create the right frame
        self.right_frame = Frame(main_frame, width=200)
        self.right_frame.pack(side='right', fill='y')
        self.right_frame.pack_propagate(False)
        self.create_right_frame_content()

        pygame.mixer.init()

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
        
    def create_right_frame_content(self):
        # Add content to the right frame, e.g., a label and a button
        label = tk.Label(self.right_frame, text="Right Frame", font=("Arial", 16))
        label.pack(pady=20)
        button = Button(self.right_frame, text="Example Button")
        button.pack(pady=20)

    def mapear_item(self, nome):
        if "firefly" in nome:
            return "Firefly"
        elif "arma" in nome:
            return "Cone"
        elif "base" in nome:
            return "Standard"
        elif "lixo" in nome:
            return "Lixo"
        else:
            return "Unknown"


    def save_result_to_db(self, results):
        # Ensure results is always a list for uniform processing
        if not isinstance(results, list):
            results = [results]
        
        for result in results:
            result_mapped = self.mapear_item(result)
            try:
                cursor = self.db_conn.cursor()
                cursor.execute('''
                    SELECT quantidade FROM save_char WHERE user_id = %s AND nome = %s
                ''', (self.user_id, result_mapped))
                row = cursor.fetchone()
    
                if row:
                    new_quantity = row[0] + 1
                    new_jade = 160 * new_quantity
                    cursor.execute('''
                        UPDATE save_char SET quantidade = %s, jade = %s
                        WHERE user_id = %s AND nome = %s
                    ''', (new_quantity, new_jade, self.user_id, result_mapped))
                else:
                    cursor.execute('''
                        INSERT INTO save_char (user_id, nome, quantidade, jade)
                        VALUES (%s, %s, %s, %s)
                    ''', (self.user_id, result_mapped, 1, 160))
                
                self.db_conn.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")


    def pull1x(self, x):
        print("1 pull")
        resultado = random.choice(x)
        if resultado in ['base1', 'base2', 'base3', 'base4']:
            resultado = random.choice(self.standard_possible_results)
        elif resultado in ["firefly1", "firefly2", "firefly3", "firefly4"]:
            resultado = "imagens/firefly_pull.png"
        elif resultado in ['arma1', 'arma2', 'arma3', 'arma4']:
            resultado = "imagens/firefly_cone.png"
        else:
            resultado = "imagens/lixo_lc.png"
        print(resultado)
        self.save_result_to_db(resultado)  # Save result to database
        self.show_gif_and_result(resultado)

    def pull10x(self, x):
        print("10 pulls")
        self.fila = [random.choice(x) for _ in range(10)]
        self.fila = [random.choice(self.standard_possible_results) if item in ['base1', 'base2', 'base3', 'base4']
                     else "imagens/firefly_cone.png" if item in ['arma1', 'arma2', 'arma3', 'arma4']
                     else "imagens/firefly_pull.png" if item in ["firefly1","firefly2","firefly3","firefly4"]
                     else "imagens/lixo_lc.png" for item in self.fila]
        print(self.fila)
        self.save_result_to_db(self.fila)  # Save results to database
        self.current_10x_index = 0
        self.show_gif_and_result(self.fila)


    def show_gif_and_result(self, resultado):
        new_window = tk.Toplevel(self.root)
        new_window.resizable(False, False)
        gif_path = "imagens/qiqi.gif" if "qiqi" in resultado else "imagens/5_estrelas.gif" if "imagens/firefly_pull.png" in resultado else "imagens/3_estrelas.gif"
  
        gif = AnimatedGif(new_window, gif_path, loop=False, on_complete=lambda: self.show_result(new_window, resultado))
        gif.pack()

        # Play the pull song
        self.play_audio("imagens/pull_songv3.mp3")

    def show_result(self, window, result):
        if isinstance(result, str):
            result_image_path = result  # Directly use the result if it's an image path
            self.create_result_window(window, result_image_path)
        else:
            if self.current_10x_index < len(result):
                result_image_path = result[self.current_10x_index]
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

        # Play the result song
        self.play_audio("imagens/result_song.mp3")

    def proximo(self, result_window, label):
        if self.current_10x_index < len(self.fila):
            result_image_path = self.fila[self.current_10x_index]
            new_image = ImageTk.PhotoImage(Image.open(result_image_path))
            self.image_references.append(new_image)
            label.config(image=new_image)
            self.current_10x_index += 1

            # Play the result song
            self.play_audio("imagens/result_song.mp3")
        else:
            self.close_all_windows()

    def close_all_windows(self):
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel):
                window.destroy()

    def play_audio(self, audio_path):
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main_test.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    root = tk.Tk()
    app = WarpSimulator(root, user_id)
    root.mainloop()
