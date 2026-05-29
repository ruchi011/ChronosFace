import sqlite3
conn = sqlite3.connect(
    "database/chronosface.db"
)
cursor = conn.cursor()
cursor.execute(
    "SELECT * FROM employees"
)
employees = cursor.fetchall()
print("\nEmployee Records:\n")
for employee in employees:
    print(employee)
conn.close()