import tkinter as tk
from ttkbootstrap import *
from PIL import ImageTk, Image 

root = tk.Tk()
root.title("Warp Simulator")
root.geometry("800x500")

# Configuração do estilo ttkbootstrap
style = Style(theme='darkly')  # Escolha do tema 'darkly'
style.configure('custom.TNotebook', tabposition="wn",padding=[5, 5])
style.configure('TNotebook.Tab', width=15)

# Notebook (abas)
notebook = Notebook(style='custom.TNotebook')
notebook.pack(expand=True, fill='both') 

# Primeira aba
firefly_tab = Frame(notebook,width=200,height=200)
notebook.add(firefly_tab, text="Firefly", padding=10) 
firefly_banner = ImageTk.PhotoImage(Image.open("imagens/firefly_banner.png"))
tk.Label(firefly_tab, image=firefly_banner).pack()


# Segunda aba
cone_tab = Frame(notebook,width=200,height=200)
notebook.add(cone_tab, text="Light Cone", padding=10)
cone_banner = ImageTk.PhotoImage(Image.open("imagens/cone_banner.png"))
tk.Label(cone_tab, image=cone_banner).pack()  

# Terceira aba
standard_tab = Frame(notebook,width=200,height=200)
notebook.add(standard_tab, text="Standard", padding=10)
standard_banner = ImageTk.PhotoImage(Image.open("imagens/standard_banner.png"))
tk.Label(standard_tab, image=standard_banner).pack()  
    


root.mainloop()