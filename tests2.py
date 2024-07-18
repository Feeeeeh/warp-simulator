import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image 

root = tk.Tk()
root.title("Warp Simulator")
root.geometry("800x500")

# Notebook (tabs)
notebook = ttk.Notebook(root, width=800, height=500)
notebook.pack(expand=True, fill='both')

# First tab
firefly_tab = ttk.Frame(notebook)
notebook.add(firefly_tab, text="Test Tab")

# Load and resize image
image_path = "imagens/Stellar_Warp.png"
image = Image.open(image_path)
# Resize image
resized_image = image.resize((200, 200))
# Convert Image object to PhotoImage object
resized_photo = ImageTk.PhotoImage(resized_image)

# Display resized image in a label
image_label = tk.Label(firefly_tab, image=resized_photo)
image_label.pack()

root.mainloop()