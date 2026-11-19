# User Validation Web Application (Lab 11)

A complete web application that validates user login credentials against a database backend.

## 📌 Problem Statement
A user validation web application where:
1. The user submits their **login name & password** to the server.
2. The name and password are checked against records available in the **Database**.
3. If credentials match: A **successful login page** is returned to the user.
4. If credentials do not match: A clear **failure message** is returned and displayed to the user.

---

## 🛠️ Technology Stack
- **Backend:** Python 3 + Flask
- **Database:** SQLite 3 (built-in relational database, zero external configuration required)
- **Security:** Password hashing using Werkzeug (`generate_password_hash` / `check_password_hash`) & parameterized SQL queries to prevent SQL injection
- **Frontend:** Responsive HTML5 + Modern CSS3

---

## 📁 Project Directory Structure
```
lab 11/
│
├── app.py                  # Flask web server, route handlers, session management
├── database.py             # SQLite database connection, table creation, seed data & queries
├── users.db                # SQLite database storing user credentials
├── requirements.txt        # Python dependencies (Flask)
├── README.md               # Documentation & setup guide
├── templates/
│   ├── base.html           # Base layout template
│   ├── login.html          # Login form with failure alerts & demo credentials guide
│   ├── success.html        # Successful login dashboard page
│   └── register.html       # Optional registration form to add new users to the DB
└── static/
    └── css/
        └── style.css       # Clean, modern UI styling
```

---

## 🚀 How to Run the Application

### 1. Ensure Dependencies Are Installed
Flask is already installed on your system. If needed, you can reinstall or verify:
```bash
pip install -r requirements.txt
```

### 2. Start the Server
Run the Flask application:
```bash
python app.py
```

### 3. Open in Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Pre-seeded Database Accounts
The database is pre-populated with the following user accounts for immediate testing:

| Username / Login Name | Password | Full Name |
| :--- | :--- | :--- |
| `admin` | `admin123` | System Administrator |
| `john_doe` | `password123` | John Doe |
| `alice` | `alice@2026` | Alice Smith |
| `siddharth` | `sid@pass` | Siddharth |

---

## 🧪 Testing the Application

### 1. Successful Login Test
1. Go to `http://127.0.0.1:5000/login`.
2. Enter username: `admin`
3. Enter password: `admin123`
4. Click **Login to Account**.
5. **Expected Result:** The server verifies the record against `users.db` and renders the **Login Successful!** page displaying user details and login timestamp.

### 2. Failure Validation Test
1. Go to `http://127.0.0.1:5000/login`.
2. Enter username: `admin`
3. Enter password: `wrongpassword` (or enter a non-existent username).
4. Click **Login to Account**.
5. **Expected Result:** The server rejects the credentials and returns an error alert:
   > *"Authentication Failed: Invalid login name or password. Please try again."*

### 3. Dynamic Registration (Optional)
1. Click **Register here** or navigate to `http://127.0.0.1:5000/register`.
2. Fill out the form to insert a brand new user into the SQLite database.
3. Log in with the newly created credentials to verify real-time database validation.
