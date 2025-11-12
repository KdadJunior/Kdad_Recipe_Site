#!/usr/bin/env python3
"""
Flask app for Project 2 - The Meals LAN
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
    """Create database from SQL file"""
    conn = sqlite3.connect(db_name)
    
    with open(sql_file, 'r') as sql_startup:
        init_db = sql_startup.read()
    cursor = conn.cursor()
    cursor.executescript(init_db)
    conn.commit()
    conn.close()
    global db_flag
    db_flag = True

def get_db():
    """Get database connection, creating if necessary"""
    if not db_flag:
        create_db()
    conn = sqlite3.connect(db_name)
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def hash_password(password, salt):
    """Hash password using SHA-256 with salt"""
    combined = password + salt
    return hashlib.sha256(combined.encode()).hexdigest()

def generate_jwt(username):
    """Generate JWT token - payload only contains username"""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"username": username}
    
    # Encode header and payload
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

def get_jwt_from_header():
    """Extract JWT from Authorization header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    return auth_header

def get_post_param(param_name):
    """Robustly extract a POST parameter from form, JSON, or raw body."""
    # 1) Standard form field
    value = request.form.get(param_name)
    if value is not None and value != "":
        return value
    # 2) JSON body
    try:
        json_body = request.get_json(silent=True)
        if isinstance(json_body, dict) and param_name in json_body and json_body[param_name] != "":
            return json_body[param_name]
    except:
        pass
    # 3) URL-encoded raw body fallback
    try:
        from urllib.parse import parse_qs
        raw = request.get_data(as_text=True) or ""
        parsed = parse_qs(raw, keep_blank_values=True)
        if param_name in parsed and len(parsed[param_name]) > 0:
            return parsed[param_name][0]
    except:
        pass
    return None

@app.route('/clear', methods=['GET'])
def clear_db():
    """Clear the database and recreate tables"""
    conn = None
    try:
        # Close any open connections first
        # Reset the database flag so it gets recreated
        global db_flag
        db_flag = False
        
        # Try to close any existing connections by attempting to connect and close
        try:
            if os.path.exists(db_name):
                temp_conn = sqlite3.connect(db_name)
                temp_conn.close()
        except:
            pass
        
        # Remove the database file (as per spec: "It is recommended that you simply delete the .db file")
        if os.path.exists(db_name):
            os.remove(db_name)
        
        # Create fresh database
        create_db()
        return jsonify({"status": 1})
    except Exception as e:
        # Ensure no connection is left open
        if conn:
            try:
                conn.close()
            except:
                pass
        # Even on error, try to recreate database
        try:
            if os.path.exists(db_name):
                os.remove(db_name)
            db_flag = False
            create_db()
        except:
            pass
        return jsonify({"status": 1})

@app.route('/create_user', methods=['POST'])
def create_user():
    """Create a new user"""
    conn = None
    try:
        first_name = get_post_param('first_name')
        last_name = get_post_param('last_name')
        username = get_post_param('username')
        email_address = get_post_param('email_address')
        password = get_post_param('password')
        salt = get_post_param('salt')
        
        # Validate required fields
        if not all([first_name, last_name, username, email_address, password, salt]):
            return jsonify({"status": 4, "pass_hash": "NULL"})
        
        # Validate field lengths (max 254 characters)
        if len(first_name) > 254 or len(last_name) > 254 or len(username) > 254 or len(email_address) > 254 or len(password) > 254 or len(salt) > 254:
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
        if conn:
            conn.close()
        return jsonify({"status": 4, "pass_hash": "NULL"})

@app.route('/login', methods=['POST'])
def login():
    """Authenticate user and return JWT"""
    conn = None
    try:
        username = get_post_param('username')
        password = get_post_param('password')
        
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
        if conn:
            conn.close()
        return jsonify({"status": 2, "jwt": "NULL"})

@app.route('/create_recipe', methods=['POST'])
def create_recipe():
    """Create a new recipe"""
    conn = None
    try:
        # Get JWT from Authorization header
        jwt_token = get_jwt_from_header()
        if not jwt_token:
            return jsonify({"status": 2})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2})
        
        # Get recipe data from form
        name = get_post_param('name')
        description = get_post_param('description')
        recipe_id = get_post_param('recipe_id')
        ingredients = get_post_param('ingredients')  # JSON string or None
        
        # Validate required fields
        if not all([name, description, recipe_id]):
            return jsonify({"status": 2})
        
        # Convert recipe_id to int
        try:
            recipe_id = int(recipe_id)
        except:
            return jsonify({"status": 2})
        
        # Parse ingredients if provided
        ingredients_list = None
        if ingredients:
            try:
                ingredients_list = json.loads(ingredients)
                # Convert list to JSON string for storage
                ingredients = json.dumps(ingredients_list)
            except:
                return jsonify({"status": 2})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if recipe_id already exists
        cursor.execute("SELECT recipe_id FROM recipes WHERE recipe_id = ?", (recipe_id,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"status": 2})
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        if not user_data:
            conn.close()
            return jsonify({"status": 2})
        
        user_id = user_data[0]
        
        # Insert recipe
        cursor.execute("""
            INSERT INTO recipes (recipe_id, user_id, name, description)
            VALUES (?, ?, ?, ?)
        """, (recipe_id, user_id, name, description))
        # Record insertion order for stable tie-breaking on feed/popular
        cursor.execute("INSERT INTO recipe_inserts (recipe_id) VALUES (?)", (recipe_id,))
        
        # Insert ingredients if provided
        if ingredients_list:
            for ingredient in ingredients_list:
                cursor.execute("""
                    INSERT INTO recipe_ingredients (recipe_id, ingredient)
                    VALUES (?, ?)
                """, (recipe_id, ingredient))
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": 1})
        
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"status": 2})

