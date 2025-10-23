#!/usr/bin/env python3
"""
Simple test to debug the issue
"""

import requests
import json

# First, let's test the basic endpoints
BASE_URL = "http://127.0.0.1:5000"

print("Testing basic endpoints...")

# Test clear
print("\n1. Testing /clear...")
response = requests.get(f"{BASE_URL}/clear")
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# Test create_user
print("\n2. Testing /create_user...")
data = {
    'first_name': 'Test',
    'last_name': 'User',
    'username': 'testuser2',
    'email_address': 'test2@example.com',
    'password': 'Password123!',
    'salt': 'salt123'
}
response = requests.post(f"{BASE_URL}/create_user", data=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# Test login
print("\n3. Testing /login...")
data = {
    'username': 'testuser2',
    'password': 'Password123!'
}
response = requests.post(f"{BASE_URL}/login", data=data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    jwt = response.json().get('jwt')
    print(f"JWT: {jwt}")
    
    # Test create_recipe
    print("\n4. Testing /create_recipe...")
    recipe_data = {
        'title': 'Test Recipe',
        'ingredients': 'test ingredients',
        'instructions': 'test instructions'
    }
    headers = {'Authorization': jwt}
    response = requests.post(f"{BASE_URL}/create_recipe", data=recipe_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test with different approach
    print("\n5. Testing /create_recipe with form data...")
    response = requests.post(f"{BASE_URL}/create_recipe", 
                           data=recipe_data, 
                           headers=headers,
                           timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Test if the route exists at all
    print("\n6. Testing route existence...")
    try:
        response = requests.get(f"{BASE_URL}/create_recipe")
        print(f"GET Status: {response.status_code}")
        print(f"GET Response: {response.text}")
    except Exception as e:
        print(f"GET Error: {e}")
