import sqlite3

def get_db():
    # Connect to SQLite database
    global conn
    conn = sqlite3.connect('stocks.db')
    return conn

def configure(app):
    app.db = get_db()

def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS purchases (
                        id INTEGER PRIMARY KEY,
                        stock_code CHAR[6] NOT NULL,
                        amount INTEGER NOT NULL
                    )''')
    conn.commit()
 
def check(conn, id, stock):
    cursor = conn.cursor()
    cursor.execute("SELECT stock_code FROM purchases WHERE id=?", (id))
    result = cursor.fetchone()
    return result is not None
 
def insert(conn, stock_code, amount):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO purchases (stock_code, amount) VALUES (?, ?)", (stock_code, amount))
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