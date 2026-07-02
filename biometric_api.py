import sqlite3
from flask import Flask, request, jsonify
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
app = Flask(__name__)
with open("embeddings/face_embeddings.pkl", "rb") as f:
    employee_embeddings = pickle.load(f)
print("Loaded Employees:", list(employee_embeddings.keys()))
def get_db_connection():
    conn = sqlite3.connect("database/chronosface.db")
    conn.row_factory = sqlite3.Row
    return conn
@app.route("/api/biometric/register", methods=["POST"])
def register():
    print("REGISTER API HIT")
    data = request.json
    registered_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO biometric_data
    (
        employee_id,
        employee_name,
        department,
        email,
        phone,
        face_embedding,
        registered_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["employeeId"],
        data["employeeName"],
        data["department"],
        data["email"],
        data["phone"],
        str(data["faceEmbedding"]),
        registered_at
    ))
    cursor.execute("""
    INSERT INTO api_logs
    (endpoint,employee_name, action, log_time)
    VALUES (?, ?, ?, ?)
    """,
    (
        "/api/biometric/register",
        data["employeeName"],
        "REGISTER",
        registered_at
    ))
    conn.commit()
    conn.close()
    return jsonify({
        "message": "Employee Registered Successfully",
        "employeeId": data["employeeId"],
        "registeredAt": registered_at
    })
@app.route("/api/biometric/verify", methods=["POST"])
def verify():

    data = request.json
    name = data["employeeName"]

    if name not in employee_embeddings:
        return jsonify({
            "status": "employee_not_found"
        }), 404

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO api_logs
    (endpoint, employee_name, action, log_time)
    VALUES (?, ?, ?, ?)
    """,
    (
        "/api/biometric/verify",
        name,
        "VERIFY",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "verified",
        "employeeName": name
    })
@app.route("/api/biometric/all", methods=["GET"])
def get_all():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM biometric_data
    """)
    employees = [
        dict(row)
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(employees)
@app.route("/api/biometric/get_embedding/<name>", methods=["GET"])
def get_embedding(name):
    if name not in employee_embeddings:
        return jsonify({
            "message":"not found"
        }), 404
    return jsonify({
        "employeeName": name,
        "faceEmbedding":
            employee_embeddings[name].tolist()
    })
@app.route("/api/logs", methods=["GET"])
def logs():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM api_logs
    ORDER BY id DESC
    """)

    data = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(data)
@app.route("/api/employees", methods=["GET"])
def get_employees():

    conn = sqlite3.connect("database/chronosface.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        employee_id,
        employee_name,
        department
    FROM biometric_data
    """)

    employees = cursor.fetchall()

    conn.close()

    data = []

    for emp in employees:
        data.append({
            "employee_id": emp[0],
            "name": emp[1],
            "department": emp[2]
        })

    return jsonify(data)
