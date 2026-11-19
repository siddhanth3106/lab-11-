from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import os
import database

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Ensure database is initialized on startup
with app.app_context():
    database.init_db()

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('success'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Basic input validation
        if not username or not password:
            error = "Both login name and password are required."
            return render_template('login.html', error=error, username=username)

        # Check credentials against the database
        user = database.verify_user(username, password)

        if user:
            # Login successful: store in session
            session['user'] = user
            session['login_time'] = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            return redirect(url_for('success'))
        else:
            # Login failed: return failure message to the user
            error = "Authentication Failed: Invalid login name or password. Please try again."
            return render_template('login.html', error=error, username=username)

    return render_template('login.html', error=error)

@app.route('/success')
def success():
    if 'user' not in session:
        flash("Please log in first to access this page.", "warning")
        return redirect(url_for('login'))
    
    return render_template(
        'success.html',
        user=session['user'],
        login_time=session.get('login_time')
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    success_msg = None
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not username or not password:
            error = "All fields are required."
        elif len(username) < 3:
            error = "Username must be at least 3 characters long."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        elif password != confirm_password:
            error = "Passwords do not match."
        else:
            registered, msg = database.register_user(username, password, full_name)
            if registered:
                flash("Registration successful! You can now log in with your credentials.", "success")
                return redirect(url_for('login'))
            else:
                error = msg

    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Running on port 5000 with debug enabled
    app.run(debug=True, host='127.0.0.1', port=5000)
