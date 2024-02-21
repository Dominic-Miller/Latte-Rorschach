from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to connect to ur users database
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to query our database
def query_db(query, args=(), one=False):
    conn = get_db_connection()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    conn.commit()
    return (rv[0] if rv else None) if one else rv

# The default page upon startup should be the login page
@app.route('/')
def index():
    return redirect(url_for('login'))

# Homepage for our application after logging in
@app.route('/home')
def home():
    if 'username' in session:
        return f'Hello, {session["username"]}! <br/><a href="/logout">Logout</a>'
    return redirect(url_for('login'))

# Registration page to crate an account
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Register account if POST
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Generate a hashed password for security
        hashed_password = generate_password_hash(password)
        # Add the username and password to the database if possible
        try:
            query_db('INSERT INTO users (username, password) VALUES (?, ?)', [username, hashed_password])
            flash('User registered successfully.')
            return redirect(url_for('login'))
        # If the username already exists, make the user try again
        except sqlite3.IntegrityError:
            flash('Username already exists.')
    # Take them to registration page for GET
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login if POST
    if request.method == 'POST':
        # Get the username and password and check the database for it
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ?', [username], one=True)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            # Redirect to the homepage for successful login
            return redirect(url_for('home'))
        flash('Invalid username or password.')
    # Take to login page if GET
    return render_template('login.html')

# Function to logout and redirect the user to the login front page
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Main execution function
if __name__ == '__main__':
    app.run(debug=True)
