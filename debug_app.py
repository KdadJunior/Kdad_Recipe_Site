#!/usr/bin/env python3
"""
Debug script to test Flask app routes
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_routes():
    """Test all routes to see which ones work"""
    print("Testing all routes...")
    
    # Test clear
    print("\n1. Testing /clear...")
    try:
        response = requests.get(f"{BASE_URL}/clear")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test create_user
    print("\n2. Testing /create_user...")
    try:
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email_address': 'test@example.com',
            'password': 'Password123!',
            'salt': 'salt123'
        }
        response = requests.post(f"{BASE_URL}/create_user", data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test login
    print("\n3. Testing /login...")
    try:
        data = {
            'username': 'testuser',
            'password': 'Password123!'
        }
        response = requests.post(f"{BASE_URL}/login", data=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            jwt = response.json().get('jwt')
            print(f"JWT: {jwt}")
            
            # Test create_recipe with JWT
            print("\n4. Testing /create_recipe...")
            try:
                recipe_data = {
                    'title': 'Test Recipe',
                    'ingredients': 'test ingredients',
                    'instructions': 'test instructions'
                }
                headers = {'Authorization': jwt}
                response = requests.post(f"{BASE_URL}/create_recipe", data=recipe_data, headers=headers)
                print(f"Status: {response.status_code}")
                print(f"Response: {response.text}")
            except Exception as e:
                print(f"Error: {e}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_routes()
