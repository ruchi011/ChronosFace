import sqlite3
import csv
import os

def export_attendance():

    os.makedirs(
        "reports",
        exist_ok=True
    )

    file_path = (
        "reports/"
        "attendance_report.csv"
    )

    conn = sqlite3.connect(
        "database/chronosface.db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM attendance
    """)

    rows = cursor.fetchall()

    with open(
        file_path,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Employee ID",
            "Name",
            "Date",
            "Clock In",
            "Break Start",
            "Break End",
            "Clock Out",
            "Total Break",
            "Working Hours"
        ])

        writer.writerows(rows)

    conn.close()

    return file_path