import sqlite3
import os
import hashlib
import hmac
import base64
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
db_name = "project1.db"
sql_file = "project1.sql"
db_flag = False

# Read the secret key from key.txt
with open('key.txt', 'r') as f:
    SECRET_KEY = f.read().strip()

def create_db():
    conn = sqlite3.connect(db_name)
    
    with open(sql_file, 'r') as sql_startup:
        init_db = sql_startup.read()
    cursor = conn.cursor()
    cursor.executescript(init_db)
    conn.commit()
    conn.close()
    global db_flag
    db_flag = True
    return conn

def get_db():
    if not db_flag:
        create_db()
    conn = sqlite3.connect(db_name)
    return conn

def hash_password(password, salt):
    """Hash password using SHA-256 with salt"""
    combined = password + salt
    return hashlib.sha256(combined.encode()).hexdigest()

def generate_jwt(username):
    """Generate JWT token"""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"username": username, "access": "True"}
    
    # Encode header and payload (keep padding)
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    
    # Create signature
    message = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    return f"{header_encoded}.{payload_encoded}.{signature}"

def verify_jwt(token):
    """Verify JWT token and return username if valid"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
            
        header_encoded, payload_encoded, signature = parts
        
        # Verify signature
        message = f"{header_encoded}.{payload_encoded}"
        expected_signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(signature, expected_signature):
            return None
            
        # Decode payload
        payload = json.loads(base64.urlsafe_b64decode(payload_encoded).decode())
        return payload.get('username')
    except:
        return None

def validate_password(password, username, first_name, last_name):
    """Validate password against requirements"""
    # 1. At least 8 characters
    if len(password) < 8:
        return False
    
    # 2. A lowercase letter
    if not any(c.islower() for c in password):
        return False
    
    # 3. An uppercase letter
    if not any(c.isupper() for c in password):
        return False
    
    # 4. A number
    if not any(c.isdigit() for c in password):
        return False
    
    # 5. No parts of your username
    if username.lower() in password.lower():
        return False
    
    # 6. Does not include your first name
    if first_name.lower() in password.lower():
        return False
    
    # 7. Does not include your last name
    if last_name.lower() in password.lower():
        return False
    
    return True

def check_password_history(user_id, password_hash):
    """Check if password has been used before (all previously used passwords)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get ALL password hashes for this user
    cursor.execute("""
        SELECT pass_hash FROM password_history 
        WHERE user_id = ?
    """, (user_id,))
    
    all_passwords = cursor.fetchall()
    conn.close()
    
    # Check if the new password hash matches any previously used password
    for (used_hash,) in all_passwords:
        if used_hash == password_hash:
            return False  # Password has been used before
    
    return True  # Password is new

