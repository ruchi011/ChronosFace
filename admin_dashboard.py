import customtkinter as ctk
import sqlite3
import subprocess
import sys
from tkinter import messagebox, ttk
import os
import shutil
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from tkinter import filedialog
import shutil
import pandas as pd
from profile_window import open_profile
from change_password import open_change_password
from email_utils import send_email
from payslip_generator import generate_payslip
import cv2
from PIL import Image
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from time import strftime
from PIL import ImageTk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("ChronosFace Admin Dashboard")
app.geometry("1500x850")    
conn = sqlite3.connect(
    "database/chronosface.db"
)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS leaves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    employee_name TEXT,
    leave_date TEXT,
    reason TEXT,
    status TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS visitors (
    visitor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    company TEXT,
    purpose TEXT,
    host_employee TEXT,
    visit_date TEXT,
    checkin_time TEXT,
    checkout_time TEXT,
    status TEXT,
    photo_path TEXT
)
""")
cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitor_whitelist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitor_name TEXT,
                phone TEXT,
                company TEXT
            )
            """)
cursor.execute("""
            CREATE TABLE IF NOT EXISTS visitor_blacklist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitor_name TEXT,
                phone TEXT,
                reason TEXT
            )
            """)
conn.commit()
conn.commit()
conn.close()
sidebar = ctk.CTkFrame( 
    app,
    width=220,
    fg_color="#111827",
    corner_radius=12
)
sidebar.pack(
    side="left",
    fill="y"
)
logo = ctk.CTkLabel(
    sidebar,
    text="ChronosFace",
    font=("Arial", 34, "bold")
)
logo.pack(pady=35)
main_frame = ctk.CTkFrame(
    app,
    fg_color="#1e1e1e"
)
main_frame.pack(
    side="right",
    fill="both",
    expand=True
)
dashboard_page = ctk.CTkFrame(main_frame)
employees_page = ctk.CTkFrame(main_frame)
attendance_page = ctk.CTkFrame(main_frame)
reports_page = ctk.CTkFrame(main_frame)
leave_page = ctk.CTkFrame(main_frame)
settings_page = ctk.CTkFrame(main_frame)
payroll_page = ctk.CTkFrame(main_frame)
groups_page=ctk.CTkFrame(main_frame)
visitor_page = ctk.CTkFrame(
    main_frame,
    fg_color="#1e1e1e"
)
for frame in (
    dashboard_page,
    employees_page,
    attendance_page,
    reports_page,
    leave_page,
    settings_page,
    payroll_page,
    groups_page,
    visitor_page
):
    frame.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )
def show_page(page):
    page.tkraise()
def load_employee_table():
    employee_table.configure(state="normal")
    employee_table.delete(
        "1.0",
        "end"
    )
    employee_table.insert(
        "end",
        "Employee Database\n\n"
    )
    employee_table.insert(
        "end",
        "ID       Name           Department\n"
    )
    employee_table.insert(
        "end",
        "--------------------------------------\n"
    )
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT employee_id, name, department FROM employees"
    )
    employees = cursor.fetchall()
    conn.close()
    for emp in employees:
        employee_table.insert(
            "end",
            f"{emp[0]:<10}{emp[1]:<18}{emp[2]}\n"
        )
    employee_table.configure(state="disabled")
def open_add_employee():
    global add_window
    add_window = ctk.CTkToplevel(app)
    add_window.focus()
    add_window.grab_set()
    add_window.lift()
    add_window.title("Add Employee")
    add_window.geometry("500x600")
    title = ctk.CTkLabel(
        add_window,
        text="Add Employee",
        font=("Arial", 32, "bold")
    )
    title.pack(pady=30)
    emp_id = ctk.CTkEntry(
        add_window,
        width=350,
        height=45,
        placeholder_text="Employee ID"
    )
    emp_id.pack(pady=15)
    emp_name = ctk.CTkEntry(
        add_window,
        width=350,
        height=45,
        placeholder_text="Employee Name"
    )
    emp_name.pack(pady=15)
    emp_dept = ctk.CTkEntry(
        add_window,
        width=350,
        height=45,
        placeholder_text="Department"
    )
    emp_dept.pack(pady=15)
    emp_email = ctk.CTkEntry(
        add_window,
        width=350,
        height=45,
        placeholder_text="Email"
    )
    emp_email.pack(pady=15)
    def save_employee():
        employee_id = emp_id.get()
        employee_name = emp_name.get()
        department = emp_dept.get()
        email = emp_email.get()
        try:
            conn = sqlite3.connect(
                "database/chronosface.db"
            )
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO employees (
                employee_id,
                name,
                department,
                email
            )
            VALUES (?, ?, ?, ?)
            """, (
                employee_id,
                employee_name,
                department,
                email
            ))
            conn.commit()
            conn.close()
            subprocess.run(
                [
                    sys.executable,
                    "capture_dataset.py",
                    employee_name
                ]
            )
            subprocess.run(
                [
                    sys.executable,
                    "generate_embeddings.py"
                ]
            )
            print("Employee Added Successfully")
            load_employee_table()
            add_window.destroy()
        except sqlite3.IntegrityError:
            print("Employee ID Already Exists")
        except sqlite3.OperationalError:
            print("Database is Locked")
    save_btn = ctk.CTkButton(
        add_window,
        text="Save Employee",
        width=300,
        height=50,
        font=("Arial", 20),
        command=save_employee
    )
    save_btn.pack(pady=40)
def open_modify_employee():
    global modify_window
    modify_window = ctk.CTkToplevel(app)
    modify_window.focus()
    modify_window.grab_set()
    modify_window.lift()
    modify_window.title("Modify Employee")
    modify_window.geometry("500x650")
    title = ctk.CTkLabel(
        modify_window,
        text="Modify Employee",
        font=("Arial", 32, "bold")
    )
    title.pack(pady=30)
    search_id = ctk.CTkEntry(
        modify_window,
        width=350,
        height=45,
        placeholder_text="Enter Employee ID"
    )
    search_id.pack(pady=15)
    emp_name = ctk.CTkEntry(
        modify_window,
        width=350,
        height=45,
        placeholder_text="Employee Name"
    )
    emp_name.pack(pady=15)
    emp_dept = ctk.CTkEntry(
        modify_window,
        width=350,
        height=45,
        placeholder_text="Department"
    )
    emp_dept.pack(pady=15)
    emp_email = ctk.CTkEntry(
        modify_window,
        width=350,
        height=45,
        placeholder_text="Email"
    )
    emp_email.pack(pady=15)
    def load_employee():
        employee_id = search_id.get()
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        cursor.execute("""
        SELECT
            employee_id,
            name,
            department,
            email
        FROM employees
        WHERE employee_id = ?
        """, (employee_id,))
        employee = cursor.fetchone()
        conn.close()
        if employee:
            emp_name.delete(0, "end")
            emp_name.insert(0, employee[0])
            emp_dept.delete(0, "end")
            emp_dept.insert(0, employee[1])
            emp_email.delete(0, "end")
            emp_email.insert(0, employee[2])
        else:
            print("Employee Not Found")
    def update_employee():
        employee_id = search_id.get()
        updated_name = emp_name.get()
        updated_department = emp_dept.get()
        updated_email = emp_email.get()
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE employees
        SET
            name = ?,
            department = ?,
            email = ?
        WHERE employee_id = ?
        """, (
            updated_name,
            updated_department,
            updated_email,
            employee_id
        ))
        conn.commit()
        print(cursor.rowcount)
        conn.close()
        print("Employee Updated Successfully")
        load_employee_table()
        modify_window.destroy()
    load_btn = ctk.CTkButton(
        modify_window,
        text="Load Employee",
        width=300,
        height=50,
        font=("Arial", 20),
        command=load_employee
    )
    load_btn.pack(pady=20)
    update_btn = ctk.CTkButton(
        modify_window,
        text="Update Employee",
        width=300,
        height=50,
        font=("Arial", 20),
        command=update_employee
    )
    update_btn.pack(pady=30)
