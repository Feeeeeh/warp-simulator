import tkinter as tk
from ttkbootstrap import Style, Frame, Button, Notebook
from PIL import ImageTk, Image
from gif_test import AnimatedGif
import random

class WarpSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Warp Simulator")
        self.root.geometry("800x500")

        # Configure ttkbootstrap style
        self.style = Style(theme='darkly')
        self.style.configure('custom.TNotebook', tabposition="wn", padding=[5, 5])
        self.style.configure('TNotebook.Tab', width=15)

        # Create notebook for tabs
        self.notebook = Notebook(style='custom.TNotebook')
        self.notebook.pack(expand=True, fill='both')
        self.image_references = []

        self.firefly_pulls = ["imagens/firefly_pull.png", "imagens/bailu_pull.png", "imagens/himeko_pull.png","imagens/welt_pull.png","imagens/yanqing_pull.png","imagens/clara_pull.png","imagens/bronya_pull.png",
                              "imagens/gepard_pull.png"]

        self.fila = []
        self.current_10x_index = 0  # To track current index for 10x pulls

        self.create_tabs()

    def create_tabs(self):
        self.create_tab("Firefly", "imagens/firefly_banner.png", self.pull1x, self.pull10x)
        self.create_tab("Light Cone", "imagens/cone_banner.png", self.pull1x, self.pull10x)
        self.create_standard_tab("Standard", "imagens/Stellar_Warp.png", self.pull1x, self.pull10x)

    def create_tab(self, title, banner_image_path, pull1x_command, pull10x_command):
        tab = Frame(self.notebook, width=200, height=200)
        self.notebook.add(tab, text=title, padding=10)
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

    def pull1x(self):
        print("1 pull")
        resultado = random.choice(self.firefly_pulls)
        print(resultado)
        self.show_gif_and_result(resultado)

    def pull10x(self):
        print("10 pulls")
        self.fila = [random.choice(self.firefly_pulls) for _ in range(10)]
        print(self.fila)
        self.current_10x_index = 0  # Reset index for new 10x pulls
        self.show_gif_and_result(self.fila[self.current_10x_index])

    def show_gif_and_result(self, resultado):
        new_window = tk.Toplevel(self.root)
        if isinstance(resultado, str):  # Single pull
            gif_path = "imagens/5_estrelas.gif" if resultado == "imagens/firefly_pull.png" else "imagens/3_estrelas.gif"
        else:  # 10x pull
            gif_path = "imagens/5_estrelas.gif" if any(r == "imagens/firefly_pull.png" for r in resultado) else "imagens/3_estrelas.gif"
        
        gif = AnimatedGif(new_window, gif_path, loop=False, on_complete=lambda: self.show_result(new_window, resultado))
        gif.pack()

    def show_result(self, window, result):
        if isinstance(result, str):  # Single pull
            result_image_path = result
            self.create_result_window(window, result_image_path)
        else:  # 10x pull
            if self.current_10x_index < len(result):
                result_image_path = result[self.current_10x_index]
                self.create_result_window(window, result_image_path)
                self.current_10x_index += 1
            else:
                self.close_all_windows()

    def create_result_window(self, window, image_path):
        result_window = tk.Toplevel(window)
        result_image = ImageTk.PhotoImage(Image.open(image_path))
        img_frame = Frame(result_window)
        img_frame.pack(fill="both",expand=True)
        label = tk.Label(img_frame, image=result_image)
        label.pack()
        self.image_references.append(result_image)
        
        frame = Frame(result_window, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        
        next_button = Button(result_window, bootstyle="light", text="Next", command=lambda: self.proximo(result_window, label))
        next_button.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)

    def proximo(self, result_window, label):
        if self.current_10x_index < len(self.fila):
            result_image_path = self.fila[self.current_10x_index]
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
