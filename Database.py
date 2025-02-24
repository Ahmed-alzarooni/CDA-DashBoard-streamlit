import sqlite3

# Function to create the database and user table (only need to run once)
def create_db():
    conn = sqlite3.connect('users.db')  # Create a database file (users.db)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT)''')
    conn.commit()
    conn.close()

# Function to insert new user into the database
def insert_user(username, hashed_password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   (username, hashed_password))
    conn.commit()
    conn.close()

# Function to check if a user exists
def check_user_exists(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to retrieve user from the database
def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    # Debugging: Check if user is being retrieved correctly
    print(f"Retrieved user from DB: {user}")
    
    return user
