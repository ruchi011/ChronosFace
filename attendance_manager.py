import sqlite3
from datetime import datetime
def clock_in(employee_id, name):
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    current_time = datetime.now().strftime(
        "%H:%M:%S"
        )

    current_date = datetime.now().strftime(
            "%Y-%m-%d"
        )

    status = "Present"
    current_hour = datetime.now().hour
    if current_hour >= 9:
            status = "Late"

    cursor.execute("""
    INSERT INTO attendance (
            employee_id,
            name,
            date,
            clock_in,
            clock_out,
            status,
            working_hours
     )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
    employee_id,
    name,
    current_date,
    current_time,
    "-",
     status,
     "-"
     ))
    conn.commit()
    conn.close()
    print(
        f"{name} Clocked In Successfully"
    )
def start_break(employee_id):
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    break_start = datetime.now().strftime(
        "%H:%M:%S"
    )
    cursor.execute("""
    UPDATE attendance
    SET break_start=?
    WHERE employee_id=?
    AND date=?
    """, (
        break_start,
        employee_id,
        datetime.now().strftime("%Y-%m-%d")
    ))
    conn.commit()
    conn.close()
    print(
        "Break Started"
    )
def end_break(employee_id):
    conn = sqlite3.connect(
        "database/chronosface.db"
    )
    cursor = conn.cursor()
    break_end = datetime.now().strftime(
        "%H:%M:%S"
    )
    cursor.execute("""
    UPDATE attendance
    SET break_end=?
    WHERE employee_id=?
    AND date=?
    """, (

        break_end,
        employee_id,
        datetime.now().strftime("%Y-%m-%d")

    ))

    conn.commit()

    conn.close()

    print(
        "Break Ended"
    )


def clock_out(employee_id):

    conn = sqlite3.connect(
        "database/chronosface.db"
    )

    cursor = conn.cursor()

    clock_out_time = datetime.now().strftime(
        "%H:%M:%S"
    )

    current_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    cursor.execute("""

    SELECT clock_in,
           break_start,
           break_end

    FROM attendance

    WHERE employee_id=?
    AND date=?

    """, (

        employee_id,
        current_date

    ))

    result = cursor.fetchone()

    clock_in_time = result[0]
    break_start = result[1]
    break_end = result[2]

    clock_in_dt = datetime.strptime(
        clock_in_time,
        "%H:%M:%S"
    )

    clock_out_dt = datetime.strptime(
        clock_out_time,
        "%H:%M:%S"
    )

    total_work = clock_out_dt - clock_in_dt

    if break_start and break_end:

        break_start_dt = datetime.strptime(
            break_start,
            "%H:%M:%S"
        )

        break_end_dt = datetime.strptime(
            break_end,
            "%H:%M:%S"
        )

        break_duration = (
            break_end_dt - break_start_dt
        )

    else:

        break_duration = total_work - total_work

    final_work = total_work - break_duration

    cursor.execute("""

    UPDATE attendance

    SET clock_out=?,
        total_break=?,
        working_hours=?

    WHERE employee_id=?
    AND date=?

    """, (

        clock_out_time,
        str(break_duration),
        str(final_work),
        employee_id,
        current_date

    ))

    conn.commit()

    conn.close()

    print(
        "Clock Out Successful"
    )