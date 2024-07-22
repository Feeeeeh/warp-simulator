import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class AnimatedGif:
    def __init__(self, root, src='', loop=True, on_complete=None):
        self.root = root
        self.loop = loop
        self.on_complete = on_complete

        # Load Frames
        self.image = Image.open(src)
        self.frames = []
        self.duration = []
        for frame in ImageSequence.Iterator(self.image):
            self.duration.append(frame.info['duration'])
            self.frames.append(ImageTk.PhotoImage(frame))
        self.counter = 0
        self.image = self.frames[self.counter]

        # Create Label
        self.label = tk.Label(self.root, image=self.image)
        self.label.pack()

        # Start Animation
        self.__step_frame()

    def __step_frame(self):
        if self.root.winfo_exists():
            # Update Frame
            self.label.config(image=self.frames[self.counter])
            self.image = self.frames[self.counter]

            # Loop Counter
            self.counter += 1
            if self.counter >= len(self.frames):
                if self.loop:
                    self.counter = 0
                else:
                    if self.on_complete:
                        self.on_complete()
                    return

            # Queue Frame Update
            self.root.after(self.duration[self.counter], self.__step_frame)

    def pack(self, **kwargs):
        self.label.pack(**kwargs)

    def grid(self, **kwargs):
        self.label.grid(**kwargs)

if __name__ == "__main__":
    root = tk.Tk()
    gif = AnimatedGif(root, "imagens/3_estrelas.gif", loop=False, on_complete=root.destroy)
    gif.pack()
    root.mainloop()