def admin_delete_login():
    global login_window
    login_window = ctk.CTkToplevel(app)
    login_window.focus()
    login_window.grab_set()
    login_window.lift()
    login_window.title("Admin Verification")
    login_window.geometry("450x400")
    title = ctk.CTkLabel(
        login_window,
        text="Admin Verification",
        font=("Arial", 30, "bold")
    )
    title.pack(pady=30)
    username_entry = ctk.CTkEntry(
        login_window,
        width=300,
        height=45,
        placeholder_text="Admin Username"
    )
    username_entry.pack(pady=20)
    password_entry = ctk.CTkEntry(
        login_window,
        width=300,
        height=45,
        placeholder_text="Admin Password",
        show="*"
    )
    password_entry.pack(pady=20)
    def verify_admin():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "admin123":
            login_window.destroy()
            open_delete_employee()
        else:
            messagebox.showerror(
                "Access Denied",
                "Invalid Admin Credentials"
            )
    verify_btn = ctk.CTkButton(
        login_window,
        text="Verify Admin",
        width=250,
        height=50,
        font=("Arial", 18),
        command=verify_admin
    )
    verify_btn.pack(pady=35)
def open_delete_employee():
    global delete_window
    delete_window = ctk.CTkToplevel(app)
    delete_window.focus()
    delete_window.grab_set()
    delete_window.lift()
    delete_window.title("Delete Employee")
    delete_window.geometry("500x400")
    title = ctk.CTkLabel(
        delete_window,
        text="Delete Employee",
        font=("Arial", 32, "bold")
    )
    title.pack(pady=30)
    emp_id = ctk.CTkEntry(
        delete_window,
        width=350,
        height=45,
        placeholder_text="Enter Employee ID"
    )
    emp_id.pack(pady=25)
    def delete_employee():
        employee_id = emp_id.get().strip()
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        cursor.execute("""
        SELECT name
        FROM employees
        WHERE employee_id = ?
        """, (employee_id,))
        employee = cursor.fetchone()
        if employee:
            employee_name = employee[0]
            cursor.execute("""
            DELETE FROM employees
            WHERE employee_id = ?
            """, (employee_id,))
            conn.commit()
            conn.close()
            dataset_path = f"dataset/{employee_name}"
            if os.path.exists(dataset_path):
                shutil.rmtree(dataset_path)
            subprocess.run(
                [
                    sys.executable,
                    "generate_embeddings.py"
                ]
            )
            load_employee_table()
            messagebox.showinfo(
                "Success",
                "Employee Deleted Successfully"
            )
            delete_window.destroy()
        else:
            messagebox.showerror(
                "Error",
                "Employee Not Found"
            )
    delete_btn = ctk.CTkButton(
        delete_window,
        text="Delete Employee",
        width=200,
        height=50,
        font=("Arial", 18),
        fg_color="red",
        hover_color="darkred",
        command=delete_employee
    )
    delete_btn.pack(pady=35)
def open_change_photo():
    change_window = ctk.CTkToplevel(app)
    change_window.title("Change Employee Photo")
    change_window.geometry("500x350")
    change_window.focus()
    change_window.grab_set()
    title = ctk.CTkLabel(
        change_window,
        text="Change Employee Photo",
        font=("Arial", 28, "bold")
    )
    title.pack(pady=30)
    emp_id_entry = ctk.CTkEntry(
        change_window,
        width=320,
        height=45,
        placeholder_text="Enter Employee ID"
    )
    emp_id_entry.pack(pady=20)
    def update_photo():
        employee_id = emp_id_entry.get().strip()
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        cursor.execute("""
        SELECT name
        FROM employees
        WHERE employee_id = ?
        """, (employee_id,))
        employee = cursor.fetchone()
        conn.close()
        if employee:
            employee_name = employee[0]
            file_path = filedialog.askopenfilename(
                title="Select Employee Photo",
                filetypes=[
                    ("Image Files", "*.jpg *.jpeg *.png")
                ]
            )
            if file_path:
                dataset_path = f"dataset/{employee_name}"
                if os.path.exists(dataset_path):
                    shutil.rmtree(dataset_path)
                os.makedirs(dataset_path)
                shutil.copy(
                    file_path,
                    f"{dataset_path}/1.jpg"
                )
                subprocess.run([
                    sys.executable,
                    "generate_embeddings.py"
                ])
                messagebox.showinfo(
                    "Success",
                    "Employee Photo Updated Successfully"
                )
                change_window.destroy()
        else:
            messagebox.showerror(
                "Error",
                "Employee Not Found"
            )
    update_btn = ctk.CTkButton(
        change_window,
        text="Capture New Photo",
        width=250,
        height=50,
        font=("Arial", 18),
        fg_color="#9333ea",
        hover_color="#7e22ce",
        command=update_photo
    )
    update_btn.pack(pady=35)
