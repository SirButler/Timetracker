import sqlite3

def initialize_db():
    conn = sqlite3.connect('topics.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            total_time INTEGER DEFAULT 0,
            running INTEGER DEFAULT 0,  -- 0 for stopped, 1 for running
            start_time INTEGER DEFAULT 0 -- last start time in seconds since epoch
        )
    ''')
    conn.commit()
    conn.close()

initialize_db()