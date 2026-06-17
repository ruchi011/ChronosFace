import customtkinter as ctk
import subprocess
import sys
import requests
from tkinter import messagebox
from admin_dashboard import load_employee_table
from admin_dashboard import load_employee_table
from attendance_export import export_attendance
from profile_window import open_profile
from change_password import open_change_password
from payslip_generator import generate_payslip
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
def load_hr_employees():
    employees_box.delete("1.0", "end")
    employees_box.insert(
        "end",
        "Employee Details\n\n"
    )
    try:
        response = requests.get(
            "http://127.0.0.1:5000/api/employees"
        )
        employees = response.json()
        for emp in employees:
            employees_box.insert(
                "end",
                f"{emp['employee_id']}    "
                f"{emp['employee_name']}    "
                f"{emp['department']}\n"
            )
    except Exception as e:
        employees_box.insert(
            "end",
            f"Error: {e}"
        )
def auto_refresh_hr():
    load_hr_employees()
    app.after(
        3000,
        auto_refresh_hr
    )
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("ChronosFace HR Dashboard")
app.geometry("1400x800")
app.configure(fg_color="#0f172a")
sidebar = ctk.CTkFrame(
    app,
    width=250,
    fg_color="#111827",
    corner_radius=0
)
sidebar.pack(
    side="left",
    fill="y"
)
logo = ctk.CTkLabel(
    sidebar,
    text="ChronosFace",
    font=("Segoe UI", 30, "bold")
)
logo.pack(pady=30)
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
wfh_page = ctk.CTkFrame(main_frame)
payroll_page = ctk.CTkFrame(main_frame)
settings_page = ctk.CTkFrame(main_frame)
leave_page = ctk.CTkFrame(main_frame)
logs_page = ctk.CTkFrame(main_frame)
for frame in (
    dashboard_page,
    employees_page,
    attendance_page,
    reports_page,
    leave_page,
    wfh_page,
    payroll_page,
    settings_page,
    logs_page,
):
    frame.place(
        relwidth=1,
        relheight=1
    )
def show_page(page):
    page.tkraise()
dashboard_btn = ctk.CTkButton(
    sidebar,
    text="📊 Dashboard",
    width=200,
    height=50,
    font=("Arial", 20),
    command=lambda: show_page(dashboard_page)
)
dashboard_btn.pack(pady=10)
employees_btn = ctk.CTkButton(
    sidebar,
    text="👥 Employees",
    width=200,
    height=50,
    font=("Arial", 20),
    command=lambda: show_page(employees_page)
)
employees_btn.pack(pady=10)
attendance_btn = ctk.CTkButton(
    sidebar,
    text="Attendance",
    width=200,
    height=50,
    font=("Arial", 20),
    command=lambda: show_page(attendance_page)
)
attendance_btn.pack(pady=10)
reports_btn = ctk.CTkButton(
    sidebar,
    text="📄 Reports",
    width=200,
    height=50,
    font=("Arial", 20),
    command=lambda: show_page(reports_page)
)
reports_btn.pack(pady=10)
leave_btn = ctk.CTkButton(
    sidebar,
    text="Leave Requests",
    width=200,
    height=50,
    font=("Arial",20),
    command=lambda:
        show_page(leave_page)
)
leave_btn.pack(pady=10)
wfh_btn = ctk.CTkButton(
    sidebar,
    text="Work From Home",
    width=200,
    height=50,
    font=("Arial", 20),
    command=lambda: show_page(wfh_page)
)
wfh_btn.pack(pady=10)
payroll_btn = ctk.CTkButton(
    sidebar,
    text="Payroll",
    width=200,
    height=50,
    font=("Arial", 20),
    command=lambda: show_page(payroll_page)
)
payroll_btn.pack(pady=10)
settings_btn = ctk.CTkButton(
    sidebar,
    text="⚙ Settings",
    width=200,
    height=50,
    font=("Arial", 20),
    command=lambda: show_page(settings_page)
)
settings_btn.pack(pady=10)
logout_btn = ctk.CTkButton(
    sidebar,
    text="Logout",
    width=200,
    height=50,
    font=("Arial", 20, "bold"),
    fg_color="red",
    hover_color="darkred",
    command=lambda: [
        app.destroy(),
        subprocess.Popen([
            sys.executable,
            "login.py"
        ])
    ]
)
logout_btn.pack(
    side="bottom",
    pady=30
)
def menu_action(choice):
    if choice == "Switch to Employee":
        app.destroy()
        subprocess.Popen([
            sys.executable,
            "employee_login.py"
        ])
    elif choice == "Switch to Admin":
        app.destroy()
        subprocess.Popen([
            sys.executable,
            "admin_login.py"
        ])
    elif choice == "Change Password":
        open_change_password("hr")
    elif choice == "Logout":
        app.destroy()
        subprocess.Popen([
            sys.executable,
            "login.py"
        ])
