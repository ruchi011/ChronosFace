from urllib import response

import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import subprocess
import sys
import requests
def save_employee():
    name = name_entry.get()
    employee_id = id_entry.get()
    department = dept_entry.get()
    email = email_entry.get()
    if not name or not employee_id:
        messagebox.showerror(
            "Error",
            "Fill all required fields"
        )
        return
    try:
        response = requests.post(
            "http://127.0.0.1:5000/api/biometric/register",
            json={
                "employeeId": employee_id,
                "employeeName": name,
                "department": department,
                "email": email,
                "phone": "9876543210",
                "faceEmbedding": [0.12, 0.34, 0.56]
            }
        )
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)  
        if response.status_code == 200:
            messagebox.showinfo(
                "Success",
                "Employee Added Through Server"
            )
            subprocess.Popen(
                [
                    sys.executable,
                    "capture_dataset.py",
                    name
                ]
            )
    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )
    
app = ctk.CTk()
app.geometry("500x600")
app.title("Add Employee")
title = ctk.CTkLabel(
    app,
    text="+ Add Employee",
    font=("Arial", 30, "bold")
)
title.pack(pady=20)
name_entry = ctk.CTkEntry(
    app,
    placeholder_text="Employee Name",
    width=300,
    height=40
)
name_entry.pack(pady=10)
id_entry = ctk.CTkEntry(
    app,
    placeholder_text="Employee ID",
    width=300,
    height=40
)
id_entry.pack(pady=10)
dept_entry = ctk.CTkEntry(
    app,
    placeholder_text="Department",
    width=300,
    height=40
)
dept_entry.pack(pady=10)
email_entry = ctk.CTkEntry(
    app,
    placeholder_text="Email",
    width=300,
    height=40
)
email_entry.pack(pady=10)
save_btn = ctk.CTkButton(
    app,
    text="Save Employee",
    width=250,
    height=50,
    command=save_employee
)
save_btn.pack(pady=30)
app.mainloop()
