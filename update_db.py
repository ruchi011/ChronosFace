import sqlite3

conn = sqlite3.connect("database/chronosface.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE strangers ADD COLUMN camera TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE strangers ADD COLUMN confidence REAL")
except:
    pass

try:
    cursor.execute("ALTER TABLE strangers ADD COLUMN status TEXT")
except:
    pass

conn.commit()
conn.close()

print("Strangers table updated successfully.")