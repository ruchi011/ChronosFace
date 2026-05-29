import customtkinter as ctk
from PIL import Image
import sqlite3
ImportError
ctk.set_appearance_mode("dark")
def open_profile(employee_id):
    profile = ctk.CTkToplevel()
    profile.title("Profile")
    profile.geometry("500x650")
    profile.configure(fg_color="#0f172a")
    conn = sqlite3.connect("database/chronosface.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        name,
        department,
        email,
        photo
    FROM employees
    WHERE employee_id = ?
    """, (employee_id,))
    employee = cursor.fetchone()
    conn.close()
    if employee:
        name = employee[0]
        department = employee[1]
        email = employee[2]
        photo = employee[3]
    else:
        name = "Unknown"
        department = "Unknown"
        email = "Unknown"
        photo = None
    title = ctk.CTkLabel(
        profile,
        text="Employee Profile",
        font=("Segoe UI", 34, "bold")
    )
    title.pack(pady=30)
    if photo:
        profile_image = ctk.CTkImage(
            light_image=Image.open(photo),
            dark_image=Image.open(photo),
            size=(160, 160)
        )
        image_label = ctk.CTkLabel(
            profile,
            image=profile_image,
            text=""
        )
        image_label.pack(pady=20)
    name_label = ctk.CTkLabel(
        profile,
        text=f"Name : {name}",
        font=("Segoe UI", 20)
    )
    name_label.pack(pady=10)
    id_label = ctk.CTkLabel(
        profile,
        text=f"Employee ID : {employee_id}",
        font=("Segoe UI", 20)
    )
    id_label.pack(pady=10)
    dept_label = ctk.CTkLabel(
        profile,
        text=f"Department : {department}",
        font=("Segoe UI", 20)
    )
    dept_label.pack(pady=10)
    email_label = ctk.CTkLabel(
        profile,
        text=f"Email : {email}",
        font=("Segoe UI", 18)
    )
    email_label.pack(pady=10)   