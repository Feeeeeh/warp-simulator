import tkinter as tk
from ttkbootstrap import Style, Frame, Button, Notebook
from PIL import ImageTk, Image
from gif_loader import AnimatedGif, AnimatedGif2
import random

class WarpSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Warp Simulator")
        self.root.geometry("800x500")

        self.style = Style(theme='darkly')
        self.style.configure('custom.TNotebook', tabposition="wn", padding=[5, 5])
        self.style.configure('TNotebook.Tab', width=15)

        self.notebook = Notebook(style='custom.TNotebook')
        self.notebook.pack(expand=True, fill='both')

        self.image_references = []

        self.firefly_pulls = ["imagens/firefly_pull.png", "imagens/bailu_pull.png", "imagens/himeko_pull.png"]

        self.setup_tabs()
    
    def setup_tabs(self):
        self.create_firefly_tab()
        self.create_cone_tab()
        self.create_standard_tab()

    def create_firefly_tab(self):
        firefly_tab = Frame(self.notebook, width=200, height=200)
        self.notebook.add(firefly_tab, text="Firefly", padding=10)
        firefly_banner = ImageTk.PhotoImage(Image.open("imagens/firefly_banner.png"))
        self.image_references.append(firefly_banner)
        tk.Label(firefly_tab, image=firefly_banner).pack()
        self.create_buttons(firefly_tab)
    
    def create_cone_tab(self):
        cone_tab = Frame(self.notebook, width=200, height=200)
        self.notebook.add(cone_tab, text="Light Cone", padding=10)
        cone_banner = ImageTk.PhotoImage(Image.open("imagens/cone_banner.png"))
        self.image_references.append(cone_banner)
        tk.Label(cone_tab, image=cone_banner).pack()
        self.create_buttons(cone_tab)
    
    def create_standard_tab(self):
        standard_tab = Frame(self.notebook, width=200, height=200)
        self.notebook.add(standard_tab, text="Standard", padding=10)
        warp = Image.open("imagens/Stellar_Warp.png")
        warp1 = warp.resize((700, 387))
        warp_r = ImageTk.PhotoImage(warp1)
        self.image_references.append(warp_r)
        tk.Label(standard_tab, image=warp_r).pack()
        self.create_buttons(standard_tab)
    
    def create_buttons(self, tab):
        frame = Frame(tab, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        button1 = Button(tab, bootstyle="dark", text="Warp 1x", command=self.pull1x)
        button10 = Button(tab, bootstyle="dark", text="Warp 10x", command=self.pull10x)
        button1.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)
        button10.pack(in_=frame, anchor='s', side='right', fill="both", expand=True)

    def pull1x(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Pull Result")
        new_window.geometry("300x200")

        resultado = random.choice(self.firefly_pulls)
        if resultado == "imagens/firefly_pull.png":
            gif = AnimatedGif(new_window, "imagens/5_estrelas.gif")
        else:
            gif = AnimatedGif2(new_window, "imagens/3_estrelas.gif")
        gif.pack()

        def stop_gif():
            gif.destroy()  # Stop and remove the GIF
            gif_label = tk.Label(new_window)
            gif_label.pack_forget()

            result_image = ImageTk.PhotoImage(Image.open(resultado))
            result_label = tk.Label(new_window, image=result_image)
            result_label.image = result_image  # Keep a reference to avoid garbage collection
            result_label.pack()
            new_window.after(5000, new_window.destroy)  # Close the window after 5 seconds

        new_window.after(3000, stop_gif)  # Stop GIF after 3 seconds

    def pull10x(self):
        print("10 pulls")

def main():
    root = tk.Tk()
    app = WarpSimulatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
