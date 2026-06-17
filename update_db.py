import sqlite3

conn = sqlite3.connect("database/chronosface.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE biometric_data
ADD COLUMN registered_at TEXT
""")

conn.commit()
conn.close()

print("Column added successfully")