dashboard_btn = ctk.CTkButton(
    sidebar,
    text="📊 Dashboard",
    width=220,
    height=45,
    font=("Arial", 18),
    command=lambda: show_page(dashboard_page)
)
dashboard_btn.pack(pady=12)
employees_btn = ctk.CTkButton(
    sidebar,
    text="👥 Employees",
    width=220,
    height=45,
    font=("Arial", 18),
    command=lambda: show_page(employees_page)
)
employees_btn.pack(pady=12)
attendance_btn = ctk.CTkButton(
    sidebar,
    text="Attendance",
    width=220,
    height=45,
    font=("Arial", 18),
    command=lambda: show_page(attendance_page)
)
attendance_btn.pack(pady=12)
def show_groups():
    show_page(groups_page)
    for widget in groups_page.winfo_children():
        widget.destroy()
    title = ctk.CTkLabel(
        groups_page,
        text="👥 Organization Groups",
        font=("Segoe UI", 36, "bold")
    )
    title.pack(pady=25)
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT department
    FROM employees
    ORDER BY department
    """)
    departments = cursor.fetchall()
    scroll_frame = ctk.CTkScrollableFrame(
        groups_page,
        width=1100,
        height=650,
        fg_color="transparent"
    )
    scroll_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )
    for dept in departments:
        department_name = dept[0]
        dropdown_frame = ctk.CTkFrame(
            scroll_frame,
            fg_color="#1e293b",
            corner_radius=12
        )
        dropdown_frame.pack(
            fill="x",
            padx=20,
            pady=12
        )
        employee_container = ctk.CTkFrame(
            dropdown_frame,
            fg_color="#0f172a"
        )
        expanded = False
        def toggle_dropdown(
            frame=employee_container
        ):
            if frame.winfo_ismapped():
                frame.pack_forget()
            else:
                frame.pack(
                    fill="x",
                    padx=20,
                    pady=(0, 15)
                )
        dept_button = ctk.CTkButton(
            dropdown_frame,
            text=f"🏢   {department_name} Department",
            height=60,
            font=("Segoe UI", 24, "bold"),
            fg_color="#1e293b",
            hover_color="#334155",
            anchor="w",
            command=toggle_dropdown
        )
        dept_button.pack(
            fill="x",
            padx=10,
            pady=10
        )
        cursor.execute("""
        SELECT employee_id, name
        FROM employees
        WHERE department = ?
        ORDER BY name
        """, (department_name,))
        employees = cursor.fetchall()
        for emp in employees:
            emp_id = emp[0]
            emp_name = emp[1]
            emp_label = ctk.CTkLabel(
                employee_container,
                text=f"•  {emp_name}    (ID: {emp_id})",
                font=("Arial", 20),
                anchor="w"
            )
            emp_label.pack(
                anchor="w",
                padx=30,
                pady=8
            )
    conn.close()
groups_btn = ctk.CTkButton(
    sidebar,
    text="👥 Groups",
    width=220,
    height=55,
    font=("Arial", 20),
    fg_color="#7c3aed",
    hover_color="#6d28d9",
    corner_radius=12,
    command=show_groups
)
groups_btn.pack(pady=12)
reports_btn = ctk.CTkButton(
    sidebar,
    text="📄 Reports",
    width=220,
    height=45,
    font=("Arial", 18),
    command=lambda: show_page(reports_page)
)
reports_btn.pack(pady=12)
leave_btn = ctk.CTkButton(
    sidebar,
    text="🏖 Leave Management",
    width=220,
    height=45,
    font=("Arial", 18),
    command=lambda: show_page(leave_page)
)
leave_btn.pack(pady=12)
settings_btn = ctk.CTkButton(
    sidebar,
    text="⚙ Settings",
    width=220,
    height=45,
    font=("Arial", 18),
    command=lambda: show_page(settings_page)
)
settings_btn.pack(pady=12)
payroll_btn = ctk.CTkButton(
    sidebar,
    text="💰 Payroll",
    width=220,
    height=45,
    font=("Arial", 18),
    command=lambda: show_page(payroll_page)
)
payroll_btn.pack(pady=12)
def show_visitor_dashboard():
    show_page(visitor_page)
    for widget in visitor_page.winfo_children():
        widget.destroy()
    title = ctk.CTkLabel(
        visitor_page,
        text="Visitor Management System",
        font=("Segoe UI", 36, "bold")
    )
    title.pack(
        pady=20
    )
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM visitors"
    )
    total_visitors = cursor.fetchone()[0]
    conn.close()
    analytics_frame = ctk.CTkFrame(
        visitor_page
    )
    analytics_frame.pack(
        fill="x",
        padx=20,
        pady=10
    )
    card = ctk.CTkFrame(
        analytics_frame,
        width=200,
        height=100
    )
    card.pack(
        side="left",
        padx=10
    )
    ctk.CTkLabel(
        card,
        text="Total Visitors"
    ).pack()
    ctk.CTkLabel(
        card,
        text=str(total_visitors),
        font=("Arial",30,"bold")
    ).pack()
    main_frame = ctk.CTkFrame(
        visitor_page,
        fg_color="transparent"
    )
    main_frame.pack(
        fill="both",
        expand=True
    )
    sidebar_frame = ctk.CTkFrame(
    main_frame,
        width=250,
        corner_radius=12,
        fg_color="#111827"
    )
    sidebar_frame.pack(
        side="left",
        fill="y",
        padx=20,
        pady=20
    )
    sidebar_frame.pack_propagate(False)
    content_frame = ctk.CTkFrame(
        main_frame,
        corner_radius=12
    )
    content_frame.pack(
        side="right",
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )
    menu_title = ctk.CTkLabel(
        sidebar_frame,
        text="Visitor Menu",
        font=("Segoe UI", 28, "bold")
    )
    menu_title.pack(
        pady=25
    )
    sections = [
        "📝 New Registration",
        "📋 Visitor Records",
        "✅ Whitelist",
        "⛔ Blacklist",
        "📥 Check-In",
        "📤 Check-Out"
    ]
    def open_visitor_records():
        for widget in content_frame.winfo_children():
            widget.destroy()
        title = ctk.CTkLabel(
            content_frame,
            text="Visitor Records",
            font=("Segoe UI", 32, "bold")
        )
        title.pack(pady=20)
        def export_visitors():
            conn = sqlite3.connect(
                "database/chronosface.db"
            )
            cursor = conn.cursor()
            cursor.execute("""
            SELECT *
            FROM visitors
            """)
            data = cursor.fetchall()
            conn.close()
            with open(
                "visitor_report.csv",
                "w",
                newline=""
            ) as file:
                writer = csv.writer(file)
                writer.writerows(data)
            messagebox.showinfo(
                "Success",
                "Report Exported"
            )
        ctk.CTkButton(
            content_frame,
            text="Export Report",
            command=export_visitors
        ).pack(pady=10)
        search_entry = ctk.CTkEntry(
            content_frame,
            width=350,
            height=40,
            placeholder_text="Search Visitor"
        )
        search_entry.pack(pady=10)
        table_container = ctk.CTkScrollableFrame(
            content_frame,
            width=1200,
            height=600,
            fg_color="#1f2937"
        )
        def search_visitor(event):
            keyword = search_entry.get()
            print(keyword)
        search_entry.bind(
            "<KeyRelease>",
            search_visitor
        )
        table_container.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )
        conn = sqlite3.connect(
            "database/chronosface.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            photo_path,
            name,
            company,
            purpose,
            host_employee,
            visit_date,
            checkin_time,
            checkout_time,
            status
        FROM visitors
        ORDER BY visitor_id DESC
        """)

        visitors = cursor.fetchall()

        conn.close()
        headers = [
            "Photo",
            "Name",
            "Company",
            "Purpose",
            "Host",
            "Visit Date",
            "Check-In",
            "Check-Out",
            "Status"
        ]

        for col, header in enumerate(headers):

            header_label = ctk.CTkLabel(
                table_container,
                text=header,
                font=("Arial", 16, "bold"),
                text_color="#38bdf8",
                width=70
            )
            header_label.grid(
                row=0,
                column=col,
                padx=5,
                pady=15
            )
        for row_num, visitor in enumerate(visitors, start=1):

            for col_num, value in enumerate(visitor):

                if value is None or value == "":
                    value = "-"
                if col_num == 0:
                    try:
                        image = Image.open(value)

                        image = image.resize((60, 60))

                        photo = ctk.CTkImage(
                            light_image=image,
                            dark_image=image,
                            size=(60, 60)
                        )

                        photo_label = ctk.CTkLabel(
                            table_container,
                            text="",
                            image=photo
                        )

                        photo_label.image = photo

                        photo_label.grid(
                            row=row_num,
                            column=col_num,
                            padx=5,
                            pady=10
                        )

                    except:
                        photo_label = ctk.CTkLabel(
                            table_container,
                            text="No Photo"
                        )

                        photo_label.grid(
                            row=row_num,
                            column=col_num,
                            padx=5,
                            pady=10
                        )

                    continue
                text_color = "white"

                if value == "Checked-In":
                    text_color = "#22c55e"

                elif value == "Checked-Out":
                    text_color = "#ef4444"

                value_label = ctk.CTkLabel(
                    table_container,
                    text=str(value),
                    font=("Arial", 14),
                    width=90,
                    text_color=text_color
                )

                value_label.grid(
                    row=row_num,
                    column=col_num,
                    padx=5,
                    pady=12
                )
    def open_registration():
        for widget in content_frame.winfo_children():
            widget.destroy()
        title = ctk.CTkLabel(
            content_frame,
            text="New Visitor Registration",
            font=("Segoe UI", 32, "bold")
        )
        title.pack(
            pady=20
        )
        form_frame = ctk.CTkScrollableFrame(
            content_frame,
            width=900,
            height=650
        )
        form_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        visitor_name = ctk.CTkEntry(
            form_frame,
            width=400,
            height=45,
            placeholder_text="Visitor Name"
        )
        visitor_name.pack(pady=15)
        visitor_phone = ctk.CTkEntry(
            form_frame,
            width=400,
            height=45,
            placeholder_text="Phone Number"
        )
        visitor_phone.pack(pady=15)
        visitor_email = ctk.CTkEntry(
            form_frame,
            width=400,
            height=45,
            placeholder_text="Email"
        )
        visitor_email.pack(pady=15)
        visitor_company = ctk.CTkEntry(
            form_frame,
            width=400,
            height=45,
            placeholder_text="Company"
        )
        visitor_company.pack(pady=15)
        purpose_entry = ctk.CTkEntry(
            form_frame,
            width=400,
            height=45,
            placeholder_text="Visit Purpose"
        )
        purpose_entry.pack(pady=15)
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        cursor.execute("""
        SELECT name
        FROM employees
        """)
        employees = cursor.fetchall()
        conn.close()
        employee_names = [
            emp[0]
            for emp in employees
        ]
        host_dropdown = ctk.CTkComboBox(
            form_frame,
            values=employee_names,
            width=400,
            height=45
        )
        host_dropdown.pack(pady=15)
        host_dropdown.set(
            "Select Host Employee"
        )
        def capture_visitor_face():
            visitor_name_text = (
                visitor_name.get().strip()
            )
            if visitor_name_text == "":
                messagebox.showerror(
                    "Error",
                    "Enter Visitor Name First"
                )
                return
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.putText(
                    frame,
                    "Press S to Save Face",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                cv2.imshow(
                    "Visitor Face Capture",
                    frame
                )
                key = cv2.waitKey(1)
                if key == ord("s"):
                    os.makedirs(
                        "visitor_faces",
                        exist_ok=True
                    )
                    image_path = (
                        f"visitor_faces/"
                        f"{visitor_name_text}.jpg"
                    )
                    cv2.imwrite(
                        image_path,
                        frame
                    )
                    messagebox.showinfo(
                        "Success",
                        "Visitor Face Captured"
                    )
                    cap.release()
                    cv2.destroyAllWindows()
                    return image_path
                elif key == ord("q"):
                    break
            cap.release()
            cv2.destroyAllWindows()
            return None
        capture_btn = ctk.CTkButton(
            form_frame,
            text="📸 Capture Visitor Face",
            width=300,
            height=50,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=capture_visitor_face
        )
        capture_btn.pack(
            pady=20
        )
        def save_visitor():
            if visitor_name.get().strip() == "":
                messagebox.showerror(
                    "Error",
                    "Visitor Name Required"
                )
                return
            if visitor_phone.get().strip() == "":
                messagebox.showerror(
                    "Error",
                    "Phone Number Required"
                )
                return
            photo_path = (
                f"visitor_faces/"
                f"{visitor_name.get().strip()}.jpg"
            )
            conn = sqlite3.connect("database/chronosface.db")
            cursor = conn.cursor()
            phone = visitor_phone.get().strip()
            cursor.execute("""
            SELECT *
            FROM visitor_blacklist
            WHERE phone=?
            """, (phone,))

            blocked = cursor.fetchone()

            if blocked:
                messagebox.showerror(
                    "Blocked Visitor",
                    "This visitor is blacklisted and cannot register."
                )
                conn.close()
                return
            cursor.execute("""
            INSERT INTO visitors (
                name,
                phone,
                email,
                company,
                purpose,
                host_employee,
                visit_date,
                checkin_time,
                checkout_time,
                status,
                photo_path
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                visitor_name.get(),
                visitor_phone.get(),
                visitor_email.get(),
                visitor_company.get(),
                purpose_entry.get(),
                host_dropdown.get(),
                datetime.now().strftime("%Y-%m-%d"),
                "",
                "",
                "Registered",
                photo_path
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo(
                "Success",
                "Visitor Registered Successfully"
            )
            print("Visitor Saved")
        register_btn = ctk.CTkButton(
            form_frame,
            text="✅ Register Visitor",
            width=350,
            height=55,
            font=("Arial", 20, "bold"),
            fg_color="#15803d",
            hover_color="#166534",
            command=save_visitor
        )
        register_btn.pack(
            pady=30
        )
    def visitor_checkin():
            import cv2
            import sqlite3
            import os
            import numpy as np
            from datetime import datetime
            from tkinter import messagebox
            conn = sqlite3.connect(
                "database/chronosface.db"
            )
            cursor = conn.cursor()
            cursor.execute("""
            SELECT visitor_id, name, photo_path
            FROM visitors
            """)
            visitors = cursor.fetchall()
            known_faces = []
            visitor_names = []
            visitor_ids = []
            for visitor in visitors:
                visitor_id = visitor[0]
                name = visitor[1]
                image_path = visitor[2]
                if not os.path.exists(image_path):
                    continue
                image = cv2.imread(image_path)
                gray = cv2.cvtColor(
                    image,
                    cv2.COLOR_BGR2GRAY
                )
                face_resized = cv2.resize(
                    gray,
                    (200, 200)
                )
                known_faces.append(face_resized)
                visitor_names.append(name)
                visitor_ids.append(visitor_id)
            cap = cv2.VideoCapture(0)
            face_detector = cv2.CascadeClassifier(
                cv2.data.haarcascades +
                "haarcascade_frontalface_default.xml"
            )
            recognized = False
            while True:
                ret, frame = cap.read()
                gray = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2GRAY
                )
                faces = face_detector.detectMultiScale(
                    gray,
                    1.3,
                    5
                )
                for (x, y, w, h) in faces:
                    face = gray[y:y+h, x:x+w]
                    try:
                        face_resized = cv2.resize(
                            face,
                            (200, 200)
                        )
                    except:
                        continue
                    best_match = None
                    best_score = 999999
                    for i, known_face in enumerate(known_faces):
                        diff = np.sum(
                            cv2.absdiff(
                                known_face,
                                face_resized
                            )
                        )
                        if diff < best_score:
                            best_score = diff
                            best_match = i
                    print("Best Score:", best_score)        
                    if best_match is not None and best_score < 15000000:
                        visitor_name = visitor_names[best_match]
                        visitor_id = visitor_ids[best_match]
                        current_time = datetime.now().strftime(
                            "%H:%M:%S"
                        )
                        from datetime import datetime
                        current_time = datetime.now().strftime("%H:%M:%S")
                        cursor.execute("""
                            UPDATE visitors
                            SET
                                status = 'Checked-In',
                                checkin_time = ?
                            WHERE name = ?
                        """, (current_time, visitor_name))
                        conn.commit()
                        cv2.rectangle(
                            frame,
                            (x, y),
                            (x+w, y+h),
                            (0, 255, 0),
                            2
                        )
                        cv2.putText(
                            frame,
                            f"Welcome {visitor_name}",
                            (x, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 255, 0),
                            2
                        )
                        recognized = True
                        cv2.destroyAllWindows()
                        messagebox.showinfo(
                            "Success",
                            f"{visitor_name} Checked-In Successfully"
                        )
                        break
                    else:
                        cv2.putText(
                            frame,
                            "Visitor Not Recognized",
                            (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 0, 255),
                            2
                        )
                cv2.imshow(
                    "Visitor Check-In",
                    frame
                )
                if recognized:
                    break
                if cv2.waitKey(1) == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()
            conn.close()
    def visitor_checkout():
            conn = sqlite3.connect(
                "database/chronosface.db"
            )
            cursor = conn.cursor()
            cursor.execute("""
            SELECT
                visitor_id,
                name
            FROM visitors
            WHERE status='Checked-In'
            """)
            visitors = cursor.fetchall()
            if len(visitors) == 0:
                messagebox.showinfo(
                    "Info",
                    "No Checked-In Visitors"
                )
                return
            checkout_window = ctk.CTkToplevel(app)
            checkout_window.title(
                "Visitor Check-Out"
            )
            checkout_window.geometry("400x300")
            visitor_names = [
                visitor[1]
                for visitor in visitors
            ]
            dropdown = ctk.CTkComboBox(
                checkout_window,
                values=visitor_names,
                width=250
            )
            dropdown.pack(pady=40)
            def confirm_checkout():
                selected_name = dropdown.get()
                checkout_time = datetime.now().strftime(
                    "%H:%M:%S"
                )
                cursor.execute("""
                UPDATE visitors
                SET
                    status=?,
                    checkout_time=?
                WHERE name=?
                """, (
                    "Checked-Out",
                    checkout_time,
                    selected_name
                ))
                conn.commit()
                messagebox.showinfo(
                    "Success",
                    f"{selected_name} Checked-Out"
                )
                checkout_window.destroy()
            btn = ctk.CTkButton(
                checkout_window,
                text="Confirm Check-Out",
                command=confirm_checkout
            )   
            btn.pack(pady=20)
    def open_whitelist():
        for widget in content_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            content_frame,
            text="Whitelist Visitors",
            font=("Segoe UI", 32, "bold")
        )
        title.pack(pady=20)
        search_entry = ctk.CTkEntry(
            content_frame,
            width=300,
            placeholder_text="Search Visitor..."
        )
        search_entry.pack(pady=5)
        def add_to_whitelist():
            win = ctk.CTkToplevel(app)
            win.geometry("400x350")
            win.focus()
            win.grab_set()
            win.lift()
            win.attributes("-topmost", True)
            win.after(100, lambda: win.attributes("-topmost", False))
            win.title("Add Visitor")
            name = ctk.CTkEntry(
                win,
                placeholder_text="Visitor Name"
            )
            name.pack(pady=10)
            phone = ctk.CTkEntry(
                win,
                placeholder_text="Phone"
            )
            phone.pack(pady=10)
            company = ctk.CTkEntry(
                win,
                placeholder_text="Company"
            )
            company.pack(pady=10)
            def save():
                conn = sqlite3.connect(
                        "database/chronosface.db"
                    )
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO visitor_whitelist
                (
                    visitor_name,
                    phone,
                    company
                    )
                VALUES
                (?, ?, ?)
                """,
                (
                    name.get(),
                    phone.get(),
                    company.get()
                    ))
                conn.commit()
                conn.close()
                messagebox.showinfo(
                        "Success",
                        "Visitor Added"
                    )
                win.destroy()
                open_whitelist()
            ctk.CTkButton(
                win,
                text="Save",
                command=save
                ).pack(pady=20) 
        ctk.CTkButton(
            content_frame,
            text="Add Visitor To Whitelist",
            command=add_to_whitelist
        ).pack(pady=10)
        conn = sqlite3.connect(
            "database/chronosface.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
            SELECT visitor_name,
            phone,
            company
            FROM visitor_whitelist
        """)

        records = cursor.fetchall()

        conn.close()

        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#1f2937",
            foreground="white",
            fieldbackground="#1f2937",
            rowheight=35
        )

        style.configure(
            "Treeview.Heading",
            background="#2563eb",
            foreground="white",
            font=("Arial", 12, "bold")
        )
        table = ttk.Treeview(
            content_frame,
            columns=(
                "Name",
                "Phone",
                "Company"
            ),
            show="headings"
        )
        table.heading(
            "Name",
            text="Name"
        )
        table.heading(
            "Phone",
            text="Phone"
        )
        table.heading(
            "Company",
            text="Company"
        )
        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        def search_whitelist(event=None):
            keyword = search_entry.get().lower()
            for item in table.get_children():
                table.delete(item)
            conn = sqlite3.connect(
                "database/chronosface.db"
            )
            cursor = conn.cursor()
            cursor.execute("""
            SELECT
                visitor_name,
                phone,
                company
            FROM visitor_whitelist
            WHERE visitor_name LIKE ?
            """, (f"%{keyword}%",))
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                table.insert("", "end", values=row)
        search_entry.bind(
            "<KeyRelease>",
            search_whitelist
        )
        for row in records:
            table.insert(
                "",
                "end",
                values=row
            )
        def delete_visitor():
            selected = table.selection()
            if not selected:
                messagebox.showerror(
                    "Error",
                    "Select a visitor first"
                )
                return
            item = table.item(selected)
            phone = item["values"][1]
            conn = sqlite3.connect(
                "database/chronosface.db"
            )
            cursor = conn.cursor()
            cursor.execute("""
            DELETE FROM visitor_whitelist
            WHERE phone = ?
            """, (phone,))
            conn.commit()
            conn.close()
            messagebox.showinfo(
                "Success",
                "Visitor Deleted"
            )
            open_whitelist()
        ctk.CTkButton(
            content_frame,
            text="Delete Selected Visitor",
            fg_color="red",
            hover_color="darkred",
            command=delete_visitor
        ).pack(pady=10)
    def open_blacklist():
        for widget in content_frame.winfo_children():
            widget.destroy()

        title = ctk.CTkLabel(
            content_frame,
            text="Blacklist Visitors",
            font=("Segoe UI", 32, "bold")
        )
        title.pack(pady=20)
        search_entry = ctk.CTkEntry(
            content_frame,
            width=300,
            placeholder_text="Search Visitor..."
        )
        search_entry.pack(pady=5)
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#1f2937",
            foreground="white",
            fieldbackground="#1f2937",
            rowheight=35
        )
        style.configure(
            "Treeview.Heading",
            background="#2563eb",
            foreground="white",
            font=("Arial", 12, "bold")
        )
        table = ttk.Treeview(
            content_frame,
            columns=(
                "Name",
                "Phone",
                "Company"
            ),
            show="headings"
        )
        def add_blacklisted_visitor():
            win = ctk.CTkToplevel(app)
            win.geometry("400x350")
            win.focus()
            win.grab_set()
            win.lift()
            win.attributes("-topmost", True)
            win.after(100, lambda: win.attributes("-topmost", False))
            name = ctk.CTkEntry(
                win,
                placeholder_text="Visitor Name"
            )
            name.pack(pady=10)
            phone = ctk.CTkEntry(
                win,
                placeholder_text="Phone"
            )
            phone.pack(pady=10)
            reason = ctk.CTkEntry(
                win,
                placeholder_text="Reason"
            )
            reason.pack(pady=10)
            def save():
                conn = sqlite3.connect(
                    "database/chronosface.db"
                )
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO visitor_blacklist
                (
                    visitor_name,
                    phone,
                    reason
                )
                VALUES
                (?, ?, ?)
                """,
                (
                    name.get(),
                    phone.get(),
                    reason.get()
                ))
                conn.commit()
                conn.close()
                messagebox.showinfo(
                    "Success",
                    "Visitor Blacklisted"
                )
                win.destroy()
                open_blacklist()
            ctk.CTkButton(
                win,
                text="Save",
                command=save
            ).pack(pady=20)
        ctk.CTkButton(
            content_frame,
            text="Add Visitor To Blacklist",
            command=add_blacklisted_visitor
        ).pack(pady=10)
        def search_blacklist(event=None):
            keyword = search_entry.get().lower()
            for item in table.get_children():
                table.delete(item)
            conn = sqlite3.connect(
                "database/chronosface.db"
            )
            cursor = conn.cursor()
            cursor.execute("""
            SELECT
                visitor_name,
                phone,
                reason
            FROM visitor_blacklist
            WHERE visitor_name LIKE ?
            """, (f"%{keyword}%",))
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                table.insert("", "end", values=row)
        search_entry.bind(
            "<KeyRelease>",
            search_blacklist
        )    
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT visitor_name,
            phone,
            reason
            FROM visitor_blacklist
        """)
        records = cursor.fetchall()
        conn.close()
        table = ttk.Treeview(
            content_frame,
            columns=(
                "Name",
                "Phone",
                "Reason"
            ),
            show="headings"
        )
        table.heading(
            "Name",
            text="Name"
        )
        table.heading(
            "Phone",
            text="Phone"
        )
        table.heading(
            "Reason",
            text="Reason"
        )
        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )
        def delete_blacklisted():
            selected = table.selection()
            if not selected:
                return
            item = table.item(selected)
            phone = item["values"][1]
            conn = sqlite3.connect(
                "database/chronosface.db"
            )
            cursor = conn.cursor()
            cursor.execute("""
            DELETE FROM visitor_blacklist
            WHERE phone=?
            """, (phone,))
            conn.commit()
            conn.close()
            open_blacklist()
        ctk.CTkButton(
            content_frame,
            text="Delete Selected Visitor",
            fg_color="red",
            command=delete_blacklisted
        ).pack(pady=10)
        for row in records:
            table.insert(
                "",
                "end",
                values=row
            )
    for section in sections:
        if section == "📝 New Registration":
            btn_command = open_registration
        elif section == "📋 Visitor Records":
            btn_command = open_visitor_records
        elif section == "✅ Whitelist":
            btn_command = open_whitelist
        elif section == "⛔ Blacklist":
            btn_command = open_blacklist
        elif section == "📥 Check-In":
            btn_command = visitor_checkin
        elif section == "📤 Check-Out":
            btn_command = visitor_checkout
        else:
            btn_command = None
        btn = ctk.CTkButton(
            sidebar_frame,
            text=section,
            width=220,
            height=50,
            font=("Arial", 18),
            fg_color="#1f2937",
            hover_color="#374151",
            command=btn_command
        )
        btn.pack(
            pady=10,
            padx=10
        )
    welcome = ctk.CTkLabel(
        content_frame,
        text="Select a Visitor Management Option",
        font=("Arial", 30)
    )
    welcome.pack(
        pady=200
    )
    info = ctk.CTkLabel(
            content_frame,
            text="Blocked Visitors",
            font=("Arial", 20)
        )
    info.pack(pady=10)
visitor_btn = ctk.CTkButton(
    sidebar,
    text="🧑 Visitor Management",
    width=220,
    height=45,
    corner_radius=12,
    font=("Segoe UI", 18, "bold"),
    fg_color="#0f766e",
    hover_color="#115e59",
    command=show_visitor_dashboard
)
visitor_btn.pack(pady=12)
def show_monthly_report():
    report_window = ctk.CTkToplevel(app)
    report_window.title("Monthly Attendance Report")
    report_window.geometry("1000x650")
    report_window.focus()
    report_window.grab_set()
    title = ctk.CTkLabel(
        report_window,
        text="📊 Monthly Attendance Report",
        font=("Segoe UI", 36, "bold")
    )
    title.pack(pady=20)
    report_box = ctk.CTkTextbox(
        report_window,
        width=900,
        height=500,
        font=("Consolas", 18)
    )
    report_box.pack(pady=20)
    report_box.insert(
        "end",
        "ID       Name          Present   Total Hours\n"
    )
    report_box.insert(
        "end",
        "------------------------------------------------------\n"
    )
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        employee_id,
        name,
        COUNT(*)
    FROM attendance
    GROUP BY employee_id
    """)
    records = cursor.fetchall()
    for row in records:
        employee_id = row[0]
        employee_name = row[1]
        present_days = row[2]
        cursor.execute("""
        SELECT working_hours
        FROM attendance
        WHERE employee_id = ?
        """, (employee_id,))
        work_records = cursor.fetchall()
        total_seconds = 0
        for item in work_records:
            try:
                h, m, s = map(
                    int,
                    item[0].split(":")
                )
                total_seconds += (
                    h * 3600 +
                    m * 60 +
                    s
                )
            except:
                pass
        total_hours = round(
            total_seconds / 3600,
            2
        )
        report_box.insert(
            "end",
            f"{employee_id:<10}"
            f"{employee_name:<15}"
            f"{present_days:<10}"
            f"{total_hours} hrs\n"
        )
    conn.close()
    report_box.configure(
        state="disabled"
    )
