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


# create table  for user responses to be stored 
conn.execute('''
             CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
             userID INTEGER NOT NULL,
                response TEXT NOT NULL,
                FOREIGN KEY (userID) REFERENCES users(id)
             );
             ''')


print("Users database setup successfully.")
conn.close()
