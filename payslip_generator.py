from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import os
import sqlite3
def generate_payslip(
    employee_id,
    name,
    department,
    salary
):

    os.makedirs(
        "payslips",
        exist_ok=True
    )

    file_path = (
        f"payslips/"
        f"{employee_id}_payslip.pdf"
    )

    doc = SimpleDocTemplate(
        file_path,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "<b>ChronosFace AI Payslip</b>",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
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
    absent_days = max(
        0,
        30 - present_days
    )
    conn.close()
    per_day_salary = salary / 30
    absence_deduction = (
        absent_days * per_day_salary
    )
    if present_days >= 28:
        overtime_bonus = 3000
    else:
        overtime_bonus = 1000
    net_salary = (
        salary
        - absence_deduction
        + overtime_bonus
    )
    employee_info = Paragraph(
        f"""
        Employee ID: {employee_id}<br/>
        Employee Name: {name}<br/>
        Department: {department}<br/>
        Basic Salary: ₹{salary}<br/>
        Present Days: {present_days}<br/>
        Absent Days: {absent_days}<br/>
        Absence Deduction: ₹{absence_deduction:.2f}<br/>
        Overtime Bonus: ₹{overtime_bonus}<br/>
        Net Salary: ₹{net_salary:.2f}
        """,

        styles["BodyText"]
    )

    elements.append(
        employee_info
    )

    doc.build(elements)

    return file_path