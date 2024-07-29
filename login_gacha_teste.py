import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
from ttkbootstrap import Style, Frame, Button
import subprocess  # To start the main file

# Database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "HSR"

def handle_login():
    username = entry_username.get()
    password = entry_password.get()

    user_id = validate_user(username, password)  # Get user ID

    if user_id:
        root.withdraw()  # Hide the login window
        try:
            subprocess.call(["python", "app_teste.py", str(user_id)])
        except Exception as e:
            root.deiconify()
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        root.deiconify()  # Show the login window again when the main app closes
    else:
        messagebox.showerror("Login Error", "Invalid username or password.")
    
    # Call clear_entries() only if the widgets are valid
    if entry_username.winfo_exists() and entry_password.winfo_exists():
        clear_entries()  # Clear the entry fields after attempting login
     
        
def handle_register():
    username = entry_username.get()
    password = entry_password.get()
    
    if add_user(username, password):
        messagebox.showinfo("Registration Successful", "Registration successful!")
        show_login()  # Show the login form after successful registration
    else:
        messagebox.showerror("Registration Error", "Registration failed. User may already exist.")
    
    # Call clear_entries() only if the widgets are valid
    if entry_username.winfo_exists() and entry_password.winfo_exists():
        clear_entries()  # Clear the entry fields after attempting registration

def validate_user(username, password):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM login WHERE nome = %s AND senha = %s", (username, password))
        user = cursor.fetchone()
        conn.close()
        return user[0] if user else None
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def add_user(username, password):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Check if the username already exists
        cursor.execute("SELECT * FROM login WHERE nome = %s", (username,))
        if cursor.fetchone():
            conn.close()
            return False  # User already exists
        
        # Insert the new user
        cursor.execute("INSERT INTO login (nome, senha) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return False

def show_login():
    clear_frame()
    label_username.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_username.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    label_password.grid(row=1, column=4, padx=5, pady=5, sticky='e')
    entry_password.grid(row=1, column=5, padx=5, pady=5, sticky='w')
    button_login.grid(row=1, column=8, padx=20, pady=5, sticky='e')
    back_button.grid(row=1, column=10, padx=20, pady=5, sticky='e')

def show_register():
    clear_frame()
    label_username.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_username.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    label_password.grid(row=1, column=4, padx=5, pady=5, sticky='e')
    entry_password.grid(row=1, column=5, padx=5, pady=5, sticky='w')
    button_register.grid(row=1, column=8, padx=20, pady=5, sticky='e')
    back_button.grid(row=1, column=10, padx=20, pady=5, sticky='e')

def go_back():
    clear_frame()
    login()

def clear_frame():
    for widget in frame_login.winfo_children():
        widget.grid_remove()

def clear_entries():
    if entry_username.winfo_exists() and entry_password.winfo_exists():
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)

def on_return_key(event):
    handle_login()

# Tkinter setup
root = tk.Tk()
root.title("Login")
root.geometry("600x400")
style = Style(theme='darkly')

# Background image
banner_image = ImageTk.PhotoImage(Image.open("imagens/wallpaper.png"))
tk.Label(root, image=banner_image).place(relx=0, rely=0, relwidth=1, relheight=0.9)

# Frame for login form
frame_login = Frame(root)
frame_login.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

def login(): # Login/Register buttons
    button_show_login = Button(frame_login, text="Login", command=show_login, bootstyle="primary")
    button_show_login.grid(row=0, column=0, padx=5, pady=5)
    button_show_register = Button(frame_login, text="Register", command=show_register, bootstyle="success")
    button_show_register.grid(row=0, column=1, padx=5, pady=5)
login()

# Username entry
label_username = tk.Label(frame_login, text="Username", bg="white")
entry_username = tk.Entry(frame_login)

# Password entry
label_password = tk.Label(frame_login, text="Password", bg="white")
entry_password = tk.Entry(frame_login, show="*")

# Login button
button_login = Button(frame_login, text="Login", command=handle_login, bootstyle="info")

# Register button
button_register = Button(frame_login, text="Register", command=handle_register, bootstyle="info")

# Back button
back_button = Button(frame_login, text="Back", command=go_back, bootstyle="danger")

# Bind the Return key to the login function
root.bind('<Return>', on_return_key)
root.mainloop()