def show_about():
    messagebox.showinfo(
        "About ChronosFace AI",
        
        "ChronosFace AI\n\n"
        "Smart Face Recognition Attendance System\n\n"
        "Developed Using:\n"
        "- Python\n"
        "- CustomTkinter\n"
        "- SQLite\n"
        "- OpenCV\n"
        "- Face Recognition"
    )
report_btn = ctk.CTkButton(
    sidebar,
    text="📊 Monthly Report",
    width=220,
    height=55,
    font=("Arial", 20),
    fg_color="#0f766e",
    hover_color="#115e59",
    command=show_monthly_report
)
report_btn.pack(pady=12)
def logout():
    app.destroy()
    subprocess.Popen([
        sys.executable,
        "login.py"
    ])
logout_btn = ctk.CTkButton(
    sidebar,
    text="Logout",
    width=220,
    height=45,
    font=("Arial", 18),
    fg_color="red",
    hover_color="darkred",
    command=logout
)
logout_btn.pack(
    side="bottom",
    pady=35
)
dashboard_title = ctk.CTkLabel(
    dashboard_page,
    text="Admin Dashboard",
    font=("Segoe UI", 42, "bold")
)
dashboard_title.pack(
    anchor="nw",
    padx=30,
    pady=30
)
def update_clock():
    current_time = strftime(
        "%d-%m-%Y  %H:%M:%S"
    )
    clock_label.configure(
        text=current_time
    )
    clock_label.after(
        1000,
        update_clock
    )
