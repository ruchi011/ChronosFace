import customtkinter as ctk
import subprocess
import sys
from tkinter import messagebox
from profile_window import open_profile
from change_password import open_change_password
from payslip_generator import generate_payslip
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
for frame in (
    dashboard_page,
    employees_page,
    attendance_page,
    reports_page,
    wfh_page,
    payroll_page,
    settings_page
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
    "25",
    "green"
)
create_card(
    cards_frame,
    "Present Today",
    "19",
    "cyan"
)
create_card(
    cards_frame,
    "Absent",
    "6",
    "red"
)
create_card(
    cards_frame,
    "Avg Work Hours",
    "7.5h",
    "orange"
)
employees_title = ctk.CTkLabel(
    employees_page,
    text="👥 Employees",
    font=("Segoe UI", 42, "bold")
)
employees_title.pack(pady=30)
employees_box = ctk.CTkTextbox(
    employees_page,
    width=900,
    height=500,
    font=("Consolas", 18)
)
employees_box.pack(pady=20)
employees_box.insert(
    "end",
    "Employee Details\n\n"
)
employees_box.insert(
    "end",
    "1040    Ruchitha    IT\n"
)
employees_box.insert(
    "end",
    "1041    John        HR\n"
)
employees_box.insert(
    "end",
    "1042    Tony        Finance\n"
)
attendance_title = ctk.CTkLabel(
    attendance_page,
    text="Attendance",
    font=("Segoe UI", 42, "bold")
)
attendance_title.pack(pady=30)
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
attendance_box.insert(
    "end",
    "1040    Ruchitha    Present\n"
)
attendance_box.insert(
    "end",
    "1041    John        Present\n"
)
attendance_box.insert(
    "end",
    "1042    Tony        Absent\n"
)
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
reports_box.insert(
    "end",
    "Ruchitha   95%\n"
)
reports_box.insert(
    "end",
    "John       90%\n"
)
reports_box.insert(
    "end",
    "Tony       82%\n"
)
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
def create_payslip():
    file_path = generate_payslip(
        "1040",
        "Ruchitha",
        "IT",
        50000
    )
    messagebox.showinfo(
        "Success",
        f"Payslip Generated\n\n{file_path}"
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
app.mainloop()