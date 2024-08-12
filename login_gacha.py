import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
from ttkbootstrap import Style, Frame, Button
import subprocess

# conexão com o root pra chegar na database
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "HSR"

def login():
    username = entry_username.get()
    password = entry_password.get()

    user_id = validate_user(username, password)  # uma função que pega o id do usuario do banco de dados

    if user_id:
        root.withdraw()  # esconde a tela de login, mas ela continua rodando em segundo plano
        try:
            subprocess.call(["python", "app.py", str(user_id)]) # inicia o arquivo app.py como um subprocesso
        except Exception as e:
            root.deiconify()
            messagebox.showerror("Erro:", f"{e}")
        root.deiconify()  # o contrario do withdraw, abre de novo o aplicativo que ficou em segundo plano
                          # nesse caso, ele vai abrir de novo a tela caso o app.py seja fechado
    else:
        messagebox.showerror("Erro de login.")
    
    # chama a função pra limpar o que está na entry, caso os widgets existam
    if entry_username.winfo_exists() and entry_password.winfo_exists():
        clear_entries() 
     
        
def register():
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
        user = cursor.fetchone() # pegou o usuario no qual o nome e a senha se encaixam
        conn.close()
        return user[0] if user else None # retornou o primeiro item do usuario, no caso, o id
    
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
        
        # checa se o nome ja existe
        cursor.execute("SELECT * FROM login WHERE nome = %s", (username,))
        if cursor.fetchone():
            conn.close()
            return False  # caso ele conseguir pegar 1 item com aquele nome
        
        # adiciona o novo usuario
        cursor.execute("INSERT INTO login (nome, senha) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as e:
        messagebox.showerror(f"Erro de Database: {e}")
        return False

def show_login(): # mostra as entries e botões pro login
    clear_frame()
    label_username.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_username.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    label_password.grid(row=1, column=4, padx=5, pady=5, sticky='e')
    entry_password.grid(row=1, column=5, padx=5, pady=5, sticky='w')
    button_login.grid(row=1, column=8, padx=20, pady=5, sticky='e')
    back_button.grid(row=1, column=10, padx=20, pady=5, sticky='e')

def show_register(): # mostra as entries e botões pro registro
    clear_frame()
    label_username.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    entry_username.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    label_password.grid(row=1, column=4, padx=5, pady=5, sticky='e')
    entry_password.grid(row=1, column=5, padx=5, pady=5, sticky='w')
    button_register.grid(row=1, column=8, padx=20, pady=5, sticky='e')
    back_button.grid(row=1, column=10, padx=20, pady=5, sticky='e')

def voltar(): # limpa a tela e volta pro começo do programa
    clear_frame()
    tela_inicial()

def clear_frame(): # limpa a tela
    for widget in frame_login.winfo_children():
        widget.grid_remove()

def clear_entries(): # limpa o que estiver nas entries
    if entry_username.winfo_exists() and entry_password.winfo_exists():
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)

def on_return_key(event): # pra entry funcionar com enter
    login()

# setup basico do tkinter com o tema darkly da biblioteca ttkbootstrap
root = tk.Tk()
root.title("Login")
root.geometry("600x400")
style = Style(theme='darkly')

# imagem de fundo
banner_image = ImageTk.PhotoImage(Image.open("imagens/wallpaper.png"))
tk.Label(root, image=banner_image).place(relx=0, rely=0, relwidth=1, relheight=0.9)

# frame pros botões abaixo da imagem
frame_login = Frame(root)
frame_login.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)

def tela_inicial(): # tela inicial com botões de Login/Register
    button_show_login = Button(frame_login, text="Login", command=show_login, bootstyle="primary")
    button_show_login.grid(row=0, column=0, padx=5, pady=5)
    button_show_register = Button(frame_login, text="Register", command=show_register, bootstyle="success")
    button_show_register.grid(row=0, column=1, padx=5, pady=5)
tela_inicial()

# entrada de usuario
label_username = tk.Label(frame_login, text="Username", bg="white")
entry_username = tk.Entry(frame_login)

# entrada de senha
label_password = tk.Label(frame_login, text="Password", bg="white")
entry_password = tk.Entry(frame_login, show="*")

# botão de login
button_login = Button(frame_login, text="Login", command=login, bootstyle="info")

# botão de registro
button_register = Button(frame_login, text="Register", command=register, bootstyle="info")

# botão de voltar
back_button = Button(frame_login, text="Back", command=voltar, bootstyle="danger")

# fazer o entry enviar com enter
root.bind('<Return>', on_return_key) # return é o enter 
root.mainloop()