import os
import sqlite3
import random
import string

def get_db():
    db_file = './app/db/purchases.db'
    
    global conn
    conn = sqlite3.connect(db_file)
    create_purchases(conn)
    return conn

def configure(app):
    app.db = get_db()

def create_purchases(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS purchases (
                        id TEXT PRIMARY KEY,
                        ticker TEXT NOT NULL,
                        amount INTEGER NOT NULL,
                        date DATE NOT NULL
                    )''')
    conn.commit()

def check(ticker, now):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM purchases WHERE ticker=? AND date(date)=?", (ticker, now))
    result = cursor.fetchone()
    return result is not None
 
def insert(ticker, amount, now):
    id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO purchases (
        id, ticker, amount, date) VALUES (?, ?, ?, ?)""", 
        (id, ticker, amount, now)
    )
    conn.commit()
    print("Added successfully.")
    return

def close():
    # Close connection
    conn.close()