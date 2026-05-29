import customtkinter as ctk
import sqlite3
import sys
import subprocess
import sys
from PIL import Image
import os
from tkinter import messagebox
from datetime import datetime
from profile_window import open_profile
from change_password import open_change_password
import os
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
employee_id = sys.argv[1]
app = ctk.CTk()
app.title("Employee Dashboard")
app.geometry("1400x1000")
app.configure(fg_color="#0f172a")
try:
    with open("current_employee.txt", "r") as file:
        employee_id = file.read().strip()
except:
    employee_id = "Unknown"
main_frame = ctk.CTkScrollableFrame(
    app,
    fg_color="transparent"
)
main_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)
title = ctk.CTkLabel(
    main_frame,
    text="Employee Dashboard",
    font=("Segoe UI", 42, "bold")
)
title.pack(pady=30)
def menu_action(choice):
    if choice == "Profile":
        open_profile(employee_id)
    elif choice == "Change Password":
        open_change_password(employee_id)
    elif choice == "Switch to Admin":
        app.destroy()
        subprocess.Popen([
            sys.executable,
            "admin_dashboard.py"
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
profile_menu = ctk.CTkOptionMenu(
    main_frame,
    values=[
        "Profile",
        "Change Password",
        "Logout"
    ],
    command=menu_action,
    width=220,
    height=40,
    font=("Arial", 16)
)

profile_menu.place(
    x=1180,
    y=30
)
conn = sqlite3.connect(
    "database/chronosface.db"
)
cursor = conn.cursor()
cursor.execute("""
SELECT name, department, email
FROM employees
WHERE employee_id = ?
""", (employee_id,))
employee = cursor.fetchone()
conn.close()
if employee:
    employee_name = employee[0]
    department = employee[1]
    email = employee[2]
else:
    employee_name = "Unknown"
    department = "Unknown"
    email = "Unknown"
photo_path = None
dataset_path = "dataset"
if employee_name != "Unknown":
    employee_folder = os.path.join(
        dataset_path,
        employee_name
    )
    if os.path.exists(employee_folder):
        images = os.listdir(employee_folder)
        if len(images) > 0:
            photo_path = os.path.join(
                employee_folder,
                images[0]
            )
info_frame = ctk.CTkFrame(
    main_frame,
    width=1200,
    height=180
)
info_frame.pack(pady=10)
info_frame.pack_propagate(False)
if photo_path:
    profile_image = ctk.CTkImage(
        light_image=Image.open(photo_path),
        dark_image=Image.open(photo_path),
        size=(130, 130)
    )
    image_label = ctk.CTkLabel(
        info_frame,
        image=profile_image,
        text=""
    )
    image_label.place(
        x=40,
        y=25
    )
welcome_label = ctk.CTkLabel(
    info_frame,
    text=f"Welcome, {employee_name}",
    font=("Arial", 34, "bold")
)
welcome_label.pack(
    pady=15,
    padx=160
)
details_label = ctk.CTkLabel(
    info_frame,
    text=f"Employee ID : {employee_id}        Department : {department}        Email : {email}",
    font=("Arial", 20)
)
details_label.pack(
    pady=25,
    padx=160
)
conn = sqlite3.connect(
    "database/chronosface.db"
)
cursor = conn.cursor()
cursor.execute("""
SELECT
    clock_in,
    clock_out,
    working_hours
FROM attendance
WHERE employee_id = ?
ORDER BY id DESC
LIMIT 1
""", (employee_id,))
today_record = cursor.fetchone()
conn.close()
if today_record:
    clock_in = today_record[0]
    clock_out = today_record[1]
    work_hours = today_record[2]
    status_text = "Present"
else:
    clock_in = "-"
    clock_out = "-"
    work_hours = "-"
    status_text = "Absent"
status_dropdown = ctk.CTkFrame(
    main_frame,
    fg_color="#1e293b",
    corner_radius=20
)
status_dropdown.pack(
    fill="x",
    padx=30,
    pady=20
)
status_content = ctk.CTkFrame(
    status_dropdown,
    fg_color="#0f172a"
)
def toggle_status():
    if status_content.winfo_ismapped():
        status_content.pack_forget()
    else:
        status_content.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )
status_button = ctk.CTkButton(
    status_dropdown,
    text="📅 Today's Status",
    height=65,
    font=("Segoe UI", 28, "bold"),
    fg_color="#1e293b",
    hover_color="#334155",
    anchor="w",
    command=toggle_status
)
status_button.pack(
    fill="x",
    padx=15,
    pady=15
)
status_textbox = ctk.CTkTextbox(
    status_content,
    height=140,
    font=("Arial", 22)
)
status_textbox.pack(
    fill="x",
    padx=20,
    pady=20
)
status_textbox.insert(
    "end",
    f"""
Status : {status_text}
Clock In : {clock_in}
Clock Out : {clock_out}
Working Hours : {work_hours}
"""
)
status_textbox.configure(state="disabled")
summary_dropdown = ctk.CTkFrame(
    main_frame,
    fg_color="#1e293b",
    corner_radius=20
)
summary_dropdown.pack(
    fill="x",
    padx=30,
    pady=20
)
summary_content = ctk.CTkFrame(
    summary_dropdown,
    fg_color="#0f172a"
)
def toggle_summary():
    if summary_content.winfo_ismapped():
        summary_content.pack_forget()
    else:
        summary_content.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )
