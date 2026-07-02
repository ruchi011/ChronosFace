import customtkinter as ctk
from tkinter import messagebox
import sqlite3
ctk.set_appearance_mode("dark")
def open_change_password(employee_id):
    window = ctk.CTkToplevel()
    window.focus_force()
    window.grab_set()
    window.lift()
    window.attributes("-topmost", True)
    window.after(
        200,
        lambda: window.attributes("-topmost", False)
    )
    window.title("Change Password")
    window.geometry("500x560")
    window.configure(fg_color="#0f172a")
    title = ctk.CTkLabel(
        window,
        text="Change Password",
        font=("Segoe UI", 30, "bold"),
        text_color="white"
    )
    title.pack(pady=30)
    old_password_entry = ctk.CTkEntry(
        window,
        width=320,
        height=50,
        placeholder_text="Old Password",
        show="*",
        corner_radius=12,
        font=("Arial", 16)
    )
    old_password_entry.pack(pady=15)
    new_password_entry = ctk.CTkEntry(
        window,
        width=320,
        height=50,
        placeholder_text="New Password",
        show="*",
        corner_radius=12,
        font=("Arial", 16)
    )
    new_password_entry.pack(pady=15)
    confirm_password_entry = ctk.CTkEntry(
        window,
        width=320,
        height=50,
        placeholder_text="Confirm Password",
        show="*",
        corner_radius=12,
        font=("Arial", 16)
    )
    confirm_password_entry.pack(pady=15)
    def update_password():
        old_password = old_password_entry.get()
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()
        if (
            old_password == "" or
            new_password == "" or
            confirm_password == ""
        ):
            messagebox.showerror(
                "Error",
                "All Fields Are Required"
            )
            return
        if new_password != confirm_password:
            messagebox.showerror(
                "Error",
                "New Passwords Do Not Match"
            )
            return
        conn = sqlite3.connect(
            "database/chronosface.db"
        )
        cursor = conn.cursor()
        if employee_id == "admin":
            cursor.execute("""
            SELECT admin_password
            FROM settings
            WHERE id=1
            """)
            current_password = cursor.fetchone()
            if (
                current_password and
                current_password[0] == old_password
            ):
                cursor.execute("""
                UPDATE settings
                SET admin_password=?
                WHERE id=1
                """,
                (new_password,)
                )
                conn.commit()
                messagebox.showinfo(
                    "Success",
                    "Admin Password Changed Successfully"
                )
                window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Old Password Incorrect"
                )
                conn.commit()
                messagebox.showinfo(
                    "Success",
                    "Admin Password Changed Successfully"
                )
                window.destroy()
        elif employee_id == "hr":
            cursor.execute("""
            SELECT hr_password
            FROM settings
            WHERE id=1
            """)
            current_password = cursor.fetchone()
            if (
                current_password and
                current_password[0] == old_password
            ):
                cursor.execute("""
                UPDATE settings
                SET hr_password=?
                WHERE id=1
                """,
                (new_password,)
                )
                conn.commit()
                messagebox.showinfo(
                    "Success",
                    "HR Password Changed Successfully"
                )
                window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Old Password Incorrect"
                )
                conn.commit()
                messagebox.showinfo(
                    "Success",
                    "HR Password Changed Successfully"
                )
                window.destroy()
        else:
            cursor.execute("""
            SELECT password
            FROM employees
            WHERE employee_id = ?
            """, (employee_id,))
            current_password = cursor.fetchone()
            if (
                current_password and
                current_password[0] == old_password
            ):
                cursor.execute("""
                UPDATE employees
                SET password = ?
                WHERE employee_id = ?
                """,
                (
                    new_password,
                    employee_id
                ))
                conn.commit()
                messagebox.showinfo(
                    "Success",
                    "Password Changed Successfully"
                )
                window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    "Old Password Incorrect"
                )
        conn.close()
    save_btn = ctk.CTkButton(
        window,
        text="Update Password",
        width=260,
        height=50,
        corner_radius=15,
        font=("Arial", 18, "bold"),
        fg_color="#2563eb",
        hover_color="#1d4ed8",
        command=update_password
    )
    save_btn.pack(pady=35)