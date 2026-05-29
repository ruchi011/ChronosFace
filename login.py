import customtkinter as ctk
import subprocess
import sys
from PIL import Image
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()
app.title("ChronosFace Login")
app.geometry("700x750")
app.configure(fg_color="#0f172a")
app.resizable(False, False)
logo_image = ctk.CTkImage(
    light_image=Image.open("assets/logo.png"),
    dark_image=Image.open("assets/logo.png"),
    size=(120, 120)
)
logo_label = ctk.CTkLabel(
    app,
    image=logo_image,
    text=""
)
logo_label.pack(pady=(40, 10))
title = ctk.CTkLabel(
    app,
    text="ChronosFace AI",
    font=("Segoe UI", 48, "bold")
)
title.pack(pady=20)
subtitle = ctk.CTkLabel(
    app,
    text="Smart Face Recognition Attendance System",
    font=("Segoe UI", 18),
    text_color="#94a3b8"
)
subtitle.pack(pady=5)
def open_admin():
    app.destroy()
    subprocess.Popen([
        sys.executable,
        "admin_login.py"
    ])
def open_hr():
    app.destroy()
    subprocess.run([
        sys.executable,
        "hr_dashboard.py"
    ])
def open_employee():
    app.destroy()
    subprocess.run([
        sys.executable,
        "employee_login.py"
    ])
admin_btn = ctk.CTkButton(
    app,
    text="🛡 Admin",
    width=300,
    height=65,
    font=("Arial", 24),
    fg_color="#15803d",
    hover_color="#166534",
    command=open_admin
)
admin_btn.pack(pady=20)
hr_btn = ctk.CTkButton(
    app,
    text="👥 HR",
    width=300,
    height=65,
    font=("Arial", 24),
    fg_color="#ca8a04",
    hover_color="#a16207",
    text_color="black",
    command=open_hr
)
hr_btn.pack(pady=20)
employee_btn = ctk.CTkButton(
    app,
    text="🧑 Employee",
    width=300,
    height=65,
    font=("Arial", 24),
    fg_color="#dc2626",
    hover_color="#991b1b",
    command=open_employee
)
employee_btn.pack(pady=20)
signup_btn = ctk.CTkButton(
    app,
    text="📝 Signup",
    width=300,
    height=60,
    font=("Arial", 24),
    fg_color="#7c3aed",
    hover_color="#6d28d9",
    corner_radius=18,
    command=lambda: [
        app.destroy(),
        subprocess.Popen([
            sys.executable,
            "signup.py"
        ])
    ]
)
signup_btn.pack(pady=20)
app.mainloop()