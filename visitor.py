import customtkinter as ctk
import sqlite3
from datetime import datetime
from tkinter import ttk, messagebox
DB_PATH = "database/chronosface.db"
def open_visitors(parent):
    window = ctk.CTkToplevel(parent)
    window.title("Visitor Management")
    window.geometry("1550x850")
    window.transient(parent)
    window.grab_set()
    title = ctk.CTkLabel(
        window,
        text="Visitor Management",
        font=("Segoe UI", 34, "bold")
    )
    title.pack(pady=(20, 10))
    toolbar = ctk.CTkFrame(window)
    toolbar.pack(fill="x", padx=20, pady=10)
    entry_frame = ctk.CTkFrame(window)
    entry_frame.pack(fill="x", padx=20, pady=(0,10))
    button_frame = ctk.CTkFrame(window)
    button_frame.pack(fill="x", padx=20, pady=(0,10))
    total_label = ctk.CTkLabel(
        toolbar,
        text="Total Visitors : 0",
        font=("Segoe UI", 15, "bold")
    )
    total_label.pack(
        side="right",
        padx=15
    )
    search_entry = ctk.CTkEntry(
        toolbar,
        width=250,
        placeholder_text="Search Name / Phone / Company"
    )
    search_entry.pack(side="left", padx=10)
    name_entry = ctk.CTkEntry(
        entry_frame,
        width=180,
        placeholder_text="Visitor Name"
    )
    name_entry.pack(side="left", padx=5)
    purpose_entry = ctk.CTkEntry(
        entry_frame,
        width=180,
        placeholder_text="Purpose"
    )
    purpose_entry.pack(side="left", padx=5)
    phone_entry = ctk.CTkEntry(
        entry_frame,
        width=140,
        placeholder_text="Phone"
    )
    phone_entry.pack(side="left", padx=5)
    email_entry = ctk.CTkEntry(
        entry_frame,
        width=180,
        placeholder_text="Email"
    )
    email_entry.pack(side="left", padx=5)
    company_entry = ctk.CTkEntry(
        entry_frame,
        width=150,
        placeholder_text="Company"
    )
    company_entry.pack(side="left", padx=5)
    host_entry = ctk.CTkEntry(
        entry_frame,
        width=150,
        placeholder_text="Host Employee"
    )
    host_entry.pack(side="left", padx=5)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="#202020",
        foreground="white",
        fieldbackground="#202020",
        rowheight=34,
        font=("Segoe UI", 11)
    )
    style.configure(
        "Treeview.Heading",
        background="#2563eb",
        foreground="white",
        font=("Segoe UI", 12, "bold")
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
        "Name",
        "Phone",
        "Email",
        "Company",
        "Purpose",
        "Host",
        "Visit Date",
        "Check In",
        "Check Out",
        "Status"
    )
    visitor_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )
    x_scroll = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=visitor_table.xview
    )
    y_scroll = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=visitor_table.yview
    )
    visitor_table.configure(
        xscrollcommand=x_scroll.set,
        yscrollcommand=y_scroll.set
    )
    widths = {
        "ID":70,
        "Name":160,
        "Phone":130,
        "Email":220,
        "Company":150,
        "Purpose":170,
        "Host":150,
        "Visit Date":110,
        "Check In":100,
        "Check Out":100,
        "Status":120
    }
    for col in columns:
        visitor_table.heading(
            col,
            text=col
        )
        visitor_table.column(
            col,
            width=widths[col],
            anchor="center",
            stretch=False
        )
    visitor_table.grid(
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
    table_frame.grid_rowconfigure(
        0,
        weight=1
    )
    table_frame.grid_columnconfigure(
        0,
        weight=1
    )
    def load_visitors(search_text=""):
        for item in visitor_table.get_children():
            visitor_table.delete(item)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if search_text == "":
            cursor.execute("""
            SELECT
                visitor_id,
                name,
                phone,
                email,
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
        else:
            cursor.execute("""
            SELECT
                visitor_id,
                name,
                phone,
                email,
                company,
                purpose,
                host_employee,
                visit_date,
                checkin_time,
                checkout_time,
                status
            FROM visitors
            WHERE
                name LIKE ?
                OR phone LIKE ?
                OR company LIKE ?
                OR purpose LIKE ?
            ORDER BY visitor_id DESC
            """,
            (
                f"%{search_text}%",
                f"%{search_text}%",
                f"%{search_text}%",
                f"%{search_text}%"
            ))
        records = cursor.fetchall()
        total_label.configure(
            text=f"Total Visitors : {len(records)}"
        )
        conn.close()
        visitor_table.tag_configure(
            "checkedin",
            foreground="#22c55e"
        )
        visitor_table.tag_configure(
            "checkedout",
            foreground="#ef4444"
        )
        for row in records:
            tag = "checkedin"
            if row[10] == "Checked Out":
                tag = "checkedout"
            visitor_table.insert(
                "",
                "end",
                values=row,
                tags=(tag,)
            )
    def add_visitor():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        company = company_entry.get().strip()
        purpose = purpose_entry.get().strip()
        host = host_entry.get().strip()
        if name == "" or purpose == "":
            messagebox.showwarning(
                "Missing Data",
                "Enter Visitor Name and Purpose."
            )
            return
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO visitors
        (
            name,
            phone,
            email,
            company,
            purpose,
            host_employee,
            visit_date,
            checkin_time,
            status
        )
        VALUES
        (
            ?,?,?,?,?,?,?,?,?
        )
        """,
        (
            name,
            phone,
            email,
            company,
            purpose,
            host,
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%H:%M:%S"),
            "Checked In"
        ))
        conn.commit()
        conn.close()
        name_entry.delete(0, "end")
        phone_entry.delete(0, "end")
        email_entry.delete(0, "end")
        company_entry.delete(0, "end")
        purpose_entry.delete(0, "end")
        host_entry.delete(0, "end")
        load_visitors()
    def delete_visitor():
        selected = visitor_table.selection()
        if not selected:
            messagebox.showwarning(
                "Select Visitor",
                "Select a visitor first."
            )
            return
        confirm = messagebox.askyesno(
            "Delete",
            "Delete selected visitor?"
        )
        if not confirm:
            return
        visitor_id = visitor_table.item(
            selected[0]
        )["values"][0]
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM visitors
        WHERE visitor_id=?
        """,
        (visitor_id,)
        )
        conn.commit()
        conn.close()
        load_visitors()
    def refresh_table():
        search_entry.delete(
            0,
            "end"
        )
        load_visitors()
    def search_visitors(event=None):
        keyword = search_entry.get().strip()
        load_visitors(keyword)
    search_entry.bind(
        "<KeyRelease>",
        search_visitors
    )
    add_btn = ctk.CTkButton(
        button_frame,
        text="+ Add",
        width=130,
        height=38,
        font=("Segoe UI",14,"bold"),
        command=add_visitor
    )
    add_btn.pack(
        side="left",
        padx=8
    )
    delete_btn = ctk.CTkButton(
        button_frame,
        text="🗑 Delete",
        width=130,
        height=38,
        font=("Segoe UI",14,"bold"),
        fg_color="#dc2626",
        hover_color="#b91c1c",
        command=delete_visitor
    )
    delete_btn.pack(
        side="left",
        padx=8
    )
    refresh_btn = ctk.CTkButton(
        button_frame,
        text="🔄 Refresh",
        width=130,
        height=38,
        font=("Segoe UI",14,"bold"),
        command=refresh_table
    )
    refresh_btn.pack(
        side="left",
        padx=8
    )
    def edit_visitor():
        selected = visitor_table.selection()
        if not selected:
            messagebox.showwarning(
                "Edit Visitor",
                "Please select a visitor."
            )
            return
        values = visitor_table.item(
            selected[0]
        )["values"]
        edit_window = ctk.CTkToplevel(window)
        edit_window.title("Edit Visitor")
        edit_window.geometry("500x420")
        edit_window.transient(window)
        edit_window.grab_set()
        ctk.CTkLabel(
            edit_window,
            text="Edit Visitor",
            font=("Segoe UI",26,"bold")
        ).pack(pady=20)
        name = ctk.CTkEntry(
            edit_window,
            width=350
        )
        name.pack(pady=10)
        name.insert(0, values[1])
        purpose = ctk.CTkEntry(
            edit_window,
            width=350
        )
        purpose.pack(pady=10)
        purpose.insert(0, values[5])
        status = ctk.CTkComboBox(
            edit_window,
            width=350,
            values=[
                "Checked In",
                "Checked Out"
            ]
        )
        status.pack(pady=10)
        status.set(values[10])
        def update():
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE visitors
            SET
                name=?,
                purpose=?,
                status=?
            WHERE visitor_id=?
            """,
            (
                name.get(),
                purpose.get(),
                status.get(),
                values[0]
            ))
            conn.commit()
            conn.close()
            edit_window.destroy()
            load_visitors()
        ctk.CTkButton(
            edit_window,
            text="Update Visitor",
            width=250,
            command=update
        ).pack(pady=25)
    edit_btn = ctk.CTkButton(
        button_frame,
        text="✏ Edit",
        width=130,
        height=38,
        font=("Segoe UI",14,"bold"),
        command=edit_visitor
    )
    edit_btn.pack(
        side="left",
        padx=8
    )
    visitor_table.bind(
        "<Double-1>",
        lambda e: edit_visitor()
    )
    load_visitors()