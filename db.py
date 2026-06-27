import sqlite3
import os
from datetime import date, datetime

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.db")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL CHECK(amount > 0),
            category_id INTEGER NOT NULL,
            description TEXT DEFAULT '',
            date TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('expense', 'income')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
        );

        INSERT OR IGNORE INTO categories (name, type) VALUES ('Food & Drink', 'expense');
        INSERT OR IGNORE INTO categories (name, type) VALUES ('Transport', 'expense');
        INSERT OR IGNORE INTO categories (name, type) VALUES ('Shopping', 'expense');
        INSERT OR IGNORE INTO categories (name, type) VALUES ('Entertainment', 'expense');
        INSERT OR IGNORE INTO categories (name, type) VALUES ('Bills & Utilities', 'expense');
        INSERT OR IGNORE INTO categories (name, type) VALUES ('Salary', 'income');
        INSERT OR IGNORE INTO categories (name, type) VALUES ('Freelance', 'income');
        INSERT OR IGNORE INTO categories (name, type) VALUES ('Investment', 'income');
        INSERT OR IGNORE INTO categories (name, type) VALUES ('Other Income', 'income');
        INSERT OR IGNORE INTO categories (name, type) VALUES ('Other Expense', 'expense');
    """)
    conn.commit()
    conn.close()


init_db()
