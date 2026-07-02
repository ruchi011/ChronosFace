import customtkinter as ctk
import sqlite3
from tkinter import messagebox

DB_PATH = "database/chronosface.db"


def open_param_settings(parent):

    window = ctk.CTkToplevel(parent)
    window.title("Parameter Settings")
    window.geometry("700x550")
    window.transient(parent)
    window.grab_set()
    title = ctk.CTkLabel(
        window,
        text="Parameter Settings",
        font=("Segoe UI", 30, "bold")
    )
    title.pack(pady=20)
    form = ctk.CTkFrame(window)
    form.pack(fill="both", expand=True, padx=30, pady=20)
    camera_label = ctk.CTkLabel(
        form,
        text="Camera ID",
        font=("Segoe UI",16,"bold")
    )
    camera_label.grid(row=0,column=0,padx=20,pady=15,sticky="w")
    camera_entry = ctk.CTkEntry(
        form,
        width=250
    )
    camera_entry.grid(row=0,column=1,padx=20,pady=15)
    recognition_label = ctk.CTkLabel(
        form,
        text="Recognition Threshold",
        font=("Segoe UI",16,"bold")
    )
    recognition_label.grid(row=1,column=0,padx=20,pady=15,sticky="w")
    recognition_entry = ctk.CTkEntry(
        form,
        width=250
    )
    recognition_entry.grid(row=1,column=1,padx=20,pady=15)
    unknown_label = ctk.CTkLabel(
        form,
        text="Unknown Threshold",
        font=("Segoe UI",16,"bold")
    )
    unknown_label.grid(row=2,column=0,padx=20,pady=15,sticky="w")
    unknown_entry = ctk.CTkEntry(
        form,
        width=250
    )
    unknown_entry.grid(row=2,column=1,padx=20,pady=15)
    admin_label = ctk.CTkLabel(
        form,
        text="Admin Password",
        font=("Segoe UI",16,"bold")
    )
    admin_label.grid(row=3,column=0,padx=20,pady=15,sticky="w")
    admin_entry = ctk.CTkEntry(
        form,
        width=250,
        show="*"
    )
    admin_entry.grid(row=3,column=1,padx=20,pady=15)
    hr_label = ctk.CTkLabel(
        form,
        text="HR Password",
        font=("Segoe UI",16,"bold")
    )
    hr_label.grid(row=4,column=0,padx=20,pady=15,sticky="w")
    hr_entry = ctk.CTkEntry(
        form,
        width=250,
        show="*"
    )
    hr_entry.grid(row=4,column=1,padx=20,pady=15)
    def load_settings():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT
            admin_password,
            hr_password,
            camera_index,
            recognition_threshold,
            ear_threshold
        FROM settings
        WHERE id=1
        """)
        row = cursor.fetchone()
        conn.close()
        if row:
            admin_entry.insert(0,row[0])
            hr_entry.insert(0,row[1])
            camera_entry.insert(0,str(row[2]))
            recognition_entry.insert(0,str(row[3]))
            unknown_entry.insert(0,str(row[4]))
    load_settings()
    def save_settings():
        try:
            camera = int(camera_entry.get())
            recognition = float(recognition_entry.get())
            ear = float(unknown_entry.get())
            admin = admin_entry.get().strip()
            hr = hr_entry.get().strip()
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE settings
            SET
                admin_password=?,
                hr_password=?,
                camera_index=?,
                recognition_threshold=?,
                ear_threshold=?
            WHERE id=1
            """,
            (
                admin,
                hr,
                camera,
                recognition,
                ear
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo(
                "Success",
                "Settings saved successfully."
            )
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Camera ID must be an integer.\nThresholds must be numeric."
            )
    button_frame = ctk.CTkFrame(
        window,
        fg_color="transparent"
    )
    button_frame.pack(
        pady=20
    )
    save_btn = ctk.CTkButton(
        button_frame,
        text="💾 Save Changes",
        width=180,
        height=40,
        command=save_settings
    )
    save_btn.pack(
        side="left",
        padx=10
    )
    reload_btn = ctk.CTkButton(
        button_frame,
        text="↻ Reload",
        width=180,
        height=40,
        command=lambda: (
            camera_entry.delete(0, "end"),
            recognition_entry.delete(0, "end"),
            unknown_entry.delete(0, "end"),
            admin_entry.delete(0, "end"),
            hr_entry.delete(0, "end"),
            load_settings()
        )
    )
    reload_btn.pack(
        side="left",
        padx=10
    )
    