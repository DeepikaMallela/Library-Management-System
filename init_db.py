# import sqlite3

# conn = sqlite3.connect('library.db')
# cursor = conn.cursor()

# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS books (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         title TEXT NOT NULL,
#         author TEXT NOT NULL,
#         copies INTEGER NOT NULL
#     )
# ''')
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS history (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         book_id INTEGER NOT NULL,
#         action TEXT NOT NULL,
#         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#     )
# ''')


# conn.commit()
# conn.close()

# print("'books' table created successfully!")
# print("'history' table created successfully.")