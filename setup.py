import sqlite3

# Connect our create our database for our users' usernames and passwords
conn = sqlite3.connect('users.db')

# Create a new 'users' table with username (unique) and password fields
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
''')

print("Users database setup successfully.")
conn.close()