profile_menu = ctk.CTkOptionMenu(
    main_frame,
    values=[
        "Profile",
        "Switch to Employee",
        "Switch to Admin",
        "Change Password",
        "Logout"
    ],
    command=menu_action,
    width=220,
    height=40,
    font=("Arial", 16)
)
profile_menu.place(
    x=1150,
    y=20
)
dashboard_title = ctk.CTkLabel(
    dashboard_page,
    text="HR Dashboard",
    font=("Segoe UI", 42, "bold")
)
dashboard_title.pack(
    anchor="nw",
    pady=20,
    padx=20
)
cards_frame = ctk.CTkFrame(
    dashboard_page,
    fg_color="transparent"
)
cards_frame.pack(
    pady=20
)
conn = sqlite3.connect(
    "database/chronosface.db"
)

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM biometric_data"
)
total_employees = cursor.fetchone()[0]

today = datetime.now().strftime(
    "%Y-%m-%d"
)

cursor.execute("""
SELECT COUNT(*)
FROM attendance
WHERE date=?
""", (today,))
present_today = cursor.fetchone()[0]

absent_today = (
    total_employees
    - present_today
)

cursor.execute("""
SELECT AVG(
CAST(
REPLACE(working_hours,':','.')
AS REAL
))
FROM attendance
""")

avg_hours = cursor.fetchone()[0]

if avg_hours is None:
    avg_hours = 0

conn.close()
def create_card(parent, title, value, color):
    card = ctk.CTkFrame(
        parent,
        width=250,
        height=150,
        corner_radius=20
    )
    card.pack(
        side="left",
        padx=20
    )
    card.pack_propagate(False)
    title_label = ctk.CTkLabel(
        card,
        text=title,
        font=("Arial", 24, "bold")
    )
    title_label.pack(pady=15)
    value_label = ctk.CTkLabel(
        card,
        text=value,
        font=("Segoe UI", 42, "bold"),
        text_color=color
    )
    value_label.pack()
    return card
create_card(
    cards_frame,
    "Total Employees",
    str(total_employees),
    "green"
)
create_card(
    cards_frame,
    "Present Today",
    str(present_today),
    "cyan"
)
create_card(
    cards_frame,
    "Absent",
    str(absent_today),
    "red"
)
create_card(
    cards_frame,
    "Avg Work Hours",
    f"{avg_hours:.1f}",
    "orange"
)
employees_title = ctk.CTkLabel(
    employees_page,
    text="👥 Employees",
    font=("Segoe UI", 42, "bold")
)
employees_title.pack(pady=30)
search_employee = ctk.CTkEntry(
    employees_page,
    width=300,
    height=40,
    placeholder_text="Search Employee"
)
search_employee.pack(pady=10)
employees_box = ctk.CTkTextbox(
    employees_page,
    width=900,
    height=500,
    font=("Consolas", 18)
)
employees_box.pack(pady=20)
search_employee.bind(
    "<KeyRelease>",
    lambda e: load_employee_table()
)
load_hr_employees()
attendance_title = ctk.CTkLabel(
    attendance_page,
    text="Attendance",
    font=("Segoe UI", 42, "bold")
)
attendance_title.pack(pady=30)
attendance_search = ctk.CTkEntry(
    attendance_page,
    placeholder_text="Search Employee"
)
attendance_search.pack(pady=10)
keyword = attendance_search.get()
cursor.execute("""
SELECT
employee_id,
employee_name
FROM attendance
WHERE date=?
AND name LIKE ?
""",
(
today,
f"%{keyword}%"
))
attendance_box = ctk.CTkTextbox(
    attendance_page,
    width=900,
    height=500,
    font=("Consolas", 18)
)
attendance_box.pack(pady=20)
attendance_box.insert(
    "end",
    "Today's Attendance\n\n"
)
def load_attendance_data():

    attendance_box.delete(
        "1.0",
        "end"
    )

    attendance_box.insert(
        "end",
        "Today's Attendance\n\n"
    )

    conn = sqlite3.connect(
        "database/chronosface.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
    employee_id,
    employee_name
    FROM attendance
    WHERE date=?
    """,
    (
        datetime.now().strftime(
            "%Y-%m-%d"
        ),
    ))

    rows = cursor.fetchall()

    for row in rows:

        attendance_box.insert(
            "end",
            f"{row[0]}    "
            f"{row[1]}    "
            f"Present\n"
        )

    conn.close()
load_attendance_data()
def show_attendance_graph():
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
    data = cursor.fetchall()
    conn.close()
    names = []
    hours = []
    for row in data:
        names.append(row[0])
        try:
            hours.append(
                float(
                    row[1].split(":")[0]
                )
            )
        except:
            hours.append(0)
    plt.figure(figsize=(8,5))
    plt.bar(
        names,
        hours
    )
    plt.title(
        "Employee Working Hours"
    )
    plt.xlabel(
        "Employees"
    )
    plt.ylabel(
        "Hours"
    )
    plt.show()
analytics_btn = ctk.CTkButton(
    dashboard_page,
    text="Show Analytics",
    width=250,
    height=50,
    command=show_attendance_graph
)
analytics_btn.pack(
    pady=20
)
graph_btn = ctk.CTkButton(
    attendance_page,
    text="Show Analytics Graph",
    command=show_attendance_graph
)
graph_btn.pack(pady=10)
reports_title = ctk.CTkLabel(
    reports_page,
    text="📄 Reports",
    font=("Segoe UI", 42, "bold")
)
reports_title.pack(pady=30)
reports_box = ctk.CTkTextbox(
    reports_page,
    width=900,
    height=500,
    font=("Consolas", 18)
)
reports_box.pack(pady=20)
reports_box.insert(
    "end",
    "Attendance Reports\n\n"
)
def load_reports():

    reports_box.delete(
        "1.0",
        "end"
    )

    reports_box.insert(
        "end",
        "Attendance Reports\n\n"
    )

    conn = sqlite3.connect(
        "database/chronosface.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
    employee_id,
    employee_name
    FROM biometric_data
    """)

    employees = cursor.fetchall()

    for emp in employees:

        cursor.execute("""
        SELECT COUNT(*)
        FROM attendance
        WHERE employee_id=?
        AND strftime('%Y-%m', date)=strftime('%Y-%m','now')
        """,
        (emp[0],))

        present_days = (
            cursor.fetchone()[0]
        )

        percentage = (
            present_days / 30
        ) * 100

        reports_box.insert(
            "end",
            f"{emp[1]}    "
            f"{percentage:.1f}%\n"
        )

    conn.close()
