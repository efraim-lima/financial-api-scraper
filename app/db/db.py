# Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import bleach
import sqlite3
import random
import re
import string
import contextlib

def validation(input_string):
    pattern = r'^[a-zA-Z0-9]+$'
    return bool(re.match(pattern, input_string))


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
    if validation(ticker) == True:
        ticker = bleach.clean(ticker)
        now = bleach.clean(now)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM 
        history 
        WHERE 
        ticker=%(ticker)s AND date(date)=%(now)s;""", {
            'ticker': ticker,
            'now': now
        })
        result = cursor.fetchone()
        return result
    else: 
        return "Error"
 
def insert(conn, ticker, amount, now):
    if validation(ticker) and validation(amount) == True:
        ticker = bleach.clean(ticker)
        amount = bleach.clean(amount)
        now = bleach.clean(now)
        with get_db_connection() as conn:
            cursor = conn.cursor()
            id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            cursor.execute("""INSERT INTO history (id, ticker, amount, date) VALUES (
                %(id)s, 
                %(ticker)s, 
                %(amount)s, 
                %(date)s
                );""",{
                    'id': id,
                    'ticker': ticker,
                    'amount': amount,
                    'date': now
                })
            conn.commit()
            print("Added successfully.")
            return
    else:
        return "Error"
def get_amount_sum(conn, stock_symbol):
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM history WHERE ticker=?;", (stock_symbol))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else 0

def close():
    # Close connection
    conn.close()
