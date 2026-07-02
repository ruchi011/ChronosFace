import customtkinter as ctk
import sqlite3
import os
from tkinter import ttk, messagebox
from PIL import Image
DB_PATH = "database/chronosface.db"
def open_strangers(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Stranger Management")
    window.geometry("1550x850")
    window.transient(parent)
    window.grab_set()
    title = ctk.CTkLabel(
        window,
        text="Stranger Management",
        font=("Segoe UI",34,"bold")
    )
    title.pack(pady=(20,10))
    toolbar = ctk.CTkFrame(window)
    toolbar.pack(fill="x", padx=20, pady=10)
    search_entry = ctk.CTkEntry(
        toolbar,
        width=280,
        placeholder_text="Search by Date / Time"
    )
    search_entry.pack(side="left", padx=10)
    total_label = ctk.CTkLabel(
        toolbar,
        text="Total Strangers : 0",
        font=("Segoe UI",16,"bold")
    )
    total_label.pack(side="right", padx=20)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#202020",
        foreground="white",
        fieldbackground="#202020",
        rowheight=36,
        font=("Segoe UI",11)
    )
    style.configure(
        "Treeview.Heading",
        background="#2563eb",
        foreground="white",
        font=("Segoe UI",12,"bold")
    )
    table_frame = ctk.CTkFrame(window)
    table_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )
    columns = (
        "ID",
        "Image",
        "Date",
        "Time",
        "Camera",
        "Confidence",
        "Status"
    )
    stranger_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )
    x_scroll = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=stranger_table.xview
    )
    y_scroll = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=stranger_table.yview
    )
    stranger_table.configure(
        xscrollcommand=x_scroll.set,
        yscrollcommand=y_scroll.set
    )
    widths = {
        "ID":70,
        "Image":300,
        "Date":120,
        "Time":120,
        "Camera":120,
        "Confidence":120,
        "Status":120
    }
    for col in columns:
        stranger_table.heading(
            col,
            text=col
        )
        stranger_table.column(
            col,
            width=widths[col],
            anchor="center",
            stretch=False
        )
    stranger_table.grid(
        row=0,
        column=0,
        sticky="nsew"
    )
    y_scroll.grid(
        row=0,
        column=1,
        sticky="ns"
    )
    x_scroll.grid(
        row=1,
        column=0,
        sticky="ew"
    )
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    def load_strangers(search_text=""):
        for item in stranger_table.get_children():
            stranger_table.delete(item)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if search_text == "":
            cursor.execute("""
            SELECT
                id,
                image_path,
                date,
                time,
                camera,
                confidence,
                status
            FROM strangers
            ORDER BY id DESC
            """)
        else:
            cursor.execute("""
            SELECT
                id,
                image_path,
                date,
                time,
                camera,
                confidence,
                status
            FROM strangers
            WHERE
                date LIKE ?
                OR time LIKE ?
                OR status LIKE ?
            ORDER BY id DESC
            """,
            (
                f"%{search_text}%",
                f"%{search_text}%",
                f"%{search_text}%"
            ))
        records = cursor.fetchall()
        print(records)
        conn.close()
        total_label.configure(
            text=f"Total Strangers : {len(records)}"
        )
        for row in records:
            image_name = os.path.basename(row[1])
            stranger_table.insert(
                "",
                "end",
                values=(
                    row[0],
                    image_name,
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6]
                )
            )
    def refresh_table():
        search_entry.delete(0, "end")
        load_strangers()
    def search_strangers(event=None):
        keyword = search_entry.get().strip()
        load_strangers(keyword)
    search_entry.bind(
        "<KeyRelease>",
        search_strangers
    )
    def delete_stranger():
        selected = stranger_table.selection()
        if not selected:
            messagebox.showwarning(
                "Delete Stranger",
                "Please select a stranger."
            )
            return
        confirm = messagebox.askyesno(
            "Delete",
            "Delete selected stranger?"
        )
        if not confirm:
            return
        stranger_id = stranger_table.item(
            selected[0]
        )["values"][0]
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM strangers
        WHERE id=?
        """,
        (stranger_id,)
        )
        conn.commit()
        conn.close()
        load_strangers()
    refresh_btn = ctk.CTkButton(
        toolbar,
        text="↻ Refresh",
        width=120,
        command=refresh_table
    )
    refresh_btn.pack(
        side="left",
        padx=5
    )
    delete_btn = ctk.CTkButton(
        toolbar,
        text="🗑 Delete",
        width=120,
        fg_color="#dc2626",
        hover_color="#b91c1c",
        command=delete_stranger
    )
    delete_btn.pack(
        side="left",
        padx=5
    )
    def preview_image(event=None):
        selected = stranger_table.selection()
        if not selected:
            return
        values = stranger_table.item(selected[0])["values"]
        stranger_id = values[0]
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT image_path
        FROM strangers
        WHERE id=?
        """,
        (stranger_id,)
        )
        result = cursor.fetchone()
        conn.close()
        if result is None:
            return
        image_path = result[0]
        if not os.path.exists(image_path):
            messagebox.showerror(
                "Image Missing",
                "Image file not found."
            )
            return
        preview = ctk.CTkToplevel(window)
        preview.title("Stranger Image")
        preview.geometry("600x650")
        preview.transient(window)
        img = ctk.CTkImage(
            light_image=Image.open(image_path),
            dark_image=Image.open(image_path),
            size=(500,500)
        )
        image_label = ctk.CTkLabel(
            preview,
            image=img,
            text=""
        )
        image_label.image = img
        image_label.pack(pady=20)
        ctk.CTkLabel(
            preview,
            text=os.path.basename(image_path),
            font=("Segoe UI",16)
        ).pack()
    stranger_table.bind(
        "<Double-1>",
        preview_image
    )
    load_strangers()