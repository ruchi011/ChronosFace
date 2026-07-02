import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import subprocess
import sys
from email_utils import send_email
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("Employee Signup")
app.geometry("650x850")
app.configure(fg_color="#0f172a")
def initialize_departments_table():
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT UNIQUE
    )
    """)
    default_departments = [
        "IT",
        "HR",
        "Finance",
        "Management",
        "AI Team",
        "Security"
    ]
    for dept in default_departments:
        try:
            cursor.execute("""
            INSERT INTO departments (
                department_name
            )
            VALUES (?)
            """, (dept,))
        except:
            pass
    conn.commit()
    conn.close()
initialize_departments_table()
def load_departments():
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT department_name
    FROM departments
    ORDER BY department_name
    """)
    departments = [
        row[0]
        for row in cursor.fetchall()
    ]
    conn.close()
    return departments
title = ctk.CTkLabel(
    app,
    text="Create Employee Account",
    font=("Segoe UI", 36, "bold")
)
title.pack(pady=30)
employee_id_entry = ctk.CTkEntry(
    app,
    width=380,
    height=55,
    placeholder_text="Employee ID",
    font=("Arial", 16)
)
employee_id_entry.pack(pady=6)
name_entry = ctk.CTkEntry(
    app,
    width=380,
    height=55,
    placeholder_text="Full Name",
    font=("Arial", 16)
)
name_entry.pack(pady=6)
department_menu = ctk.CTkOptionMenu(
    app,
    values=load_departments(),
    width=380,
    height=55,
    font=("Arial", 16)
)
department_menu.pack(pady=6)
new_department_entry = ctk.CTkEntry(
    app,
    width=380,
    height=55,
    placeholder_text="Add New Department",
    font=("Arial", 16)
)
new_department_entry.pack(pady=6)
def add_department():
    department_name = (
        new_department_entry.get().strip()
    )
    if department_name == "":
        messagebox.showerror(
            "Error",
            "Enter Department Name"
        )
        return
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO departments (
            department_name
        )
        VALUES (?)
        """, (department_name,))
        conn.commit()
        messagebox.showinfo(
            "Success",
            f"{department_name} Added"
        )
        department_menu.configure(
            values=load_departments()
        )
        department_menu.set(
            department_name
        )
        new_department_entry.delete(
            0,
            "end"
        )
    except:
        messagebox.showerror(
            "Error",
            "Department Already Exists"
        )
    conn.close()
add_department_btn = ctk.CTkButton(
    app,
    text="➕ Add Department",
    width=300,
    height=50,
    font=("Arial", 18, "bold"),
    fg_color="#7c3aed",
    hover_color="#6d28d9",
    command=add_department
)
add_department_btn.pack(pady=15)
email_entry = ctk.CTkEntry(
    app,
    width=380,
    height=55,
    placeholder_text="Email",
    font=("Arial", 16)
)
email_entry.pack(pady=6)
password_entry = ctk.CTkEntry(
    app,
    width=380,
    height=55,
    placeholder_text="Password",
    show="*",
    font=("Arial", 16)
)
password_entry.pack(pady=6)
confirm_password_entry = ctk.CTkEntry(
    app,
    width=380,
    height=55,
    placeholder_text="Confirm Password",
    show="*",
    font=("Arial", 16)
)
confirm_password_entry.pack(pady=6)
def signup():
    employee_id = (
        employee_id_entry.get().strip()
    )
    name = (
        name_entry.get().strip()
    )
    department = (
        department_menu.get()
    )
    email = (
        email_entry.get().strip()
    )
    password = (
        password_entry.get().strip()
    )
    confirm_password = (
        confirm_password_entry.get().strip()
    )
    if (
        employee_id == "" or
        name == "" or
        email == "" or
        password == "" or
        confirm_password == ""
    ):
        messagebox.showerror(
            "Error",
            "All Fields Are Required"
        )
        return
    if password != confirm_password:
        messagebox.showerror(
            "Error",
            "Passwords Do Not Match"
        )
        return
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT *
    FROM employees
    WHERE employee_id = ?
    """, (employee_id,))
    existing_user = cursor.fetchone()
    if existing_user:
        messagebox.showerror(
            "Error",
            "Employee ID Already Exists"
        )
        conn.close()
        return
    cursor.execute("""
    INSERT INTO employees (
        employee_id,
        name,
        department,
        email,
        password
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        employee_id,
        name,
        department,
        email,
        password
    ))
    conn.commit()
    conn.close()
    try:
        send_email(
            email,
            "Welcome to ChronosFace AI",
            f"""
Hello {name},
Welcome to ChronosFace AI.
Your employee account has been created successfully.
Employee ID: {employee_id}
Department: {department}
Thank you.
"""
        )
    except Exception as e:
        print(
            "Email Error:",
            e
        )
    messagebox.showinfo(
        "Success",
        "Account Created Successfully"
    )
    app.destroy()
    subprocess.Popen([
        sys.executable,
        "employee_login.py"
    ])
signup_btn = ctk.CTkButton(
    app,
    text="Create Account",
    width=320,
    height=60,
    font=("Arial", 22, "bold"),
    fg_color="#15803d",
    hover_color="#166534",
    corner_radius=15,
    command=signup
)
signup_btn.pack(pady=35)
back_btn = ctk.CTkButton(
    app,
    text="Back",
    width=320,
    height=55,
    font=("Arial", 20),
    fg_color="gray",
    hover_color="#4b5563",
    corner_radius=15,
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