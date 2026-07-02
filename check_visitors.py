import sqlite3

conn = sqlite3.connect("database/chronosface.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(visitors)")
print(cursor.fetchall())

conn.close()