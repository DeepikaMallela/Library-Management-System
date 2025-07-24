from flask import Flask, render_template, request, redirect, url_for, session, flash

import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('lms.db')
    conn.row_factory = sqlite3.Row
    return conn
def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                copies INTEGER NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                action TEXT NOT NULL,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        if user:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/books')
def view_books():
    if 'user' not in session:
        return redirect(url_for('login'))

    filter_by = request.args.get('filter_by')
    query = request.args.get('query')

    conn = get_db_connection()

    if filter_by and query:
        sql = f"SELECT * FROM books WHERE {filter_by} LIKE ?"
        books = conn.execute(sql, ('%' + query + '%',)).fetchall()
    else:
        books = conn.execute('SELECT * FROM books').fetchall()

    conn.close()
    return render_template('books.html', books=books)


@app.route('/issue_return', methods=['GET', 'POST'])
def issue_return():
    message = ''
    if request.method == 'POST':
        book_id = request.form['book_id']
        action = request.form['action']

        conn = get_db_connection()
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()

        if book:
            if action == 'issue':
                conn.execute('UPDATE books SET copies = copies - 1 WHERE id = ?', (book_id,))
                message = 'Book issued successfully.'
            elif action == 'return':
                conn.execute('UPDATE books SET copies = copies + 1 WHERE id = ?', (book_id,))
                message = 'Book returned successfully.'

            # Add to history table
            conn.execute('INSERT INTO history (book_id, action) VALUES (?, ?)', (book_id, action))
            conn.commit()

        conn.close()
        print("Message to be shown:", message)  # Debug

    return render_template('issue_return.html', message=message)



@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        copies = request.form['copies']

        conn = sqlite3.connect('library.db')
        conn.execute('INSERT INTO books (title, author, copies) VALUES (?, ?, ?)', (title, author, copies))
        conn.commit()
        conn.close()

        flash('Book added successfully!')
        return redirect(url_for('dashboard'))  # or 'view_books'

    return render_template('add_book.html')

@app.route('/history')
def view_history():
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM history ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('history.html', history=history)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
