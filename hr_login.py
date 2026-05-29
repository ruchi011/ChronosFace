import customtkinter as ctk
import subprocess
import sys
from tkinter import messagebox
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("HR Login")
app.geometry("500x500")
app.configure(fg_color="#0f172a")
title = ctk.CTkLabel(
    app,
    text="HR Login",
    font=("Segoe UI", 42, "bold")
)
title.pack(pady=40)
username_entry = ctk.CTkEntry(
    app,
    width=320,
    height=55,
    placeholder_text="HR Username",
    font=("Arial", 18)
)
username_entry.pack(pady=20)
password_entry = ctk.CTkEntry(
    app,
    width=320,
    height=55,
    placeholder_text="HR Password",
    show="*",
    font=("Arial", 18)
)
password_entry.pack(pady=20)
def login_hr():
    username = username_entry.get()
    password = password_entry.get()
    if username == "hr" and password == "hr123":
        app.destroy()
        subprocess.run([
            sys.executable,
            "hr_login.py"
        ])
    else:
        messagebox.showerror(
            "Access Denied",
            "Invalid HR Credentials"
        )
login_btn = ctk.CTkButton(
    app,
    text="Login",
    width=300,
    height=55,
    font=("Arial", 22),
    fg_color="#ca8a04",
    hover_color="#a16207",
    text_color="black",
    command=login_hr
)
login_btn.pack(pady=35)
back_btn = ctk.CTkButton(
    app,
    text="Back",
    width=300,
    height=55,
    font=("Arial", 22),
    fg_color="gray",
    command=lambda: [
        app.destroy(),
        subprocess.run([
            sys.executable,
            "login.py"
        ])
    ]
)
back_btn.pack(pady=10)
app.mainloop()