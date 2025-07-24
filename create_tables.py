import sqlite3

conn = sqlite3.connect('lms.db')
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Insert default user (e.g., admin/admin)
cursor.execute('''
INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)
''', ('admin', 'admin'))

conn.commit()
conn.close()
