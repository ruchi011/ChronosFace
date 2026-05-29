import customtkinter as ctk
import subprocess
import sys
import sqlite3
from tkinter import messagebox
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Employee Login")
app.geometry("500x550")
app.configure(fg_color="#0f172a")
title = ctk.CTkLabel(
    app,
    text="Employee Login",
    font=("Segoe UI", 38, "bold")
)
title.pack(pady=40)
employee_id_entry = ctk.CTkEntry(
    app,
    width=320,
    height=55,
    placeholder_text="Employee ID",
    font=("Arial", 18),
    corner_radius=15
)
employee_id_entry.pack(pady=20)
password_entry = ctk.CTkEntry(
    app,
    width=320,
    height=55,
    placeholder_text="Password",
    show="*",
    font=("Arial", 18),
    corner_radius=15
)
password_entry.pack(pady=20)
def login_employee():
    employee_id = employee_id_entry.get().strip()
    password = password_entry.get().strip()
    if employee_id == "" or password == "":
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
    FROM employees
    WHERE employee_id = ?
    """, (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    if employee and employee[0] == password:
        print("Employee ID Passed:", employee_id)
        with open(
            "current_employee.txt",
            "w"
        ) as file:
            file.write(employee_id)
        subprocess.Popen([
            sys.executable,
            "employee_dashboard.py",
            str(employee_id)
        ])
        app.destroy()
    else:
        messagebox.showerror(
            "Access Denied",
            "Invalid Employee Credentials"
        )
login_btn = ctk.CTkButton(
    app,
    text="Login",
    width=300,
    height=55,
    font=("Arial", 22),
    fg_color="#2563eb",
    hover_color="#1d4ed8",
    corner_radius=15,
    command=login_employee
)
login_btn.pack(pady=35)
back_btn = ctk.CTkButton(
    app,
    text="Back",
    width=300,
    height=55,
    font=("Arial", 22),
    fg_color="gray",
    hover_color="#4b5563",
    corner_radius=15,
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