summary_button = ctk.CTkButton(
    summary_dropdown,
    text="📊 Monthly Attendance Summary",
    height=65,
    font=("Segoe UI", 28, "bold"),
    fg_color="#1e293b",
    hover_color="#334155",
    anchor="w",
    command=toggle_summary
)
summary_button.pack(
    fill="x",
    padx=15,
    pady=15
)
summary_textbox = ctk.CTkTextbox(
    summary_content,
    height=160,
    font=("Arial", 22)
)
summary_textbox.pack(
    fill="x",
    padx=20,
    pady=20
)
summary_textbox.insert(
    "end",
    """
Present Days : 22
Absent Days : 2
Attendance : 91%
"""
)
summary_textbox.configure(state="disabled")
history_dropdown = ctk.CTkFrame(
    main_frame,
    fg_color="#1e293b",
    corner_radius=20
)
history_dropdown.pack(
    fill="x",
    padx=30,
    pady=20
)
history_content = ctk.CTkFrame(
    history_dropdown,
    fg_color="#0f172a"
)
def toggle_history():
    if history_content.winfo_ismapped():
        history_content.pack_forget()
    else:
        history_content.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )
history_button = ctk.CTkButton(
    history_dropdown,
    text="📜 Attendance History",
    height=65,
    font=("Segoe UI", 28, "bold"),
    fg_color="#1e293b",
    hover_color="#334155",
    anchor="w",
    command=toggle_history
)
history_button.pack(
    fill="x",
    padx=15,
    pady=15
)
attendance_box = ctk.CTkTextbox(
    history_content,
    width=1200,
    height=220,
    font=("Consolas", 18)
)
attendance_box.pack(
    fill="x",
    padx=20,
    pady=20
)
def open_leave_window():
    leave_window = ctk.CTkToplevel(app)
    leave_window.title("Apply Leave")
    leave_window.geometry("500x500")
    leave_window.configure(fg_color="#1e1e1e")
    leave_window.focus()
    leave_window.grab_set()
    leave_window.lift()
    title = ctk.CTkLabel(
        leave_window,
        text="Apply Leave",
        font=("Arial", 32, "bold")
    )
    title.pack(pady=30)
    leave_date_entry = ctk.CTkEntry(
        leave_window,
        width=320,
        height=50,
        placeholder_text="Leave Date (YYYY-MM-DD)"
    )
    leave_date_entry.pack(pady=20)
    reason_entry = ctk.CTkEntry(
        leave_window,
        width=320,
        height=50,
        placeholder_text="Reason"
    )
    reason_entry.pack(pady=20)
    def submit_leave():
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO leaves (
            employee_id,
            name,
            leave_date,
            reason,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            employee_id,
            employee_name,
            leave_date_entry.get(),
            reason_entry.get(),
            "Pending"
        ))
        conn.commit()
        conn.close()
        leave_window.destroy()
    submit_btn = ctk.CTkButton(
        leave_window,
        text="Submit Leave",
        width=250,
        height=50,
        command=submit_leave
    )
    submit_btn.pack(pady=30)
