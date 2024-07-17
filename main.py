import tkinter as tk
from ttkbootstrap import Style, Window, Notebook, Frame

class MainApp(tk.Tk):  # Subclasse de tk.Tk para criar a janela principal
    def __init__(self):
        super().__init__()
        
        self.title("Warp Simulator")
        self.geometry("800x500")
        
        # Configuração do estilo ttkbootstrap
        style = Style(theme='darkly')  # Escolha do tema 'darkly'
        style.configure('custom.TNotebook', tabposition="w")
        
        # Notebook (abas)
        nb_tabs = Notebook(self, style='custom.TNotebook')
        nb_tabs.pack(expand=1, fill='both')
        
        # Primeira aba
        home_tab = Frame(nb_tabs)
        nb_tabs.add(home_tab, text="Firefly")
        
        # Segunda aba
        search_tab = Frame(nb_tabs)
        nb_tabs.add(search_tab, text="Light Cone")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()