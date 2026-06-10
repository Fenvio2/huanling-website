import sqlite3
import os

SECRET_KEY = 'huanling_secret_key_2026'
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'huanling.db')


def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL,
            last_login TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            user_id INTEGER,
            amount TEXT,
            payment_method TEXT,
            status TEXT DEFAULT 'pending',
            created_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()
