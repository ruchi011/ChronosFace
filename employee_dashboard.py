from urllib import response
import requests
from tkinter import simpledialog
from tkinter import messagebox
import customtkinter as ctk
import sqlite3
import sys
import subprocess
import sys
from PIL import Image
import os
from tkinter import messagebox
from datetime import datetime
from attendance_export import export_attendance
from profile_window import open_profile
from change_password import open_change_password
import os
import requests
from datetime import datetime
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
SELECT employee_name, department, email
FROM biometric_data
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
attendance_btn_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)
attendance_btn_frame.pack(pady=20)
def clock_in():
    data = {
        "employeeId": employee_id,
        "employeeName": employee_name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "clockIn": datetime.now().strftime("%H:%M:%S")
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/attendance/clockin",
        json=data
    )
    print("Showing popup now...")
    if response.status_code == 200:
        app.focus_force()
        app.lift()
        app.after(
            100,
            lambda:messagebox.showinfo(
                parent=app,
                title="Success",
                message="Clock In Successful"
            )
        )
        load_attendance()
        load_today_status()

    else:
        messagebox.showerror(
            "Error",
            "Clock In Failed"
        )
def start_break():
    data = {
        "employeeId": employee_id
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/attendance/startbreak",
        json=data
    )
    if response.status_code == 200:
        app.focus_force()
        app.lift()
        app.after(
            100,
            lambda: messagebox.showinfo(
                "Success",
                "Break Started"
            )
        )
        load_attendance()
        load_today_status()
def end_break():
    data = {
        "employeeId": employee_id,
        "employeeName": employee_name   
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/attendance/endbreak",
        json=data
    )
    if response.status_code == 200:
        app.focus_force()
        app.lift()
        app.after(
            100,
            lambda: messagebox.showinfo(
                "Success",
                "Break Ended"
            )
        )
        load_attendance()
        load_today_status()
    else:
        messagebox.showerror(
            "Error",
            "Failed to End Break"
        )
def clock_out():
    print("CLOCK OUT BUTTON CLICKED")
    data = {
        "employeeId": employee_id,
        "employeeName": employee_name
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/attendance/clockout",
        json=data
    )
    if response.status_code == 200:
        app.focus_force()
        app.lift()
        app.after(
            100,
            lambda: messagebox.showinfo(
                "Success",
                "Clock Out Successful"
            )
        )
        load_attendance()
        load_today_status()
    else:
        messagebox.showerror(
            "Error",
            "Clock Out Failed"
        )
        
clockin_btn = ctk.CTkButton(
    attendance_btn_frame,
    text="Clock In",
    width=180,
    command=clock_in
)
clockin_btn.grid(row=0, column=0, padx=10)
break_btn = ctk.CTkButton(
    attendance_btn_frame,
    text="Start Break",
    width=180,
    command=start_break
)
break_btn.grid(row=0, column=1, padx=10)
endbreak_btn = ctk.CTkButton(
    attendance_btn_frame,
    text="End Break",
    width=180,
    command=end_break
)
endbreak_btn.grid(row=1, column=0, padx=10, pady=10)
clockout_btn = ctk.CTkButton(
    attendance_btn_frame,
    text="Clock Out",
    width=180,
    command=clock_out
)
clockout_btn.grid(row=1, column=1, padx=10, pady=10)
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
def load_today_status():
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
    WHERE employee_id=?
    ORDER BY id DESC
    LIMIT 1
    """,
    (employee_id,)
    )
    row = cursor.fetchone()
    conn.close()
    status_textbox.configure(state="normal")
    status_textbox.delete("1.0","end")
    if row:
        status_textbox.insert(
            "end",
            f"""
Status : Present
Clock In : {row[0]}
Clock Out : {row[1]}
Working Hours : {row[2]}
"""
        )
    else:
        status_textbox.insert(
            "end",
            "Absent"
        )
    status_textbox.configure(state="disabled")
load_today_status()
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
conn = sqlite3.connect(
    "database/chronosface.db"
)
cursor = conn.cursor()
cursor.execute("""
SELECT COUNT(*)
FROM attendance
WHERE employee_id=?
AND strftime('%Y-%m', date)=strftime('%Y-%m','now')
""",
(employee_id,))
present_days = cursor.fetchone()[0]
absent_days = 30 - present_days
attendance_percent = round(
    (present_days / 30) * 100,
    2
)
conn.close()
summary_textbox.insert(
    "end",
    f"""
