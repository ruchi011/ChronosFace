import sqlite3

conn = sqlite3.connect("database/chronosface.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings(

id INTEGER PRIMARY KEY,

camera_id INTEGER,

recognition_threshold REAL,

unknown_threshold REAL,

attendance_cooldown INTEGER,

recognition_interval INTEGER,

admin_password TEXT

)
""")

cursor.execute("""
SELECT COUNT(*)
FROM settings
""")

if cursor.fetchone()[0] == 0:

    cursor.execute("""
    INSERT INTO settings
    VALUES(
        1,
        0,
        0.60,
        0.45,
        30,
        1,
        'admin123'
    )
    """)

conn.commit()
conn.close()
print("Settings table ready.")