from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter

import os


def generate_payslip(
    employee_id,
    employee_name,
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
    present_days = 26

    absent_days = 4

    per_day_salary = salary / 30

    absence_deduction = (
        absent_days * per_day_salary
    )

    overtime_bonus = 2000

    net_salary = (
        salary
        - absence_deduction
        + overtime_bonus
    )
    employee_info = Paragraph(
        f"""
        Employee ID: {employee_id}<br/>
        Employee Name: {employee_name}<br/>
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