load_reports()
def export_report():
    path = export_attendance()
    messagebox.showinfo(
        "Success",
        f"Report Saved\n{path}"
    )
export_btn = ctk.CTkButton(
    reports_page,
    text="Export Attendance CSV",
    width=250,
    height=45,
    command=export_report
)
export_btn.pack(
    pady=10
)
leave_title = ctk.CTkLabel(
    leave_page,
    text="Leave Requests",
    font=("Segoe UI",42,"bold")
)
leave_title.pack(pady=30)
leave_box = ctk.CTkTextbox(
    leave_page,
    width=900,
    height=500,
    font=("Consolas",18)
)
leave_box.pack(pady=20)
leave_id_entry = ctk.CTkEntry(
    leave_page,
    width=250,
    height=40,
    placeholder_text="Enter Leave ID"
)
leave_id_entry.pack(pady=10)
def load_pending_leaves():
    leave_box.delete("1.0","end")
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
    id,
    employee_id,
    employee_name,
    leave_date,
    reason,
    status
    FROM leaves
    WHERE status='Pending'
    """)
    rows = cursor.fetchall()
    for row in rows:
        leave_box.insert(
            "end",
            f"ID:{row[0]} | "
            f"{row[2]} | "
            f"{row[3]} | "
            f"{row[4]} | "
            f"{row[5]}\n"
        )
    conn.close()
load_pending_leaves()
def approve_leave():
    leave_id = leave_id_entry.get()
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE leaves
    SET status='Approved'
    WHERE id=?
    """,
    (leave_id,))
    cursor.execute("""
    SELECT name
    FROM leaves
    WHERE id=?
    """,(leave_id,))
    employee = cursor.fetchone()
    if employee:
        cursor.execute("""
        INSERT INTO api_logs
        (
            endpoint,
            employee_name,
            action,
            log_time
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            "/leave/status",
            employee[0],
            "LEAVE_APPROVED",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ))
    conn.commit()
    conn.close()
    messagebox.showinfo(
        "Success",
        "Leave Approved"
    )
    load_pending_leaves()
approve_btn = ctk.CTkButton(
    leave_page,
    text="Approve Leave",
    width=220,
    height=45,
    fg_color="green",
    command=approve_leave
)
approve_btn.pack(pady=5)
def reject_leave():
    leave_id = leave_id_entry.get()
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE leaves
    SET status='Rejected'
    WHERE id=?
    """,
    (leave_id,))
    cursor.execute("""
    SELECT name
    FROM leaves
    WHERE id=?
    """,(leave_id,))

    employee = cursor.fetchone()

    if employee:
        cursor.execute("""
        INSERT INTO api_logs
        (
            endpoint,
            employee_name,
            action,
            log_time
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            "/leave/status",
            employee[0],
            "LEAVE_REJECTED",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ))
    conn.commit()
    conn.close()
    messagebox.showinfo(
        "Success",
        "Leave Rejected"
    )
    load_pending_leaves()
reject_btn = ctk.CTkButton(
    leave_page,
    text="Reject Leave",
    width=220,
    height=45,
    fg_color="red",
    command=reject_leave
)
reject_btn.pack(pady=5)
wfh_title = ctk.CTkLabel(
    wfh_page,
    text="Work From Home",
    font=("Segoe UI", 42, "bold")
)
wfh_title.pack(pady=30)
wfh_box = ctk.CTkTextbox(
    wfh_page,
    width=900,
    height=500,
    font=("Consolas", 18)
)
wfh_box.pack(pady=20)
wfh_box.insert(
    "end",
    "WFH Requests\n\n"
)
wfh_box.insert(
    "end",
    "1040    Ruchitha    Approved\n"
)
payroll_title = ctk.CTkLabel(
    payroll_page,
    text="Payroll",
    font=("Segoe UI", 42, "bold")
)
payroll_title.pack(pady=30)
payroll_box = ctk.CTkTextbox(
    payroll_page,
    width=900,
    height=500,
    font=("Consolas", 18)
)
payroll_box.pack(pady=20)
payroll_box.insert(
    "end",
    "Payroll Details\n\n"
)
payroll_box.insert(
    "end",
    "1040    Ruchitha    ₹50,000\n"
)
conn = sqlite3.connect(
    "database/chronosface.db"
)
cursor = conn.cursor()
cursor.execute("""
SELECT
    employee_id,
    employee_name
FROM biometric_data
""")
records = cursor.fetchall()
conn.close()
employee_options = [
    f"{row[0]} - {row[1]}"
    for row in records
]
def create_payslip():
    selected = employee_dropdown.get()
    employee_id = selected.split(" - ")[0]
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        employee_name,
        department
    FROM biometric_data
    WHERE employee_id=?
    """,
    (employee_id,)
    )
    employee = cursor.fetchone()
    conn.close()
    if employee:
        employee_name = employee[0]
        department = employee[1]
        file_path = generate_payslip(
            employee_id,
            employee_name,
            department,
            50000
        )
        messagebox.showinfo(
            "Success",
            f"Payslip Generated\n\n{file_path}"
        )
