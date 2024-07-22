from tkinter import *
from PIL import ImageTk, Image 
import time

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")
        self.root.geometry("300x200")

        open_window_button = Button(root, text="Open New Window", command=self.open_new_window)
        open_window_button.pack(pady=20)

    def open_new_window(self):
        new_window = Toplevel(self.root)
        new_window.title("GIF Window")
        new_window.geometry("300x200")

        gif_label = Label(new_window)
        gif_label.pack()

        gif_frames = [PhotoImage(file="imagens/3_estrelas.gif", format=f"gif -index {i}") for i in range(100)] # Adjust the range to the number of frames in your gif

        def animate_gif(count):
            gif_frame = gif_frames[count]
            gif_label.configure(image=gif_frame)
            count += 1
            if count == len(gif_frames):
                count = 0
            self.gif_animation = new_window.after(100, animate_gif, count)

        animate_gif(0)

        def stop_gif():
            new_window.after_cancel(self.gif_animation)
            gif_label.pack_forget()
            image = ImageTk.PhotoImage(Image.open("imagens/firefly_pull.png"))  # Replace with your image file
            image_label = Label(new_window, image=image)
            image_label.image = image  # Keep a reference to avoid garbage collection
            image_label.pack()
            new_window.after(5000, new_window.destroy)  # Close the window after 5 seconds

        new_window.after(3000, stop_gif)  # Stop GIF after 3 seconds

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
