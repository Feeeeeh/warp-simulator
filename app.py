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
            "imagens/bronya_pull.png", "imagens/clara_pull.png", "imagens/gepard_pull.png", 
            "imagens/himeko_pull.png", "imagens/welt_pull.png", "imagens/yanqing_pull.png", "imagens/bailu_pull.png"
        ]
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

        self.item_order = ["Firefly", "Himeko", "Bronya", "Clara", "Gepard", "Welt", "Yanqing", "Bailu", "Cone", "Qiqi", "Lixo"]
        
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

        # Fetch and display user name
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

        # Display the user name and inventory
        self.update_right_frame()


        pygame.mixer.init()


    def update_right_frame(self):
        inventory = self.get_user_inventory()
    
        # Order the inventory based on the desired display order
        self.item_order = ["Firefly", "Cone", "Himeko", "Bronya", "Clara", "Gepard", "Welt", "Yanqing", "Bailu", "Qiqi", "Lixo"]
        ordered_inventory = sorted(inventory, key=lambda item: self.item_order.index(item[0]) if item[0] in self.item_order else len(self.item_order))
    
        total_jade = sum(item[2] for item in ordered_inventory)
    
        # Clear the right frame before updating
        for widget in self.right_frame.winfo_children():
            widget.destroy()
    
        # Highlighted username at the top
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
    
        # Highlighted total jade below the username
        total_jade_label = Label(self.right_frame, text=f"Jades Gastas: {total_jade}", bootstyle="warning, inverse", font=("Arial", 12, "bold"))
        total_jade_label.pack(pady=(5, 15), fill='x')
    
        # Display inventory items in a grid
        if ordered_inventory:  # Only display inventory if it exists
            inventory_frame = Frame(self.right_frame)
            inventory_frame.pack(fill="both", expand=True, padx=10)
    
            row, col = 0, 0
            for item in ordered_inventory:
                item_frame = LabelFrame(inventory_frame, text=item[0], bootstyle="primary", padding=5, width=90, height=50)
                item_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
                item_label = Label(item_frame, text=f"Qty: {item[1]}", justify='center')
                item_label.pack(anchor='center')
    
                col += 1
                if col > 1:  # Move to the next row after 2 items
                    col = 0
                    row += 1


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
        self.create_tab("imagens/firefly_banner.png", "imagens/firefly_icon.png", lambda: self.pull1x(self.firefly_pulls), lambda: self.pull10x(self.firefly_pulls))
        self.create_tab("imagens/cone_banner.png", "imagens/cone_icon.png", lambda: self.pull1x(self.cone_pulls), lambda: self.pull10x(self.cone_pulls))
        self.create_standard_tab("imagens/Stellar_Warp.png", lambda: self.pull1x(self.standard_pulls), lambda: self.pull10x(self.standard_pulls))

    def create_tab(self, banner_image_path, icon_path, pull1x_command, pull10x_command):
        tab = Frame(self.notebook, width=200, height=200)
        img = ImageTk.PhotoImage(Image.open(icon_path))
        self.image_references.append(img)
        self.notebook.add(tab, padding=10, image=img, compound="center")
        banner_image = ImageTk.PhotoImage(Image.open(banner_image_path))
        self.image_references.append(banner_image)
        tk.Label(tab, image=banner_image).pack()
        self.create_buttons(tab, pull1x_command, pull10x_command)

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

    def create_buttons(self, tab, pull1x_command, pull10x_command):
        frame = Frame(tab, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        button1 = Button(tab, bootstyle="dark", text="Warp 1x", command=pull1x_command)
        button10 = Button(tab, bootstyle="dark", text="Warp 10x", command=pull10x_command)
        button1.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)
        button10.pack(in_=frame, anchor='s', side='right', fill="both", expand=True)
        

    def mapear_item(self, nome):
        return self.mapping.get(nome, "Unknown")


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

        self.update_right_frame()



    def pull1x(self, x):
        print("1 pull")
        resultado = random.choice(x)
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
        self.save_result_to_db(resultado)  # Save result to database
        self.show_gif_and_result(resultado)

    def pull10x(self, x):
        print("10 pulls")
        self.fila = [random.choice(x) for _ in range(10)]
        self.fila = [random.choice(self.standard_possible_results) if item in ['base1', 'base2', 'base3', 'base4']
                     else "imagens/firefly_cone.png" if item in ['arma1', 'arma2', 'arma3', 'arma4']
                     else "imagens/firefly_pull.png" if item in ["firefly1","firefly2","firefly3","firefly4"]
                     else "imagens/qiqi_pull.png" if item == "qiqi"
                     else "imagens/lixo_lc.png" for item in self.fila]
        print(self.fila)
        self.save_result_to_db(self.fila)  # Save results to database
        self.current_10x_index = 0
        self.show_gif_and_result(self.fila)


    def show_gif_and_result(self, resultado):
        new_window = tk.Toplevel(self.root)
        new_window.resizable(False, False)
        if "imagens/qiqi_pull.png" in resultado:
            gif_path = "imagens/qiqi.gif"
        elif "imagens/firefly_pull.png" in resultado or "imagens/firefly_cone.png" in resultado or any(item in resultado for item in self.standard_possible_results):
            gif_path = "imagens/5_estrelas.gif"
        else:
            gif_path = "imagens/3_estrelas.gif"
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
        self.image_references.append(result_image) # lista
        
        frame = Frame(result_window, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        
        next_button = Button(result_window, bootstyle="light", text="Next", command=lambda: self.proximo(label))
        next_button.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)
        # Play the result song
        self.play_audio("imagens/result_song.mp3")

    def proximo(self, label):
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
        
    def get_user_inventory(self):
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main_test.py <user_id>")
        sys.exit(1)

    user_id = sys.argv[1]
    root = tk.Tk()
    app = WarpSimulator(root, user_id)
    root.mainloop()