@app.route('/clear', methods=['GET'])
def clear_db():
    """Clear the database and recreate tables"""
    # Force create a new connection and drop the database
    if os.path.exists(db_name):
        os.remove(db_name)
    
    # Reset the database flag so it gets recreated
    global db_flag
    db_flag = False
    
    # Create fresh database
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS password_history")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email_address TEXT NOT NULL,
            pass_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            password_created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE password_history (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            pass_hash TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()
    return jsonify({"status": 1})

@app.route('/create_user', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        salt = request.form.get('salt')
        
        # Validate required fields
        if not all([first_name, last_name, username, email_address, password, salt]):
            return jsonify({"status": 4, "pass_hash": "NULL"})
        
        # Validate password requirements
        if not validate_password(password, username, first_name, last_name):
            return jsonify({"status": 4, "pass_hash": "NULL"})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if username already exists
        cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"status": 2, "pass_hash": "NULL"})
        
        # Check if email already exists
        cursor.execute("SELECT email_address FROM users WHERE email_address = ?", (email_address,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"status": 3, "pass_hash": "NULL"})
        
        # Hash the password
        pass_hash = hash_password(password, salt)
        
        # Insert user
        cursor.execute("""
            INSERT INTO users (first_name, last_name, username, email_address, pass_hash, salt)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (first_name, last_name, username, email_address, pass_hash, salt))
        
        # Get the user ID for password history
        user_id = cursor.lastrowid
        
        # Add password to history table
        cursor.execute("""
            INSERT INTO password_history (user_id, pass_hash)
            VALUES (?, ?)
        """, (user_id, pass_hash))
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": 1, "pass_hash": pass_hash})
        
    except Exception as e:
        return jsonify({"status": 4, "pass_hash": "NULL"})

@app.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT"""
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return jsonify({"status": 2, "jwt": "NULL"})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get user data
        cursor.execute("SELECT pass_hash, salt FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        
        if not user_data:
            conn.close()
            return jsonify({"status": 2, "jwt": "NULL"})
        
        stored_hash, salt = user_data
        
        # Verify password
        computed_hash = hash_password(password, salt)
        
        if computed_hash != stored_hash:
            conn.close()
            return jsonify({"status": 2, "jwt": "NULL"})
        
        # Generate JWT
        jwt_token = generate_jwt(username)
        
        conn.close()
        return jsonify({"status": 1, "jwt": jwt_token})
        
    except Exception as e:
        return jsonify({"status": 2, "jwt": "NULL"})

@app.route('/view', methods=['POST'])
def view_user():
    """View user data using JWT"""
    try:
        jwt_token = request.form.get('jwt')
        
        if not jwt_token:
            return jsonify({"status": 2, "data": "NULL"})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2, "data": "NULL"})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get user data
        cursor.execute("""
            SELECT username, email_address, first_name, last_name 
            FROM users WHERE username = ?
        """, (username,))
        user_data = cursor.fetchone()
        
        if not user_data:
            conn.close()
            return jsonify({"status": 2, "data": "NULL"})
        
        username, email_address, first_name, last_name = user_data
        
        conn.close()
        return jsonify({
            "status": 1, 
            "data": {
                "username": username,
                "email_address": email_address,
                "first_name": first_name,
                "last_name": last_name
            }
        })
        
    except Exception as e:
        return jsonify({"status": 2, "data": "NULL"})

@app.route('/update', methods=['POST'])
def update_user():
    """Update username or password with JWT validation"""
    try:
        jwt_token = request.form.get('jwt')
        
        if not jwt_token:
            return jsonify({"status": 3})
        
        # Verify JWT
        jwt_username = verify_jwt(jwt_token)
        if not jwt_username:
            return jsonify({"status": 3})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get user data
        cursor.execute("SELECT id, pass_hash, salt, first_name, last_name FROM users WHERE username = ?", (jwt_username,))
        user_data = cursor.fetchone()
        
        if not user_data:
            conn.close()
            return jsonify({"status": 2})
        
        user_id, stored_hash, salt, first_name, last_name = user_data
        
        # Check if this is a username update or password update
        username = request.form.get('username')
        new_username = request.form.get('new_username')
        password = request.form.get('password')
        new_password = request.form.get('new_password')
        
        if username and new_username:
            # Username update
            if username != jwt_username:
                conn.close()
                return jsonify({"status": 2})
            
            # Check if new username already exists
            cursor.execute("SELECT username FROM users WHERE username = ?", (new_username,))
            if cursor.fetchone():
                conn.close()
                return jsonify({"status": 2})
            
            # Update username
            cursor.execute("UPDATE users SET username = ? WHERE username = ?", (new_username, username))
            
            if cursor.rowcount == 0:
                conn.close()
                return jsonify({"status": 2})
            
        elif password and new_password:
            # Password update
            # Verify old password
            old_hash = hash_password(password, salt)
            if old_hash != stored_hash:
                conn.close()
                return jsonify({"status": 2})
            
            # Validate new password requirements
            if not validate_password(new_password, jwt_username, first_name, last_name):
                conn.close()
                return jsonify({"status": 2})
            
            # Check password history (cannot reuse any previously used password)
            new_hash = hash_password(new_password, salt)
            if not check_password_history(user_id, new_hash):
                conn.close()
                return jsonify({"status": 2})
            
            # Update password
            cursor.execute("UPDATE users SET pass_hash = ?, password_created_at = CURRENT_TIMESTAMP WHERE id = ?", 
                          (new_hash, user_id))
            
            # Add new password to history
            cursor.execute("INSERT INTO password_history (user_id, pass_hash) VALUES (?, ?)", 
                          (user_id, new_hash))
        else:
            conn.close()
            return jsonify({"status": 2})
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": 1})
        
    except Exception as e:
        return jsonify({"status": 2})

if __name__ == '__main__':
    app.run(debug=True)