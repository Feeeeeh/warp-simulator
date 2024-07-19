import tkinter as tk
from ttkbootstrap import *
from PIL import ImageTk, Image 
from pulls import pull1x,pull10x

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
image_references = []

def botoes(tab):
    frame = Frame(tab,bootstyle="dark")
    frame.pack(side="bottom",fill="both")
    button1 = Button(tab,bootstyle="dark",text="Warp 1x", command=pull1x)
    button10 = Button(tab,bootstyle="dark",text="Warp 10x",command=pull10x)
    button1.pack(in_=frame,anchor='s',side='left',fill="both",expand=True)
    button10.pack(in_=frame,anchor='s',side='right',fill="both",expand=True)
def firefly(): # Primeira aba
    firefly_tab = Frame(notebook,width=200,height=200)
    notebook.add(firefly_tab, text="Firefly", padding=10) 
    firefly_banner = ImageTk.PhotoImage(Image.open("imagens/firefly_banner.png"))
    image_references.append(firefly_banner)
    Label(firefly_tab, image=firefly_banner).pack()
    botoes(firefly_tab)

def cone(): # Segunda aba
    cone_tab = Frame(notebook,width=200,height=200)
    notebook.add(cone_tab, text="Light Cone", padding=10)
    cone_banner = ImageTk.PhotoImage(Image.open("imagens/cone_banner.png"))
    image_references.append(cone_banner)
    Label(cone_tab, image=cone_banner).pack()  
    botoes(cone_tab)

def standard(): # Terceira aba
    standard_tab = Frame(notebook,width=200,height=200)
    notebook.add(standard_tab, text="Standard", padding=10)
    warp = Image.open("imagens/Stellar_Warp.png")
    warp1 = warp.resize((700,387))
    warp_r = ImageTk.PhotoImage(warp1)
    image_references.append(warp_r)
    Label(standard_tab, image=warp_r).pack()
    botoes(standard_tab)
    
    
def main():
    firefly()
    cone()
    standard()
    root.mainloop()

if __name__ == "__main__":
    main()