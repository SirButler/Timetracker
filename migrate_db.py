import sqlite3

def migrate_db():
    conn = sqlite3.connect('topics.db')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE topics ADD COLUMN running INTEGER DEFAULT 0")
    cursor.execute("ALTER TABLE topics ADD COLUMN start_time INTEGER DEFAULT 0")
    conn.commit()
    conn.close()

migrate_db()