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
cursor.execute("""
CREATE TABLE IF NOT EXISTS biometric_data (
    employee_id TEXT PRIMARY KEY,
    name TEXT,
    department TEXT,
    email TEXT,
    phone TEXT,
    face_embedding TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS settings(
    id INTEGER PRIMARY KEY,
    admin_password TEXT,
    hr_password TEXT,
    camera_index INTEGER,
    recognition_threshold REAL,
    ear_threshold REAL
)
""")
cursor.execute("""
INSERT OR IGNORE INTO settings
VALUES(
    1,
    'admin123',
    'hr123',
    0,
    0.6,
    0.25
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS visitors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    visitor_name TEXT,
    purpose TEXT,
    date TEXT,
    time TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS strangers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image_path TEXT,
    date TEXT,
    time TEXT
)
""")
conn.commit()
conn.close()
print("Database Created Successfully")