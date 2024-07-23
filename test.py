import tkinter as tk # global imports are bad
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()
nb = ttk.Notebook(root)
nb.pack(fill='both', expand=True)

f = tk.Frame(nb)
tk.Label(f, text="in frame").pack()

# must keep a global reference to these two
im = Image.open('imagens/firefly_icon.jpg')
ph = ImageTk.PhotoImage(im)

# note use of the PhotoImage rather than the Image
nb.add(f, text="profile", image=ph, compound='center') # use the tk constants

root.mainloop()