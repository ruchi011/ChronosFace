import customtkinter as ctk
import csv

ctk.set_appearance_mode("dark")

app = ctk.CTk()

app.title("Attendance Reports")

app.geometry("700x500")

title = ctk.CTkLabel(
    app,
    text="Attendance Reports",
    font=("Arial", 30, "bold")
)

title.pack(pady=20)

textbox = ctk.CTkTextbox(
    app,
    width=600,
    height=350,
    font=("Arial", 16)
)

textbox.pack(pady=20)

try:

    with open(
        "attendance/attendance.csv",
        "r"
    ) as file:

        reader = csv.reader(file)

        for row in reader:

            line = " | ".join(row)

            textbox.insert(
                "end",
                line + "\n"
            )

except FileNotFoundError:

    textbox.insert(
        "end",
        "No attendance records found."
    )

app.mainloop()