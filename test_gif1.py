from tkinter import *
import time
import os
root = Tk()

frameCnt = 334
frames = [PhotoImage(file='imagens/5_estrelas.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(30, update, ind)
label = Label(root)
label.pack()
root.after(30, update, 0)
root.mainloop()