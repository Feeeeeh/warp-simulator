import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
from ttkbootstrap import Style, Frame, Button

# Database connection details
DB_HOST = "your_host"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_NAME = "your_database"

# Function to handle login
def handle_login():
    username = entry_username.get()
    password = entry_password.get()
    
    if validate_user(username, password):
        messagebox.showinfo("Login", "Login successful!")
    else:
        messagebox.showerror("Login", "Invalid username or password.")

# Function to validate user credentials
def validate_user(username, password):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False

# Function to handle pressing the Return key
def on_return_key(event):
    handle_login()

references = []

# Tkinter setup
root = tk.Tk()
root.title("Login")
root.geometry("700x400")
style = Style(theme='darkly')

# Background image
banner_image = ImageTk.PhotoImage(Image.open("imagens/wallpaper.png"))
references.append(banner_image)
tk.Label(root, image=banner_image).place(relx=0, rely=0, relwidth=1, relheight=0.8)

# Frame for login form
frame_login = Frame(root)
frame_login.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

# Username entry
label_username = tk.Label(frame_login, text="Username", bg="white")
label_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_username = tk.Entry(frame_login)
entry_username.grid(row=0, column=1, padx=5, pady=5, sticky='w')

# Password entry
label_password = tk.Label(frame_login, text="Password", bg="white")
label_password.grid(row=0, column=2, padx=5, pady=5, sticky='e')
entry_password = tk.Entry(frame_login, show="*")
entry_password.grid(row=0, column=3, padx=5, pady=5, sticky='w')

# Spacer
frame_login.columnconfigure(4, weight=1)

# Login button
button_login = Button(frame_login, text="Login", command=handle_login, bootstyle = "info")
button_login.grid(row=0, column=5, padx=20, pady=5, sticky='e')

# Bind the Return key to the login function
root.bind('<Return>', on_return_key)

root.mainloop()
