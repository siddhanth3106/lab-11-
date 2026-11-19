import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database and seed default user accounts if not present."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    # Check if default demo users exist; if not, seed them
    cursor.execute("SELECT COUNT(*) AS count FROM users")
    count = cursor.fetchone()['count']

    if count == 0:
        demo_users = [
            ("admin", "admin123", "System Administrator"),
            ("john_doe", "password123", "John Doe"),
            ("alice", "alice@2026", "Alice Smith"),
            ("siddharth", "sid@pass", "Siddharth")
        ]
        for username, password, full_name in demo_users:
            hashed_pw = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
                (username, hashed_pw, full_name)
            )
        conn.commit()
        print("Database initialized with default seed accounts.")
    conn.close()

def verify_user(username, password):
    """
    Check if the submitted username and password match records in the database.
    Returns the user dict if valid, or None if invalid.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query user by username (parameterized query prevents SQL injection)
    cursor.execute("SELECT * FROM users WHERE username = ?", (username.strip(),))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        return {
            'id': user['id'],
            'username': user['username'],
            'full_name': user['full_name'],
            'created_at': user['created_at']
        }
    return None

def register_user(username, password, full_name):
    """Register a new user in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        hashed_pw = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
            (username.strip(), hashed_pw, full_name.strip())
        )
        conn.commit()
        return True, "User registered successfully!"
    except sqlite3.IntegrityError:
        return False, "Username already exists. Please choose a different name."
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    print("Database setup complete.")
