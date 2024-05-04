# Import from the parent directory (app)
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import bleach
import datetime
import sqlite3
import random
import re
import string
import contextlib
from app.logs.logs import info, error, warn, critic

# Initialize logger
now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d %H:%M:%S")

def validation(input_string):
    pattern = r'^[a-zA-Z0-9]+$'
    return bool(re.match(pattern, input_string))


@contextlib.contextmanager
def get_db_connection():
    conn = sqlite3.connect('/app/db/purchases.db', check_same_thread=False)
    warn(f"database conn activated at {now}")
    try:
        yield conn
        warn("conn yeld at {now}")
    finally:
        warn("return of conn at {now}")
        return

def configure():
    with get_db_connection() as conn:
        create_purchases()

def create_purchases():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS history (
                            id TEXT PRIMARY KEY,
                            ticker TEXT NOT NULL,
                            amount INTEGER NOT NULL,
                            date DATE NOT NULL
                        );""")
        warn(f"table history created at {now}")
        conn.commit()

def check(ticker, now):
    with get_db_connection() as conn:
        if validation(ticker):
            ticker = bleach.clean(ticker)
            
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM history 
                              WHERE ticker = ? AND date(date) = ?;""", (ticker, now))
            result = cursor.fetchone()
            warn(f"data validation: {ticker} at {now}")

            if result:
                info(f"Record found successfully at {now}")
                return result
            else:
                info(f"No record found for the given criteria. at {now}")
                return None
        else:
            critic(f"Invalid input for ticker={ticker} at {now}.")
            return "Error"

 
def insert(ticker, amount, now):
    with get_db_connection() as conn:
        if validation(ticker) and validation(str(amount)) == True:
            ticker = bleach.clean(ticker)
            amount = bleach.clean(str(amount))

            warn(f"data sanitized: ticker={ticker}, amount={amount} and date={now} at {now}")

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
            warn(f"ticker={ticker}, amount={amount} and date={now} added successfully at {now}")            
            return
        else:
            critical(f"Sanitizatio failed in ticker={ticker} or amount={amount} at {now}")
            return "Error"

def get_amount_sum(stock_symbol):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(amount) FROM history WHERE ticker=?;", (stock_symbol,))
        result = cursor.fetchone()

        warn(f"Sum for {stock_symbol} got at {now}")            
        return result[0] if result else 0

def close():
    with get_db_connection() as conn:
        warn(f"database closed at {now}")
        # Close connection
        conn.close()
