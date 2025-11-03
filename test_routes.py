#!/usr/bin/env python3
"""
Test routes directly
"""

import app
from flask import Flask
from flask.testing import FlaskClient

# Create a test client
client = app.app.test_client()

def test_routes():
    """Test all routes"""
    print("Testing routes with test client...")
    
    # Test clear
    print("\n1. Testing /clear...")
    response = client.get('/clear')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test create_user
    print("\n2. Testing /create_user...")
    data = {
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser3',
        'email_address': 'test3@example.com',
        'password': 'Password123!',
        'salt': 'salt123'
    }
    response = client.post('/create_user', data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test login
    print("\n3. Testing /login...")
    data = {
        'username': 'testuser3',
        'password': 'Password123!'
    }
    response = client.post('/login', data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    if response.status_code == 200:
        jwt = response.get_json().get('jwt')
        print(f"JWT: {jwt}")
        
        # Test create_recipe
        print("\n4. Testing /create_recipe...")
        recipe_data = {
            'title': 'Test Recipe',
            'ingredients': 'test ingredients',
            'instructions': 'test instructions'
        }
        headers = {'Authorization': jwt}
        response = client.post('/create_recipe', data=recipe_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_json()}")

if __name__ == "__main__":
    test_routes()
