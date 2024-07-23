import tkinter as tk
from ttkbootstrap import Style, Frame, Button, Notebook
from PIL import ImageTk, Image
from gif_loader import AnimatedGif
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

        self.firefly_pulls = ["imagens/firefly_pull.png", "imagens/bailu_pull.png", "imagens/himeko_pull.png"]
        self.fila = []
        self.result_windows = []

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
        self.show_gif(resultado)

    def pull10x(self):
        print("10 pulls")
        self.fila = [random.choice(self.firefly_pulls) for _ in range(10)]
        print(self.fila)
        self.show_gif()

    def show_gif(self, result_image_path=None):
        gif_window = tk.Toplevel(self.root)
        gif = AnimatedGif(gif_window, "imagens/5_estrelas.gif", loop=False, on_complete=lambda: self.show_result(gif_window, result_image_path))
        gif.pack()
        self.result_windows.append(gif_window)


    def show_result(self, gif_window, result_image_path):
        # Close the GIF window
        gif_window.destroy()
        
        # Create a new result window
        result_window = tk.Toplevel(self.root)
        self.result_windows.append(result_window)
        
        # Check if result_image_path is valid
        if not result_image_path:
            print("No image path provided.")
            return
    
        # Initialize the fila with the result image path
        self.fila = [result_image_path]
        
        # Set up the label and display the initial result image
        self.result_image_label = tk.Label(result_window)
        self.update_result_image(result_window)
        
        # Set up the 'Next' button
        frame = Frame(result_window, bootstyle="dark")
        frame.pack(side="bottom", fill="both")
        next_button = Button(result_window, bootstyle="light", text="Next", command=lambda: self.update_result_image(result_window))
        next_button.pack(in_=frame, anchor='s', side='left', fill="both", expand=True)
    
    def update_result_image(self, result_window):
        if self.fila:
            image_path = self.fila.pop(0)
            
            try:
                # Open and display the image
                result_image = ImageTk.PhotoImage(Image.open(image_path))
                self.result_image_label.config(image=result_image)
                self.result_image_label.image = result_image  # Keep a reference to avoid garbage collection
            except Exception as e:
                print(f"Error loading image: {e}")
                result_window.destroy()  # Close the window if there's an error
        else:
            result_window.destroy()  # No more results, close this window


def main():
    root = tk.Tk()
    app = WarpSimulator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
