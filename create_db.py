import sqlite3

conn = sqlite3.connect('lms.db')

# Create users table
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Create books table
conn.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    status TEXT DEFAULT 'Available'
)
''')

# Create issued books table
conn.execute('''
CREATE TABLE IF NOT EXISTS issued (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    username TEXT,
    issue_date TEXT
)
''')

conn.close()
print("Database and tables created successfully.")