clock_label = ctk.CTkLabel(
    dashboard_page,
    font=("Arial", 20, "bold"),
    text_color="cyan"
)
clock_label.place(
    x=1000,
    y=70
)
update_clock()
def menu_action(choice):
    if choice == "Profile":
        messagebox.showinfo(
        "Admin Profile",
        "Admin Panel Access"
    )
    elif choice == "Switch to Employee":
        app.destroy()
        subprocess.Popen([
            sys.executable,
            "employee_login.py"
        ])
    elif choice == "Switch to HR":
        app.destroy()
        subprocess.Popen([
            sys.executable,
            "hr_dashboard.py"
        ])
    elif choice == "Logout":
        app.destroy()
        subprocess.Popen([
            sys.executable,
            "login.py"
        ])
    elif choice == "Change Password":
        open_change_password("admin")
profile_menu = ctk.CTkOptionMenu(
    dashboard_page,
    values=[
        "Profile",
        "Change Password",
        "Switch to Employee",
        "Switch to HR",
        "Logout"
    ],
    command=menu_action,
    width=220,
    height=40,
    font=("Arial", 16)
)
profile_menu.place(
    relx=0.82,
    y=35
)
cards_frame = ctk.CTkFrame(
    dashboard_page,
    fg_color="transparent"
)
cards_frame.pack(
    pady=20
)
card1 = ctk.CTkFrame(
    cards_frame,
    width=260,
    height=220,
    fg_color="#1e293b"
)
card1.pack(
    side="left",
    padx=20
)
card1.pack_propagate(False)
card1_title = ctk.CTkLabel(
    card1,
    text="Total Employees",
    font=("Arial", 24, "bold")
)
card1_title.pack(pady=20)
card1_value = ctk.CTkLabel(
    card1,
    text="0",
    font=("Arial", 50, "bold"),
    text_color="green"
)
card1_value.pack()
card2 = ctk.CTkFrame(
    cards_frame,
    width=260,
    height=220,
    fg_color="#064e3b"
)
card2.pack(
    side="left",
    padx=20
)
card2.pack_propagate(False)
card2_title = ctk.CTkLabel(
    card2,
    text="Present Today",
    font=("Arial", 24, "bold")
)
card2_title.pack(pady=20)
card2_value = ctk.CTkLabel(
    card2,
    text="0",
    font=("Arial", 50, "bold"),
    text_color="cyan"
)
card2_value.pack()
card3 = ctk.CTkFrame(
    cards_frame,
    width=260,
    height=220,
    fg_color="#064e3b"
)
card3.pack(
    side="left",
    padx=20
)
card3.pack_propagate(False)
card3_title = ctk.CTkLabel(
    card3,
    text="Absent",
    font=("Arial", 24, "bold")
)
card3_title.pack(pady=20)
card3_value = ctk.CTkLabel(
    card3,
    text="0",
    font=("Arial", 50, "bold"),
    text_color="red"
)
card3_value.pack()
employees_title = ctk.CTkLabel(
    employees_page,
    text="Employee Management",
    font=("Segoe UI", 42, "bold")
)
employees_title.pack(pady=40)
buttons_frame = ctk.CTkFrame(
    employees_page,
    fg_color="transparent"
)
buttons_frame.pack(pady=20)
add_btn = ctk.CTkButton(
    buttons_frame,
    text="Add Employee",
    width=200,
    height=50,
    font=("Arial", 18),
    command=open_add_employee
)
add_btn.grid(
    row=0,
    column=0,
    padx=20,
    pady=20
)
modify_btn = ctk.CTkButton(
    buttons_frame,
    text="Modify Employee",
    width=200,
    height=50,
    font=("Arial", 18),
    command=open_modify_employee
)
modify_btn.grid(
    row=0,
    column=1,
    padx=20,
    pady=20
)
delete_btn = ctk.CTkButton(
    buttons_frame,
    text="Delete Employee",
    width=200,
    height=50,
    font=("Arial", 18),
    fg_color="red",
    hover_color="darkred",
    command=admin_delete_login
)
delete_btn.grid(
    row=0,
    column=2,
    padx=20,
    pady=20
)
change_photo_btn = ctk.CTkButton(
    buttons_frame,
    text="Change Photo",
    width=200,
    height=50,
    font=("Arial", 18),
    fg_color="#9333ea",
    hover_color="#7e22ce",
    command=open_change_photo
)
change_photo_btn.grid(
    row=0,
    column=3,
    padx=20,
    pady=20
)
employee_table = ctk.CTkTextbox(
    employees_page,
    width=1000,
    height=400,
    font=("Consolas", 18)
)
employee_table.pack(pady=30)
def search_employee():
    keyword = search_entry.get()
    employee_table.configure(state="normal")
    employee_table.delete("1.0", "end")
    employee_table.insert(
        "end",
        "Search Results\n\n"
    )
    employee_table.insert(
        "end",
        "ID       Name            Department\n"
    )
    employee_table.insert(
        "end",
        "--------------------------------------\n"
    )
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT employee_id, name, department
    FROM employees
    WHERE employee_id LIKE ?
    OR name LIKE ?
    """, (
        f"%{keyword}%",
        f"%{keyword}%"
    ))
    employees = cursor.fetchall()
    conn.close()
    for emp in employees:
        employee_table.insert(
            "end",
            f"{emp[0]:<10}{emp[1]:<18}{emp[2]}\n"
        )
    employee_table.configure(state="disabled")
search_frame = ctk.CTkFrame(
    employees_page,
    fg_color="transparent"
)
search_frame.pack(pady=10)
search_entry = ctk.CTkEntry(
    search_frame,
    width=350,
    height=45,
    placeholder_text="Search Employee ID or Name"
)
search_entry.grid(
    row=0,
    column=0,
    padx=15
)
search_btn = ctk.CTkButton(
    search_frame,
    text="Search",
    width=140,
    height=45,
    font=("Arial", 18),
    command=search_employee
)
search_btn.grid(
    row=0,
    column=1,
    padx=10
)
attendance_box = ctk.CTkTextbox(
    attendance_page,
    width=1200,
    height=500,
    font=("Consolas", 18),
    fg_color="#111111",
    text_color="white"
)
attendance_box.pack(pady=30)
reports_box = ctk.CTkTextbox(
    reports_page,
    width=1100,
    height=500,
    font=("Consolas", 20),
    fg_color="#111111",
    text_color="white"
)
reports_box.pack(pady=30)
def show_attendance_chart():
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT DISTINCT employee_id
    FROM attendance
    """)
    present_records = cursor.fetchall()
    present_count = len(present_records)
    cursor.execute("""
    SELECT COUNT(*)
    FROM employees
    """)
    total_employees = cursor.fetchone()[0]
    absent_count = total_employees - present_count
    conn.close()
    labels = [
        "Present Employees",
        "Absent Employees"
    ]
    values = [
        present_count,
        absent_count
    ]
    colors = [
        "green",
        "red"
    ]
    plt.figure(figsize=(7,7))
    plt.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        colors=colors
    )
    plt.title(
        "Employee Attendance Analytics"
    )
    plt.show()
