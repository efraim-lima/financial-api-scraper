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
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def validation(input_string):
    pattern = r'^[a-zA-Z0-9]+$'
    return bool(re.match(pattern, input_string))


@contextlib.contextmanager
def get_db_connection():
    conn = sqlite3.connect('./app/db/purchases.db', check_same_thread=False)
    try:
        yield conn
    finally:
        return

def configure(app):
    app.db = get_db()

def create_purchases():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS history (
                            id TEXT PRIMARY KEY,
                            ticker TEXT NOT NULL,
                            amount INTEGER NOT NULL,
                            date DATE NOT NULL
                        );""")
        conn.commit()

def check(ticker, now):
    with get_db_connection() as conn:
        if validation(ticker):
            ticker = bleach.clean(ticker)
            
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM history 
                              WHERE ticker = ? AND date(date) = ?;""", (ticker, now))
            result = cursor.fetchone()
            
            if result:
                logger.info("Record found successfully.")
                return result
            else:
                logger.info("No record found for the given criteria.")
                return None
        else:
            logger.error("Invalid input for ticker.")
            return "Error"

 
def insert(ticker, amount, now):
    with get_db_connection() as conn:
        if validation(ticker) and validation(str(amount)) == True:
            ticker = bleach.clean(ticker)
            amount = bleach.clean(str(amount))
            now = bleach.clean(now)
            with get_db_connection() as conn:
                cursor = conn.cursor()
                id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO history (ticker, amount, date) VALUES (
                            :ticker, 
                            :amount, 
                            :date
                            );""", {
                                'ticker': ticker,
                                'amount': amount,
                                'date': now
                            })
            conn.commit()
            logger.info("Added successfully.")            
            return
        else:
            logger.error("Failed to insert in database")
            return "Error"
def get_amount_sum(stock_symbol):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM history WHERE ticker=?;", (stock_symbol,))
        result = cursor.fetchone()
        return result[0] if result else 0

def close():
    with get_db_connection() as conn:
        # Close connection
        conn.close()
