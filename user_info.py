import customtkinter as ctk
import sqlite3

def open_user_info(parent):

    window = ctk.CTkToplevel(parent)
    window.transient(parent)
    window.grab_set()
    window.focus()
    window.title("User Information")
    window.geometry("1300x800")
    title = ctk.CTkLabel(
        window,
        text="Employee Information",
        font=("Segoe UI", 34, "bold")
    )
    title.pack(pady=20)
    table_frame = ctk.CTkScrollableFrame(
        window,
        width=1200,
        height=600
    )
    table_frame.pack(
        padx=20,
        pady=20,
        fill="both",
        expand=True
    )
    headers = [
        "ID",
        "Name",
        "Department",
        "Email"
    ]
    for col, header in enumerate(headers):
        ctk.CTkLabel(
            table_frame,
            text=header,
            font=("Segoe UI",18,"bold")
        ).grid(
            row=0,
            column=col,
            padx=20,
            pady=15
        )
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        employee_id,
        employee_name,
        department,
        email
    FROM biometric_data
    """)
    employees = cursor.fetchall()
    conn.close()
    for row_num, employee in enumerate(employees,start=1):
        for col_num, value in enumerate(employee):
            ctk.CTkLabel(
                table_frame,
                text=str(value)
            ).grid(
                row=row_num,
                column=col_num,
                padx=20,
                pady=10
            )