def show_work_hours_chart():
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        name,
        working_hours
    FROM attendance
    """)
    records = cursor.fetchall()
    conn.close()
    employee_names = []
    work_hours = []
    for row in records:
        name = row[0]
        time_value = row[1]
        try:
            h, m, s = map(int, time_value.split(":"))
            total_hours = h + (m / 60)
        except:
            total_hours = 0
        employee_names.append(name)
        work_hours.append(total_hours)
    plt.figure(figsize=(9,5))
    bars = plt.bar(
        employee_names,
        work_hours,
        color=[
            "#2563eb",
            "#16a34a",
            "#dc2626",
            "#ca8a04",
            "#9333ea"
        ]
    )
    plt.xlabel(
        "Employees",
        fontsize=12
    )
    plt.ylabel(
        "Work Hours",
        fontsize=12
    )
    plt.title(
        "Employee Work Hours Analysis",
        fontsize=16,
        fontweight="bold"
    )
    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.5
    )
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2,
            height,
            f"{height:.1f}h",
            ha="center",
            va="bottom",
            fontsize=10
        )
    plt.tight_layout()
    plt.show()
def export_attendance_report():
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        employee_id,
        name,
        date,
        clock_in,
        clock_out,
        total_break,
        working_hours
    FROM attendance
    """)
    records = cursor.fetchall()
    conn.close()
    os.makedirs(
        "attendance/reports",
        exist_ok=True
    )
    filename = datetime.now().strftime(
        "attendance_report_%Y%m%d_%H%M%S.csv"
    )
    filepath = os.path.join(
        "attendance/reports",
        filename
    )
    with open(
        filepath,
        "w",
        newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            "Employee ID",
            "Name",
            "Date",
            "Clock In",
            "Clock Out",
            "Break",
            "Working Hours"
        ])
        writer.writerows(records)
    messagebox.showinfo(
        "Export Successful",
        f"Report Saved:\n{filepath}"
    )
