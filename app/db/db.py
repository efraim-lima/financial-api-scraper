# Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import sqlite3
import random
import string
import contextlib

@contextlib.contextmanager
def get_db_connection():
    conn = sqlite3.connect('./app/db/purchases.db', check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()

def get_db():
    db_file = './app/db/purchases.db'
    
    global conn
    conn = sqlite3.connect(db_file, check_same_thread=False, timeout=10)
    create_purchases(conn)
    return conn

def configure(app):
    app.db = get_db()

def create_purchases(conn):
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS history (
                        id TEXT PRIMARY KEY,
                        ticker TEXT NOT NULL,
                        amount INTEGER NOT NULL,
                        date DATE NOT NULL
                    );""")
    conn.commit()

def check(conn, ticker, now):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history WHERE ticker=? AND date(date)=?;", (ticker, now))
    result = cursor.fetchone()
    return result is not None
 
def insert(conn, ticker, amount, now):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        cursor.execute("INSERT INTO history (id, ticker, amount, date) VALUES (?, ?, ?, ?);", (id, ticker, amount, now))
        conn.commit()
        print("Added successfully.")
        return

def close():
    # Close connection
    conn.close()
