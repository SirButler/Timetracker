import sqlite3

conn = sqlite3.connect('topics.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(topics)")
columns = cursor.fetchall()
conn.close()

for column in columns:
    print(column)