export_btn = ctk.CTkButton(
    reports_page,
    text="Export Attendance Excel",
    width=250,
    height=50,
    font=("Arial", 18),
    fg_color="green",
    hover_color="darkgreen",
    command=export_attendance_report
)
export_btn.pack(pady=15)
chart_btn = ctk.CTkButton(
    reports_page,
    text="Show Attendance Chart",
    width=250,
    height=50,
    font=("Arial", 18),
    fg_color="#2563eb",
    hover_color="#1d4ed8",
    command=show_attendance_chart
)
chart_btn.pack(pady=10)
work_chart_btn = ctk.CTkButton(
    reports_page,
    text="Show Work Hours Chart",
    width=250,
    height=50,
    font=("Arial", 18),
    fg_color="#15803d",
    hover_color="#166534",
    command=show_work_hours_chart
)
work_chart_btn.pack(pady=10)
payroll_title = ctk.CTkLabel(
    payroll_page,
    text="💰 Payroll Management",
    font=("Segoe UI", 42, "bold")
)
payroll_title.pack(pady=30)
payroll_box = ctk.CTkTextbox(
    payroll_page,
    width=1100,
    height=500,
    font=("Consolas", 18),
    fg_color="#111111",
    text_color="white"
)
payroll_box.pack(pady=20)
payroll_box.insert(
    "end",
    "Employee Payroll Details\n\n"
)
payroll_box.insert(
    "end",
    "ID       Name            Salary\n"
)
payroll_box.insert(
    "end",
    "-----------------------------------\n"
)
payroll_box.insert(
    "end",
    "1040     Ruchitha       ₹50,000\n"
)
payroll_box.insert(
    "end",
    "1041     John           ₹45,000\n"
)
payroll_box.insert(
    "end",
    "1042     Tony           ₹40,000\n"
)
employee_options = [
    "1040 - Ruchitha",
    "1041 - John",
    "1042 - Tony"
]
employee_dropdown = ctk.CTkComboBox(
    payroll_page,
    values=employee_options,
    width=350,
    height=50,
    font=("Arial", 18),
    corner_radius=12
)
employee_dropdown.pack(pady=15)
employee_dropdown.set(
    "Select Employee"
)
def create_payslip():
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    selected_employee = (
        employee_dropdown.get()
        )
    employee_id = (
            selected_employee.split(" - ")[0]
        )
    cursor.execute("""
    SELECT
        employee_id,
        name,
        department,
        salary
        FROM employees
        WHERE employee_id = ?
        """, (employee_id,))
    employee =  cursor.fetchone()
    conn.close()
    if employee:
        employee_id = employee[0]
        employee_name = employee[1]
        department = employee[2]
        salary = employee[3]
        file_path = generate_payslip(
            employee_id,
            employee_name,
            department,
            salary
        )
        os.startfile(file_path)
        messagebox.showinfo(
            "Success",
            "Payslip Generated Successfully"
        )
    else:
        messagebox.showerror(
            "Error",
            "Employee Not Found"
        )
generate_btn = ctk.CTkButton(
    payroll_page,
    text="📄 Generate Payslip",
    width=300,
    height=55,
    font=("Arial", 20, "bold"),
    fg_color="#2563eb",
    hover_color="#1d4ed8",
    command=create_payslip
)
generate_btn.pack(pady=20)
settings_title = ctk.CTkLabel(
    settings_page,
    text="System Settings",
    font=("Segoe UI", 42, "bold")
)
settings_title.pack(pady=40)
change_password_btn = ctk.CTkButton(
    settings_page,
    text="🔑 Change Admin Password",
    width=320,
    height=55,
    font=("Arial", 20, "bold"),
    fg_color="#2563eb",
    hover_color="#1d4ed8",
    command=lambda: open_change_password("admin")
)
change_password_btn.pack(pady=25)
def backup_database():
    os.makedirs("backup", exist_ok=True)
    shutil.copy(
        "database/chronosface.db",
        "backup/chronosface_backup.db"
    )
    messagebox.showinfo(
        "Success",
        "Database Backup Created"
    )