Present Days : {present_days}
Absent Days : {absent_days}
Attendance : {attendance_percent} %
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
        date = row[0] if row[0] else "-"
        clock_in = row[1] if row[1] else "-"
        clock_out = row[2] if row[2] else "-"
        total_break = row[3] if row[3] else "-"
        working_hours = row[4] if row[4] else "-"
        attendance_box.insert(
            "end",
            f"{date:<13}{clock_in:<14}{clock_out:<14}{total_break:<13}{working_hours}\n"
        )
    attendance_box.configure(state="disabled")
load_attendance()

def apply_leave():
    leave_window = ctk.CTkToplevel(app)
    leave_window.title("Apply Leave")
    leave_window.geometry("550x700")
    leave_window.configure(fg_color="#1e1e1e")
    leave_window.transient(app)
    leave_window.grab_set()
    leave_window.focus_force()
    leave_window.lift()
    leave_window.attributes("-topmost", True)
    leave_window.after(
        500,
        lambda: leave_window.attributes("-topmost", False)
    )
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
        print("SUBMIT BUTTON CLICKED")
        leave_date = date_entry.get().strip()
        reason = reason_box.get("1.0", "end").strip()
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO leaves (
            employee_id,
            employee_name,
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
        cursor.execute("""
        INSERT INTO api_logs
        (
            endpoint,
            employee_name,
            action,
            log_time
        )
        VALUES (?, ?, ?, ?)
        """, (
            "/leave/apply",
            employee_name,
            "APPLY_LEAVE",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
        load_leave_history()
        print("LEAVE SAVED")
        leave_window.lift()
        leave_window.focus_force()
        messagebox.showinfo(
            parent=leave_window,
            title="Success",
            message="Leave Request Submitted"
        )
        leave_window.after(
            500,
            leave_window.destroy
        )
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
    font=("Arial",20),
    fg_color="#2563eb",
    hover_color="#1d4ed8",
    command=apply_leave
)
apply_leave_btn.pack(pady=10)
def download_report():
    export_attendance(employee_id)
    messagebox.showinfo(
        "Success",
        "Attendance Report Generated"
    )
download_btn = ctk.CTkButton(
    main_frame,
    text="Download Attendance Report",
    width=250,
    height=50,
    command=download_report
)
download_btn.pack(pady=10)
leave_dropdown = ctk.CTkFrame(
    main_frame,
    fg_color="#1e293b",
    corner_radius=20
)
leave_dropdown.pack(
    fill="x",
    padx=30,
    pady=20
)
leave_content = ctk.CTkFrame(
    leave_dropdown,
    fg_color="#0f172a"
)
def toggle_leave():
    if leave_content.winfo_ismapped():
        leave_content.pack_forget()
    else:
        leave_content.pack(
            fill="x",
            padx=20,
            pady=(0,20)
        )
leave_button = ctk.CTkButton(
    leave_dropdown,
    text="📋 Leave History",
    height=65,
    font=("Segoe UI",28,"bold"),
    fg_color="#1e293b",
    hover_color="#334155",
    anchor="w",
    command=toggle_leave
)
leave_button.pack(
    fill="x",
    padx=15,
    pady=15
)
leave_box = ctk.CTkTextbox(
    leave_content,
    height=200,
    font=("Consolas",18)
)
leave_box.pack(
    fill="x",
    padx=20,
    pady=20
)
def load_leave_history():
    leave_box.configure(state="normal")
    leave_box.delete("1.0","end")
    leave_box.insert(
        "end",
        "Date          Reason               Status\n"
    )
    leave_box.insert(
        "end",
        "-------------------------------------------\n"
    )
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        leave_date,
        reason,
        status
    FROM leaves
    WHERE employee_id=?
    """,
    (employee_id,)
    )
    records = cursor.fetchall()
    conn.close()
    for row in records:
        leave_box.insert(
            "end",
            f"{row[0]:<14}{row[1]:<20}{row[2]}\n"
        )
    leave_box.configure(state="disabled")
load_leave_history()
def check_leave_status():

    conn = sqlite3.connect(
        "database/chronosface.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT leave_date,status
    FROM leaves
    WHERE employee_id=?
    ORDER BY id DESC
    LIMIT 1
    """,
    (employee_id,)
    )

    record = cursor.fetchone()

    conn.close()

    if record:

        leave_date = record[0]
        status = record[1]

        if status == "Approved":

            messagebox.showinfo(
                "Leave Approved",
                f"Your leave for {leave_date} is Approved"
            )

        elif status == "Rejected":

            messagebox.showerror(
                "Leave Rejected",
                f"Your leave for {leave_date} is Rejected"
            )
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
check_leave_status()
app.mainloop()