def load_attendance():
    attendance_box.configure(state="normal")
    attendance_box.delete("1.0", "end")
    attendance_box.insert(
        "end",
        "Date         Clock In      Clock Out     Break        Working Hours\n"
    )
    attendance_box.insert(
        "end",
        "---------------------------------------------------------------------\n"
    )
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        date,
        clock_in,
        clock_out,
        total_break,
        working_hours
    FROM attendance
    WHERE employee_id = ?
    """, (employee_id,))
    records = cursor.fetchall()
    conn.close()
    for row in records:
        attendance_box.insert(
            "end",
            f"{row[0]:<13}{row[1]:<14}{row[2]:<14}{row[3]:<13}{row[4]}\n"
        )
    attendance_box.configure(state="disabled")
load_attendance()
def clock_out():
    current_time = datetime.now().strftime(
        "%H:%M:%S"
    )
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT clock_in
    FROM attendance
    WHERE employee_id = ?
    AND date = date('now')
    """, (employee_id,))
    result = cursor.fetchone()
    if result:
        clock_in_time = result[0]
        in_time = datetime.strptime(
            clock_in_time,
            "%H:%M:%S"
        )
        out_time = datetime.strptime(
            current_time,
            "%H:%M:%S"
        )
        work_duration = (
            out_time - in_time
        )
        cursor.execute("""
        UPDATE attendance
        SET
            clock_out = ?,
            working_hours = ?
        WHERE employee_id = ?
        AND date = date('now')
        """, (
            current_time,
            str(work_duration),
            employee_id
        ))
        conn.commit()
        messagebox.showinfo(
            "Success",
            "Clock Out Successful"
        )
    else:
        messagebox.showerror(
            "Error",
            "No Clock In Found"
        )
    conn.close()
def apply_leave():
    leave_window = ctk.CTkToplevel(app)
    leave_window.title("Apply Leave")
    leave_window.geometry("500x450")
    leave_window.configure(fg_color="#1e1e1e")
    title = ctk.CTkLabel(
        leave_window,
        text="Leave Application",
        font=("Arial", 30, "bold")
    )
    title.pack(pady=25)
    date_entry = ctk.CTkEntry(
        leave_window,
        width=320,
        height=50,
        placeholder_text="Leave Date (YYYY-MM-DD)",
        font=("Arial", 18)
    )
    date_entry.pack(pady=20)
    reason_box = ctk.CTkTextbox(
        leave_window,
        width=320,
        height=220,
        font=("Arial", 16)
    )
    reason_box.pack(pady=20)
    def submit_leave():
        leave_date = date_entry.get().strip()
        reason = reason_box.get("1.0", "end").strip()
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO leaves (
            employee_id,
            name,
            leave_date,
            reason,
            status
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            employee_id,
            employee_name,
            leave_date,
            reason,
            "Pending"
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo(
            "Success",
            "Leave Request Submitted"
        )
        leave_window.destroy()
    submit_btn = ctk.CTkButton(
        leave_window,
        text="Submit Leave",
        width=250,
        height=50,
        font=("Arial", 20),
        fg_color="#2563eb",
        hover_color="#1d4ed8",
        command=submit_leave
    )
    submit_btn.pack(pady=20)
apply_leave_btn = ctk.CTkButton(
    main_frame,
    text="Apply Leave",
    width=250,
    height=50,
    font=("Arial", 20),
    fg_color="#2563eb",
    hover_color="#1d4ed8",
    command=open_leave_window
)
apply_leave_btn.pack(pady=10)
logout_btn = ctk.CTkButton(
    main_frame,
    text="Logout",
    width=220,
    height=50,
    fg_color="red",
    hover_color="darkred",
    font=("Arial", 20),
    command=app.destroy
)
logout_btn.pack(pady=10)
app.mainloop()
