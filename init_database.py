import sqlite3
import os

if not os.path.exists("database"):
    os.makedirs("database")

conn = sqlite3.connect("database/expense.db")
cur = conn.cursor()

cur.executescript("""

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS expenses;

CREATE TABLE users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE
);

CREATE TABLE expenses(
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    category TEXT,
    amount REAL,
    date TEXT
);

""")

conn.commit()
conn.close()

print("Database created")