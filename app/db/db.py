import sqlite3

def get_db():
    # Connect to SQLite database
    global conn
    conn = sqlite3.connect('stocks.db')
    return conn

def configure(app):
    app.db = get_db()

def create_purchase(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS purchase (
                        id INTEGER PRIMARY KEY,
                        ticker CHAR[6] NOT NULL,
                        amount INTEGER NOT NULL
                    )''')
    conn.commit()

def check(conn, ticker, table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM  WHERE ticker=?", (ticker, table_name))
    result = cursor.fetchone()
    return result
 
def insert(conn, ticker, amount):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO table_name (ticker, amount) VALUES (?, ?)", (ticker, amount))
    conn.commit()
    print("Added successfully.")

# Create table if it doesn't exist
create_table_if_not_exists(conn)

# Check for conflicts
if check_for_conflict(conn, name):
    print("Error: A user with this name already exists.")
else:
    # Insert user if no conflict
    insert_user(conn, name, address)

# Close connection
conn.close()