backup_btn = ctk.CTkButton(
    settings_page,
    text="💾 Backup Database",
    width=320,
    height=55,
    font=("Arial", 20, "bold"),
    fg_color="#15803d",
    hover_color="#166534",
    command=backup_database
)
backup_btn.pack(pady=20)
def import_database():
    file_path = filedialog.askopenfilename(
        title="Select Database File",
        filetypes=[
            ("Database Files", "*.db")
        ]
    )
    if file_path:
        shutil.copy(
            file_path,
            "database/chronosface.db"
        )
        messagebox.showinfo(
            "Success",
            "Database Imported Successfully"
        )
import_btn = ctk.CTkButton(
    settings_page,
    text="📂 Import Database",
    width=320,
    height=55,
    font=("Arial", 20, "bold"),
    fg_color="#0ea5e9",
    hover_color="#0284c7",
    command=import_database
)
import_btn.pack(pady=20)
current_mode = "dark"
def toggle_theme():
    global current_mode
    if current_mode == "dark":
        ctk.set_appearance_mode("light")
        current_mode = "light"
    else:
        ctk.set_appearance_mode("dark")
        current_mode = "dark"
theme_btn = ctk.CTkButton(
    settings_page,
    text="🎨 Toggle Theme",
    width=320,
    height=55,
    font=("Arial", 20, "bold"),
    fg_color="#7c3aed",
    hover_color="#6d28d9",
    command=toggle_theme
)
theme_btn.pack(pady=20)
about_btn = ctk.CTkButton(
    settings_page,
    text="ℹ About System",
    width=320,
    height=55,
    font=("Arial", 20, "bold"),
    fg_color="#ca8a04",
    hover_color="#a16207",
    text_color="black",
    command=show_about
)
about_btn.pack(pady=20)
leave_title = ctk.CTkLabel(
    leave_page,
    text="🏖 Leave Management",
    font=("Segoe UI", 42, "bold")
)
leave_title.pack(pady=30)
leave_box = ctk.CTkTextbox(
    leave_page,
    width=1100,
    height=450,
    font=("Consolas", 18),
    fg_color="#111111",
    text_color="white"
)
leave_box.pack(pady=20)
button_frame = ctk.CTkFrame(
    leave_page,
    fg_color="transparent"
)
button_frame.pack(pady=10)
approve_btn = ctk.CTkButton(
    button_frame,
    text="Approve Leave",
    width=200,
    height=45,
    fg_color="green",
    hover_color="darkgreen",
    font=("Arial", 18),
    command=lambda: update_leave_status("Approved")
)
approve_btn.pack(side="left", padx=20)
reject_btn = ctk.CTkButton(
    button_frame,
    text="Reject Leave",
    width=200,
    height=45,
    fg_color="red",
    hover_color="darkred",
    font=("Arial", 18),
    command=lambda: update_leave_status("Rejected")
)
reject_btn.pack(side="left", padx=20)
def load_attendance_table():
        attendance_box.configure(state="normal")
        attendance_box.delete("1.0", "end")
        attendance_box.insert(
            "end",
            "Attendance History\n\n"
        )
        attendance_box.insert(
            "end",
            "ID      Name           Date         Clock In      Clock Out     Break       Work Hours\n"
        )
        attendance_box.insert(
            "end",
            "--------------------------------------------------------------------------------------\n"
        )
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        cursor.execute("""
        SELECT *
        FROM attendance
        """)
        records = cursor.fetchall()
        conn.close()
        for row in records:
            attendance_box.insert(
                "end",
                f"{row[1]:<8}{row[2]:<15}{row[3]:<13}{row[4]:<14}{row[5]:<14}{row[8]:<12}{row[9]}\n"
            )
        attendance_box.configure(state="disabled")
load_attendance_table()
def load_reports():
    reports_box.configure(state="normal")
    reports_box.delete("1.0", "end")
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM employees"
    )
    total_employees = cursor.fetchone()[0]
    cursor.execute("""
    SELECT COUNT(DISTINCT employee_id)
    FROM attendance
    WHERE date = date('now')
    """)
    present_today = cursor.fetchone()[0]
    absent_today = total_employees - present_today
    cursor.execute("""
    SELECT AVG(
        CAST(substr(working_hours,1,2) AS INTEGER)
    )
    FROM attendance
    """)
    avg_hours = cursor.fetchone()[0]
    if avg_hours is None:
        avg_hours = 0
    reports_box.insert(
        "end",
        "HR Attendance Reports\n\n"
    )
    reports_box.insert(
        "end",
        f"Total Employees      : {total_employees}\n\n"
    )
    reports_box.insert(
        "end",
        f"Present Today        : {present_today}\n\n"
    )
    reports_box.insert(
        "end",
        f"Absent Today         : {absent_today}\n\n"
    )
    reports_box.insert(
        "end",
        f"Average Work Hours   : {round(avg_hours,2)} hrs\n\n"
    )
    reports_box.insert(
        "end",
        "Employee Work Summary\n\n"
    )
    reports_box.insert(
        "end",
        "ID       Name            Work Hours\n"
    )
    reports_box.insert(
        "end",
        "--------------------------------------\n"
    )
    cursor.execute("""
    SELECT employee_id, name, working_hours
    FROM attendance
    """)
    records = cursor.fetchall()
    for row in records:
        reports_box.insert(
            "end",
            f"{row[0]:<10}{row[1]:<18}{row[2]}\n"
        )
    conn.close()
    reports_box.configure(state="disabled")
load_reports()
def load_dashboard_data():
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM employees"
    )
    total_employees = cursor.fetchone()[0]
    cursor.execute("""
    SELECT COUNT(DISTINCT employee_id)
    FROM attendance
    WHERE date = date('now')
    """)
    present_today = cursor.fetchone()[0]
    absent_today = total_employees - present_today
    card1_value.configure(
        text=str(total_employees)
    )
    card2_value.configure(
        text=str(present_today)
    )
    card3_value.configure(
        text=str(absent_today)
    )
    conn.close()
load_dashboard_data()
def load_leave_requests():
    leave_box.configure(state="normal")
    leave_box.delete("1.0", "end")
    leave_box.insert(
        "end",
        "Employee Leave Requests\n\n"
    )
    leave_box.insert(
        "end",
        "ID       Name            Leave Date       Status\n"
    )
    leave_box.insert(
        "end",
        "------------------------------------------------------\n"
    )
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        employee_id,
        name,
        leave_date,
        status
    FROM leaves
    """)
    records = cursor.fetchall()
    conn.close()
    for row in records:
        leave_box.insert(
            "end",
            f"{row[0]:<10}{row[1]:<16}{row[2]:<18}{row[3]}\n"
        )
    leave_box.configure(state="disabled")
load_leave_requests()
def update_leave_status(status):
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        employee_id,
        name
    FROM leaves
    WHERE status = 'Pending'
    LIMIT 1
    """)
    leave_record = cursor.fetchone()
    if leave_record:
        employee_id = leave_record[0]
        employee_name = leave_record[1]
        cursor.execute("""
        SELECT email
        FROM employees
        WHERE employee_id = ?
        """, (employee_id,))
        email_record = cursor.fetchone()
        if email_record:
            employee_email = email_record[0]
            send_email(
                employee_email,
                f"Leave {status}",
                f"""
Hello {employee_name},
Your leave request has been {status}.
Regards,
ChronosFace Admin
"""
            )
    cursor.execute("""
    UPDATE leaves
    SET status = ?
    WHERE status = 'Pending'
    """, (status,))
    conn.commit()
    print("Rows Updated:", cursor.rowcount)
    conn.close()
    messagebox.showinfo(
        "Success",
        f"Leave {status} Successfully"
    )
    leave_box.configure(state="normal")
load_leave_requests()
show_page(dashboard_page)
app.mainloop()