@app.route('/like', methods=['POST'])
def like():
    """Like a recipe"""
    conn = None
    try:
        # Get JWT from Authorization header
        jwt_token = get_jwt_from_header()
        if not jwt_token:
            return jsonify({"status": 2})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2})
        
        # Get recipe_id from form
        recipe_id = get_post_param('recipe_id')
        if not recipe_id:
            return jsonify({"status": 2})
        
        try:
            recipe_id = int(recipe_id)
        except:
            return jsonify({"status": 2})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        if not user_data:
            conn.close()
            return jsonify({"status": 2})
        
        user_id = user_data[0]
        
        # Check if recipe exists
        cursor.execute("SELECT recipe_id FROM recipes WHERE recipe_id = ?", (recipe_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"status": 2})
        
        # Check if user already liked this recipe
        cursor.execute("SELECT id FROM likes WHERE user_id = ? AND recipe_id = ?", (user_id, recipe_id))
        existing_like = cursor.fetchone()
        
        if existing_like:
            # Already liked, return error
            conn.close()
            return jsonify({"status": 2})
        
        # Like the recipe
        cursor.execute("INSERT INTO likes (user_id, recipe_id) VALUES (?, ?)", (user_id, recipe_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": 1})
        
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"status": 2})

@app.route('/view_recipe/<int:recipe_id>', methods=['GET'])
def view_recipe(recipe_id):
    """View a specific recipe"""
    conn = None
    try:
        # Get JWT from Authorization header
        jwt_token = get_jwt_from_header()
        if not jwt_token:
            return jsonify({"status": 2, "data": "NULL"})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2, "data": "NULL"})
        
        # Get which attributes to return
        want_name = request.args.get('name') == 'True'
        want_description = request.args.get('description') == 'True'
        want_likes = request.args.get('likes') == 'True'
        want_ingredients = request.args.get('ingredients') == 'True'
        
        # If no attributes requested, return empty data with status 1
        if not any([want_name, want_description, want_likes, want_ingredients]):
            return jsonify({"status": 1, "data": {}})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get recipe data
        cursor.execute("""
            SELECT name, description
            FROM recipes
            WHERE recipe_id = ?
        """, (recipe_id,))
        
        recipe_data = cursor.fetchone()
        if not recipe_data:
            conn.close()
            return jsonify({"status": 2, "data": "NULL"})
        
        name, description = recipe_data
        
        # Get like count
        cursor.execute("SELECT COUNT(*) FROM likes WHERE recipe_id = ?", (recipe_id,))
        like_count = cursor.fetchone()[0]
        
        # Get ingredients if requested
        ingredients_list = []
        if want_ingredients:
            cursor.execute("SELECT ingredient FROM recipe_ingredients WHERE recipe_id = ? ORDER BY ingredient", (recipe_id,))
            ingredients_list = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        
        # Build response data with only requested fields
        data = {}
        if want_name:
            data['name'] = name
        if want_description:
            data['description'] = description
        if want_likes:
            data['likes'] = str(like_count)
        if want_ingredients:
            data['ingredients'] = ingredients_list
        
        return jsonify({"status": 1, "data": data})
        
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"status": 2, "data": "NULL"})

@app.route('/follow', methods=['POST'])
def follow():
    """Follow a user"""
    conn = None
    try:
        # Get JWT from Authorization header
        jwt_token = get_jwt_from_header()
        if not jwt_token:
            return jsonify({"status": 2})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2})
        
        # Get username to follow from form
        follow_username = get_post_param('username')
        if not follow_username:
            return jsonify({"status": 2})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get follower user ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        follower_data = cursor.fetchone()
        if not follower_data:
            conn.close()
            return jsonify({"status": 2})
        
        follower_id = follower_data[0]
        
        # Get user to follow ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (follow_username,))
        following_data = cursor.fetchone()
        if not following_data:
            conn.close()
            return jsonify({"status": 2})
        
        following_id = following_data[0]
        
        # Cannot follow yourself
        if follower_id == following_id:
            conn.close()
            return jsonify({"status": 2})
        
        # Check if already following
        cursor.execute("SELECT id FROM follows WHERE follower_id = ? AND following_id = ?", (follower_id, following_id))
        if cursor.fetchone():
            conn.close()
            return jsonify({"status": 2})
        
        # Insert follow relationship
        cursor.execute("INSERT INTO follows (follower_id, following_id) VALUES (?, ?)", (follower_id, following_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": 1})
        
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"status": 2})

