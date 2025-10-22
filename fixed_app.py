#!/usr/bin/env python3
"""
Fixed version of the Flask app
"""

import sqlite3
import os
import hashlib
import hmac
import base64
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
db_name = "project2.db"
sql_file = "project2.sql"
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

def get_jwt_from_header():
    """Extract JWT from Authorization header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    return auth_header

# Project 1 endpoints (adapted for Project 2)
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
    cursor.execute("DROP TABLE IF EXISTS likes")
    cursor.execute("DROP TABLE IF EXISTS recipes")
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
    cursor.execute("""
        CREATE TABLE recipes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            prep_time INTEGER,
            cook_time INTEGER,
            servings INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    cursor.execute("""
        CREATE TABLE likes (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            recipe_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (recipe_id) REFERENCES recipes (id),
            UNIQUE(user_id, recipe_id)
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

# Project 2 specific endpoints
@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    """Create a new recipe"""
    try:
        # Get JWT from Authorization header
        jwt_token = get_jwt_from_header()
        if not jwt_token:
            return jsonify({"status": 2, "recipe_id": "NULL"})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2, "recipe_id": "NULL"})
        
        # Get recipe data from form
        title = request.form.get('title')
        description = request.form.get('description', '')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        prep_time = request.form.get('prep_time')
        cook_time = request.form.get('cook_time')
        servings = request.form.get('servings')
        
        # Validate required fields
        if not all([title, ingredients, instructions]):
            return jsonify({"status": 2, "recipe_id": "NULL"})
        
        # Convert numeric fields
        prep_time = int(prep_time) if prep_time else None
        cook_time = int(cook_time) if cook_time else None
        servings = int(servings) if servings else None
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        if not user_data:
            conn.close()
            return jsonify({"status": 2, "recipe_id": "NULL"})
        
        user_id = user_data[0]
        
        # Insert recipe
        cursor.execute("""
            INSERT INTO recipes (user_id, title, description, ingredients, instructions, prep_time, cook_time, servings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, title, description, ingredients, instructions, prep_time, cook_time, servings))
        
        recipe_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({"status": 1, "recipe_id": recipe_id})
        
    except Exception as e:
        return jsonify({"status": 2, "recipe_id": "NULL"})

