import sqlite3
from contextlib import closing

import os
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'checked_cvs.db')
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'uploaded_cvs')

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS checked_cvs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT UNIQUE NOT NULL,
                    file_path TEXT NOT NULL,
                    checked_at TEXT NOT NULL,
                    result TEXT
                )
            ''')

def add_checked_cv(filename, file_bytes, checked_at, result):
    import os
    # Save file to disk
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, 'wb') as f:
        f.write(file_bytes)
    # Save metadata to DB
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute('''
                INSERT OR IGNORE INTO checked_cvs (filename, file_path, checked_at, result)
                VALUES (?, ?, ?, ?)
            ''', (filename, file_path, checked_at, result))

def is_cv_checked(filename):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute('SELECT id FROM checked_cvs WHERE filename = ?', (filename,))
        return cur.fetchone() is not None

def get_all_checked_cvs():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM checked_cvs')
        return cur.fetchall()

if __name__ == "__main__":
    init_db()
    print("Database initialized and ready.")
