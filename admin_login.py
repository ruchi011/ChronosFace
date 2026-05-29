import customtkinter as ctk
import subprocess
import sys
from tkinter import messagebox
import sqlite3
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Admin Login")
app.geometry("500x500")
app.configure(fg_color="#0f172a")
title = ctk.CTkLabel(
    app,
    text="Admin Login",
    font=("Segoe UI", 42, "bold")
)
title.pack(pady=40)
username_entry = ctk.CTkEntry(
    app,
    width=320,
    height=55,
    placeholder_text="Admin Username",
    font=("Arial", 18)
)
username_entry.pack(pady=20)
password_entry = ctk.CTkEntry(
    app,
    width=320,
    height=55,
    placeholder_text="Admin Password",
    show="*",
    font=("Arial", 18)
)
password_entry.pack(pady=20)
def login_admin():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    if username == "" or password == "":
        messagebox.showerror(
            "Error",
            "All Fields Are Required"
        )
        return
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT password
    FROM admins
    WHERE username = ?
    """, (username,))
    admin = cursor.fetchone()
    conn.close()
    if admin and admin[0] == password:
        app.destroy()
        subprocess.Popen([
            sys.executable,
            "admin_dashboard.py"
        ])
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Admin Credentials"
        )
login_btn = ctk.CTkButton(
    app,
    text="Login",
    width=300,
    height=55,
    font=("Arial", 22),
    fg_color="#15803d",
    hover_color="#166534",
    command=login_admin
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