@app.route('/view_recipe/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    """View a specific recipe"""
    try:
        # Get JWT from Authorization header
        jwt_token = get_jwt_from_header()
        if not jwt_token:
            return jsonify({"status": 2, "data": "NULL"})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2, "data": "NULL"})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get recipe data
        cursor.execute("""
            SELECT r.id, r.title, r.description, r.ingredients, r.instructions, 
                   r.prep_time, r.cook_time, r.servings, r.created_at, u.username
            FROM recipes r
            JOIN users u ON r.user_id = u.id
            WHERE r.id = ?
        """, (recipe_id,))
        
        recipe_data = cursor.fetchone()
        if not recipe_data:
            conn.close()
            return jsonify({"status": 2, "data": "NULL"})
        
        recipe_id, title, description, ingredients, instructions, prep_time, cook_time, servings, created_at, author = recipe_data
        
        # Get like count
        cursor.execute("SELECT COUNT(*) FROM likes WHERE recipe_id = ?", (recipe_id,))
        like_count = cursor.fetchone()[0]
        
        # Check if current user has liked this recipe
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        user_id = user_data[0] if user_data else None
        
        user_liked = False
        if user_id:
            cursor.execute("SELECT id FROM likes WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
            user_liked = cursor.fetchone() is not None
        
        conn.close()
        
        return jsonify({
            "status": 1,
            "data": {
                "recipe_id": recipe_id,
                "title": title,
                "description": description,
                "ingredients": ingredients,
                "instructions": instructions,
                "prep_time": prep_time,
                "cook_time": cook_time,
                "servings": servings,
                "created_at": created_at,
                "author": author,
                "like_count": like_count,
                "user_liked": user_liked
            }
        })
        
    except Exception as e:
        return jsonify({"status": 2, "data": "NULL"})

@app.route('/like_recipe/<int:recipe_id>', methods=['POST'])
def like_recipe(recipe_id):
    """Like or unlike a recipe"""
    try:
        # Get JWT from Authorization header
        jwt_token = get_jwt_from_header()
        if not jwt_token:
            return jsonify({"status": 2, "like_count": "NULL"})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2, "like_count": "NULL"})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        if not user_data:
            conn.close()
            return jsonify({"status": 2, "like_count": "NULL"})
        
        user_id = user_data[0]
        
        # Check if recipe exists
        cursor.execute("SELECT id FROM recipes WHERE id = ?", (recipe_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"status": 2, "like_count": "NULL"})
        
        # Check if user already liked this recipe
        cursor.execute("SELECT id FROM likes WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
        existing_like = cursor.fetchone()
        
        if existing_like:
            # Unlike the recipe
            cursor.execute("DELETE FROM likes WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
        else:
            # Like the recipe
            cursor.execute("INSERT INTO likes (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
        
        # Get updated like count
        cursor.execute("SELECT COUNT(*) FROM likes WHERE recipe_id = ?", (recipe_id,))
        like_count = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": 1, "like_count": like_count})
        
    except Exception as e:
        return jsonify({"status": 2, "like_count": "NULL"})

@app.route('/search_recipes', methods=['GET'])
def search_recipes():
    """Search recipes by title or ingredients"""
    try:
        # Get JWT from Authorization header
        jwt_token = get_jwt_from_header()
        if not jwt_token:
            return jsonify({"status": 2, "data": "NULL"})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2, "data": "NULL"})
        
        # Get search parameters
        search_term = request.args.get('search_term', '')
        search_type = request.args.get('search_type', 'title')  # 'title' or 'ingredients'
        
        if not search_term:
            return jsonify({"status": 2, "data": "NULL"})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Build search query
        if search_type == 'ingredients':
            query = """
                SELECT r.id, r.title, r.description, r.ingredients, r.instructions, 
                       r.prep_time, r.cook_time, r.servings, r.created_at, u.username,
                       COUNT(l.id) as like_count
                FROM recipes r
                JOIN users u ON r.user_id = u.id
                LEFT JOIN likes l ON r.id = l.recipe_id
                WHERE r.ingredients LIKE ?
                GROUP BY r.id
                ORDER BY r.created_at DESC
            """
            search_param = f"%{search_term}%"
        else:  # search_type == 'title'
            query = """
                SELECT r.id, r.title, r.description, r.ingredients, r.instructions, 
                       r.prep_time, r.cook_time, r.servings, r.created_at, u.username,
                       COUNT(l.id) as like_count
                FROM recipes r
                JOIN users u ON r.user_id = u.id
                LEFT JOIN likes l ON r.id = l.recipe_id
                WHERE r.title LIKE ?
                GROUP BY r.id
                ORDER BY r.created_at DESC
            """
            search_param = f"%{search_term}%"
        
        cursor.execute(query, (search_param,))
        recipes = cursor.fetchall()
        
        # Format results
        results = []
        for recipe in recipes:
            recipe_id, title, description, ingredients, instructions, prep_time, cook_time, servings, created_at, author, like_count = recipe
            
            results.append({
                "recipe_id": recipe_id,
                "title": title,
                "description": description,
                "ingredients": ingredients,
                "instructions": instructions,
                "prep_time": prep_time,
                "cook_time": cook_time,
                "servings": servings,
                "created_at": created_at,
                "author": author,
                "like_count": like_count
            })
        
        conn.close()
        
        return jsonify({"status": 1, "data": results})
        
    except Exception as e:
        return jsonify({"status": 2, "data": "NULL"})

@app.route('/view_user_recipes', methods=['GET'])
def view_user_recipes():
    """View all recipes by a specific user"""
    try:
        # Get JWT from Authorization header
        jwt_token = get_jwt_from_header()
        if not jwt_token:
            return jsonify({"status": 2, "data": "NULL"})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2, "data": "NULL"})
        
        # Get target username from query parameter
        target_username = request.args.get('username')
        if not target_username:
            return jsonify({"status": 2, "data": "NULL"})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if target user exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (target_username,))
        target_user = cursor.fetchone()
        if not target_user:
            conn.close()
            return jsonify({"status": 2, "data": "NULL"})
        
        target_user_id = target_user[0]
        
        # Get recipes by target user
        cursor.execute("""
            SELECT r.id, r.title, r.description, r.ingredients, r.instructions, 
                   r.prep_time, r.cook_time, r.servings, r.created_at, u.username,
                   COUNT(l.id) as like_count
            FROM recipes r
            JOIN users u ON r.user_id = u.id
            LEFT JOIN likes l ON r.id = l.recipe_id
            WHERE r.user_id = ?
            GROUP BY r.id
            ORDER BY r.created_at DESC
        """, (target_user_id,))
        
        recipes = cursor.fetchall()
        
        # Format results
        results = []
        for recipe in recipes:
            recipe_id, title, description, ingredients, instructions, prep_time, cook_time, servings, created_at, author, like_count = recipe
            
            results.append({
                "recipe_id": recipe_id,
                "title": title,
                "description": description,
                "ingredients": ingredients,
                "instructions": instructions,
                "prep_time": prep_time,
                "cook_time": cook_time,
                "servings": servings,
                "created_at": created_at,
                "author": author,
                "like_count": like_count
            })
        
        conn.close()
        
        return jsonify({"status": 1, "data": results})
        
    except Exception as e:
        return jsonify({"status": 2, "data": "NULL"})

if __name__ == '__main__':
    app.run(debug=True)
