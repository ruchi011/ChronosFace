import customtkinter as ctk
from user_info import open_user_info
from param_settings import open_param_settings
from visitor import open_visitors
from strangers import open_strangers
def open_engineering_mode():
    window = ctk.CTk()
    window.title("Engineering Mode")
    window.geometry("1400x850")
    title = ctk.CTkLabel(
        window,
        text="Engineering Mode",
        font=("Segoe UI", 42, "bold")
    )
    title.pack(pady=30)
    cards_frame = ctk.CTkFrame(
        window,
        fg_color="transparent"
    )
    cards_frame.pack(
        fill="both",
        expand=True,
        padx=80,
        pady=40
    )
    cards_frame.grid_rowconfigure(0, weight=1)
    cards_frame.grid_rowconfigure(1, weight=1)
    cards_frame.grid_columnconfigure(0, weight=1)
    cards_frame.grid_columnconfigure(1, weight=1)
    user_btn = ctk.CTkButton(
        cards_frame,
        text="👤\n\nUser Info",
        width=420,
        height=220,
        font=("Segoe UI", 30, "bold"),
        corner_radius=18,
        command=lambda: open_user_info(window)
    )
    user_btn.grid(
        row=0,
        column=0,
        padx=30,
        pady=30,
        sticky="nsew"
    )
    param_btn = ctk.CTkButton(
        cards_frame,
        text="⚙\n\nParam Settings",
        width=420,
        height=220,
        font=("Segoe UI", 30, "bold"),
        corner_radius=18,
        command=lambda: open_param_settings(window)
    )
    param_btn.grid(
        row=0,
        column=1,
        padx=30,
        pady=30,
        sticky="nsew"
    )
    visitor_btn = ctk.CTkButton(
        cards_frame,
        text="🚶\n\nVisitors",
        width=420,
        height=220,
        font=("Segoe UI", 30, "bold"),
        corner_radius=18,
        command=lambda: open_visitors(window)
    )
    visitor_btn.grid(
        row=1,
        column=0,
        padx=30,
        pady=30,
        sticky="nsew"
    )
    stranger_btn = ctk.CTkButton(
        cards_frame,
        text="❓\n\nStrangers",
        width=420,
        height=220,
        font=("Segoe UI",30,"bold"),
        corner_radius=18,
        command=lambda: open_strangers(window)
    )
    stranger_btn.grid(
        row=1,
        column=1,
        padx=30,
        pady=30,
        sticky="nsew"
    )
    window.mainloop()