import sqlite3

conn = sqlite3.connect(
    "database/chronosface.db"
)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    employee_id TEXT UNIQUE,
    department TEXT,
    email TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    name TEXT,
    date TEXT,
    clock_in TEXT,
    break_start TEXT,
    break_end TEXT,
    clock_out TEXT,
    total_break TEXT,
    working_hours TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS leaves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT,
    name TEXT,
    leave_date TEXT,
    reason TEXT,
    status TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS visitor_whitelist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitor_name TEXT,
    phone TEXT,
    company TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS visitor_blacklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitor_name TEXT,
    phone TEXT,
    reason TEXT
)
""")
cursor.execute("""
INSERT OR IGNORE INTO admins (
    username,
    password
)
VALUES (?, ?)
""", (
    "admin",
    "admin123"
))
conn.commit()
conn.close()
print("Database Created Successfully")