employee_dropdown = ctk.CTkComboBox(
    payroll_page,
    values=employee_options,
    width=300
)
employee_dropdown.pack(
    pady=10
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
    text="⚙ Settings",
    font=("Segoe UI", 42, "bold")
)
settings_title.pack(pady=40)
def hr_toggle_theme():
    current_mode = ctk.get_appearance_mode()
    if current_mode == "Dark":
        ctk.set_appearance_mode("light")
    else:
        ctk.set_appearance_mode("dark")
def hr_about():
    messagebox.showinfo(
        "About HR Dashboard",
        "ChronosFace HR Panel\n\n"
        "Features:\n"
        "- Employee Management\n"
        "- Attendance Tracking\n"
        "- Payroll System\n"
        "- Work From Home Requests\n"
        "- Reports & Analytics"
    )
def export_hr_report():
    messagebox.showinfo(
        "Export",
        "HR Report Exported Successfully"
    )
theme_btn = ctk.CTkButton(
    settings_page,
    text="🎨 Toggle Theme",
    width=320,
    height=55,
    font=("Arial", 20, "bold"),
    fg_color="#7c3aed",
    hover_color="#6d28d9",
    command=hr_toggle_theme
)
theme_btn.pack(pady=20)
report_btn = ctk.CTkButton(
    settings_page,
    text="📄 Export HR Reports",
    width=320,
    height=55,
    font=("Arial", 20, "bold"),
    fg_color="#15803d",
    hover_color="#166534",
    command=export_hr_report
)
report_btn.pack(pady=20)
about_btn = ctk.CTkButton(
    settings_page,
    text="ℹ About HR Panel",
    width=320,
    height=55,
    font=("Arial", 20, "bold"),
    fg_color="#ca8a04",
    hover_color="#a16207",
    text_color="black",
    command=hr_about
)
about_btn.pack(pady=20)
password_btn = ctk.CTkButton(
    settings_page,
    text="🔑 Change Password",
    width=320,
    height=55,
    font=("Arial", 20, "bold"),
    fg_color="#2563eb",
    hover_color="#1d4ed8",
    command=lambda: open_change_password("hr")
)
password_btn.pack(pady=20)
show_page(dashboard_page)
auto_refresh_hr()
app.mainloop()