@app.route("/api/attendance/startbreak", methods=["POST"])
def start_break_api():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id
    FROM attendance
    WHERE employee_id=?
    AND date=?
    """, (
        data["employeeId"],
        datetime.now().strftime("%Y-%m-%d")
    ))
    row = cursor.fetchone()
    if not row:
        return jsonify({
            "status":"error",
            "message":"Clock In First"
        }), 400
    cursor.execute("""
    UPDATE attendance
    SET break_start=?
    WHERE employee_id=? AND date=?
    """,
    (
        datetime.now().strftime("%H:%M:%S"),
        data["employeeId"],
        datetime.now().strftime("%Y-%m-%d")
    ))
    cursor.execute("""
    INSERT INTO api_logs
    (endpoint, employee_name, action, log_time)
    VALUES (?, ?, ?, ?)
    """,
    (
        "/api/attendance/startbreak",
        data["employeeName"],
        "START_BREAK",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()
    return jsonify({"status":"success"})
@app.route("/api/attendance/endbreak", methods=["POST"])
def end_break_api():

    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT break_start
    FROM attendance
    WHERE employee_id=?
    AND date=?
    """, (
        data["employeeId"],
        datetime.now().strftime("%Y-%m-%d")
    ))
    row = cursor.fetchone()
    if not row or not row[0]:
        return jsonify({
            "status":"error",
            "message":"Start Break First"
        }), 400
    cursor.execute("""
    UPDATE attendance
    SET break_end=?
    WHERE employee_id=? AND date=?
    """,
    (
        datetime.now().strftime("%H:%M:%S"),
        data["employeeId"],
        datetime.now().strftime("%Y-%m-%d")
    ))

    cursor.execute("""
    INSERT INTO api_logs
    (endpoint, employee_name, action, log_time)
    VALUES (?, ?, ?, ?)
    """,
    (
        "/api/attendance/endbreak",
        data["employeeName"],
        "END_BREAK",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()
    return jsonify({"status":"success"})
@app.route("/api/attendance/clockin", methods=["POST"])
def clock_in_api():
    data = request.json
    print("CLOCK IN API HIT")
    print(data)
    conn = get_db_connection()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    clock_time = datetime.now().strftime("%H:%M:%S")
    cursor.execute("""
    SELECT id
    FROM attendance
    WHERE employee_id=?
    AND date=?
    """, (
        data["employeeId"],
        today
    ))

    existing = cursor.fetchone()

    if existing:
        return jsonify({
            "status":"error",
            "message":"Already Clocked In"
        }), 400
    cursor.execute("""
    INSERT INTO attendance
    (
        employee_id,
        employee_name,
        date,
        clock_in
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        data["employeeId"],
        data["employeeName"],
        today,
        clock_time
    ))
    cursor.execute("""
    INSERT INTO api_logs
    (
        endpoint,
        employee_name,
        action,
        log_time
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        "/api/attendance/clockin",
        data["employeeName"],
        "CLOCK_IN",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success"
    })
@app.route("/api/attendance/clockout", methods=["POST"])
def clock_out_api():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT clock_in, break_start, break_end
    FROM attendance
    WHERE employee_id=? AND date=?
    """,
    (
        data["employeeId"],
        datetime.now().strftime("%Y-%m-%d")
    ))
    row = cursor.fetchone()
    if not row:
        return jsonify({
            "status":"error",
            "message":"No clock in found"
        }), 404
    clock_in = row[0]
    break_start = row[1]
    break_end = row[2]
    clock_out = datetime.now().strftime("%H:%M:%S")
    in_dt = datetime.strptime(clock_in,"%H:%M:%S")
    out_dt = datetime.strptime(clock_out,"%H:%M:%S")
    total_work = out_dt - in_dt
    if break_start and break_end:
        start_dt = datetime.strptime(
            break_start,
            "%H:%M:%S"
        )
        end_dt = datetime.strptime(
            break_end,
            "%H:%M:%S"
        )
        break_duration = end_dt - start_dt
    else:
        break_duration = timedelta()
    final_work = total_work - break_duration
    cursor.execute("""
    UPDATE attendance
    SET
        clock_out=?,
        total_break=?,
        working_hours=?
    WHERE employee_id=? AND date=?
    """,
    (
        clock_out,
        str(break_duration),
        str(final_work),
        data["employeeId"],
        datetime.now().strftime("%Y-%m-%d")
    ))
    cursor.execute("""
    INSERT INTO api_logs
    (
        endpoint,
        employee_name,
        action,
        log_time
    )
    VALUES (?, ?, ?, ?)
    """,
    (
        "/api/attendance/clockout",
        data["employeeName"],
        "CLOCK_OUT",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()
    return jsonify({
        "status":"success"
    })
@app.route("/api/leave/apply", methods=["POST"])
def apply_leave():

    data = request.json

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO leave_requests
    (
        employee_id,
        employee_name,
        leave_date,
        reason,
        status
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["employeeId"],
        data["employeeName"],
        data["leaveDate"],
        data["reason"],
        "Pending"
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "status":"success"
    })
if __name__ == "__main__":
    app.run(debug=True)