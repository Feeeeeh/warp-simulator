from gif_loader import AnimatedGif
from tkinter import *
def pull1x():
    print("1 pull")
    root = Tk()
    gif = AnimatedGif(root, 'imagens/qiqi.gif')
    gif.pack()
    root.mainloop()
def pull10x():
    print("10 pulls")
    
