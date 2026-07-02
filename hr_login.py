import customtkinter as ctk
import subprocess
import sys
from tkinter import messagebox
import sqlite3
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
DB_PATH = "database/chronosface.db"
def login_hr():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        hr_username,
        hr_password
    FROM settings
    WHERE id=1
    """)
    row = cursor.fetchone()
    conn.close()
    if row is None:
        messagebox.showerror(
            "Error",
            "HR credentials not found."
        )
        return
    db_username, db_password = row
    if (
        username == db_username
        and
        password == db_password
    ):
        app.destroy()
        subprocess.Popen([
            sys.executable,
            "hr_dashboard.py"
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
    height=45,
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
        subprocess.Popen([
            sys.executable,
            "login.py"
        ])
    ]
)
back_btn.pack(pady=10)
app.mainloop()