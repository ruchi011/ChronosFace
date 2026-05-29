import sqlite3

conn = sqlite3.connect("database/chronosface.db")
cursor = conn.cursor()

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

conn.commit()
conn.close()

print("Whitelist and Blacklist tables created successfully")