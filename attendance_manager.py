import sqlite3
from datetime import datetime
import requests
def clock_in(employee_id, name):

    response = requests.post(
        "http://127.0.0.1:5000/api/attendance/clockin",
        json={
            "employeeId": employee_id,
            "employeeName": name
        }
    )
    print(response.json())
def start_break(employee_id):

    response = requests.post(
        "http://127.0.0.1:5000/api/attendance/startbreak",
        json={
            "employeeId": employee_id
        }
    )
    print(response.json())
def end_break(employee_id):

    response = requests.post(
        "http://127.0.0.1:5000/api/attendance/endbreak",
        json={
            "employeeId": employee_id
        }
    )

    print(response.json())
def clock_out(employee_id):

    response = requests.post(
        "http://127.0.0.1:5000/api/attendance/clockout",
        json={
            "employeeId": employee_id
        }
    )
    print(response.json())