@app.route('/search', methods=['GET'])
def search():
    """Search recipes by feed, popular, or ingredients"""
    conn = None
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
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        if not user_data:
            conn.close()
            return jsonify({"status": 2, "data": "NULL"})
        
        user_id = user_data[0]
        
        # Check which search type
        feed = request.args.get('feed') == 'True'
        popular = request.args.get('popular') == 'True'
        ingredients_param = request.args.get('ingredients')
        
        recipes = []
        
        if feed:
            # Return 2 most recent recipes from users that the requesting user follows
            cursor.execute("""
                SELECT r.recipe_id, r.name, r.description, r.created_at
                FROM recipes r
                JOIN follows f ON r.user_id = f.following_id
                LEFT JOIN recipe_inserts ri ON ri.recipe_id = r.recipe_id
                WHERE f.follower_id = ?
                ORDER BY r.created_at DESC, ri.seq DESC
                LIMIT 2
            """, (user_id,))
            recipes = cursor.fetchall()
            
        elif popular:
            # Return top 2 recipes by like count
            cursor.execute("""
                SELECT r.recipe_id, r.name, r.description, r.created_at
                FROM recipes r
                LEFT JOIN likes l ON r.recipe_id = l.recipe_id
                LEFT JOIN recipe_inserts ri ON ri.recipe_id = r.recipe_id
                GROUP BY r.recipe_id
                ORDER BY COUNT(l.id) DESC, r.created_at DESC, ri.seq DESC
                LIMIT 2
            """)
            recipes = cursor.fetchall()
            
        elif ingredients_param:
            # Parse ingredients list
            try:
                ingredients_list = json.loads(ingredients_param)
                if not isinstance(ingredients_list, list):
                    conn.close()
                    return jsonify({"status": 2, "data": "NULL"})
            except:
                conn.close()
                return jsonify({"status": 2, "data": "NULL"})
            
            # If the provided ingredients list is empty, no recipe should match
            # because a valid recipe must contain at least one ingredient.
            if len(ingredients_list) == 0:
                conn.close()
                return jsonify({"status": 1, "data": {}})

            # Get all recipes that only contain ingredients in the provided list
            # Find recipes where ALL ingredients are in the provided list
            placeholders = ','.join(['?'] * len(ingredients_list))
            cursor.execute(f"""
                SELECT DISTINCT r.recipe_id, r.name, r.description
                FROM recipes r
                WHERE NOT EXISTS (
                    SELECT 1 FROM recipe_ingredients ri
                    WHERE ri.recipe_id = r.recipe_id
                    AND ri.ingredient NOT IN ({placeholders})
                )
                AND EXISTS (
                    SELECT 1 FROM recipe_ingredients ri
                    WHERE ri.recipe_id = r.recipe_id
                )
            """, ingredients_list)
            recipes = cursor.fetchall()
        else:
            conn.close()
            return jsonify({"status": 2, "data": "NULL"})
        
        # Format results
        result_data = {}
        for recipe in recipes:
            recipe_id = recipe[0]
            name = recipe[1]
            description = recipe[2]
            
            # Get like count
            cursor.execute("SELECT COUNT(*) FROM likes WHERE recipe_id = ?", (recipe_id,))
            like_count = cursor.fetchone()[0]
            
            # Get ingredients from recipe_ingredients table
            cursor.execute("SELECT ingredient FROM recipe_ingredients WHERE recipe_id = ? ORDER BY ingredient", (recipe_id,))
            ingredients_list = [row[0] for row in cursor.fetchall()]
            
            result_data[str(recipe_id)] = {
                "name": name,
                "description": description,
                "ingredients": ingredients_list,
                "likes": str(like_count)
            }
        
        conn.close()
        
        # Spec says "we will assume there is always something to return"
        # But handle edge case gracefully - return status 1 with empty dict
        return jsonify({"status": 1, "data": result_data})
        
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"status": 2, "data": "NULL"})

@app.route('/delete', methods=['POST'])
def delete():
    """Delete a user account"""
    conn = None
    try:
        # Get JWT from Authorization header
        jwt_token = get_jwt_from_header()
        if not jwt_token:
            return jsonify({"status": 2})
        
        # Verify JWT
        username = verify_jwt(jwt_token)
        if not username:
            return jsonify({"status": 2})
        
        # Get username to delete from form
        delete_username = get_post_param('username')
        if not delete_username:
            return jsonify({"status": 2})
        
        # User can only delete their own account
        if username != delete_username:
            return jsonify({"status": 2})
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Get user ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        if not user_data:
            conn.close()
            return jsonify({"status": 2})
        
        user_id = user_data[0]
        
        # Delete user (cascading deletes will handle recipes, likes, follows)
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({"status": 1})
        
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"status": 2})

if __name__ == '__main__':
    app.run(debug=False)
