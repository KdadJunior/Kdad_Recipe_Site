#!/usr/bin/env python3
"""
Test script for Project 2 - The Meals LAN
Tests all endpoints to ensure they work correctly
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_clear_db():
    """Test clearing the database"""
    print("Testing /clear endpoint...")
    response = requests.get(f"{BASE_URL}/clear")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_create_user():
    """Test creating a user"""
    print("\nTesting /create_user endpoint...")
    data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email_address': 'john@example.com',
        'password': 'Password123!',
        'salt': 'randomsalt123'
    }
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_login():
    """Test user login"""
    print("\nTesting /login endpoint...")
    data = {
        'username': 'johndoe',
        'password': 'Password123!'
    }
    response = requests.post(f"{BASE_URL}/login", data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        jwt_token = response.json().get('jwt')
        print(f"JWT Token: {jwt_token}")
        return jwt_token
    return None

def test_create_recipe(jwt_token):
    """Test creating a recipe"""
    print("\nTesting /create_recipe endpoint...")
    data = {
        'title': 'Chocolate Chip Cookies',
        'description': 'Delicious homemade chocolate chip cookies',
        'ingredients': '2 cups flour, 1 cup sugar, 1/2 cup butter, 1 egg, 1 tsp vanilla, 1 cup chocolate chips',
        'instructions': '1. Mix dry ingredients. 2. Cream butter and sugar. 3. Add egg and vanilla. 4. Combine wet and dry ingredients. 5. Add chocolate chips. 6. Bake at 375°F for 10-12 minutes.',
        'prep_time': '15',
        'cook_time': '12',
        'servings': '24'
    }
    headers = {'Authorization': jwt_token}
    response = requests.post(f"{BASE_URL}/create_recipe", data=data, headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        recipe_id = response.json().get('recipe_id')
        print(f"Recipe ID: {recipe_id}")
        return recipe_id
    return None

def test_view_recipe(jwt_token, recipe_id):
    """Test viewing a recipe"""
    print(f"\nTesting /view_recipe/{recipe_id} endpoint...")
    headers = {'Authorization': jwt_token}
    response = requests.get(f"{BASE_URL}/view_recipe/{recipe_id}", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_like_recipe(jwt_token, recipe_id):
    """Test liking a recipe"""
    print(f"\nTesting /like_recipe/{recipe_id} endpoint...")
    headers = {'Authorization': jwt_token}
    response = requests.post(f"{BASE_URL}/like_recipe/{recipe_id}", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_search_recipes(jwt_token):
    """Test searching recipes"""
    print("\nTesting /search_recipes endpoint...")
    headers = {'Authorization': jwt_token}
    params = {
        'search_term': 'chocolate',
        'search_type': 'ingredients'
    }
    response = requests.get(f"{BASE_URL}/search_recipes", headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_view_user_recipes(jwt_token):
    """Test viewing user recipes"""
    print("\nTesting /view_user_recipes endpoint...")
    headers = {'Authorization': jwt_token}
    params = {'username': 'johndoe'}
    response = requests.get(f"{BASE_URL}/view_user_recipes", headers=headers, params=params)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("Starting Project 2 Tests...")
    print("=" * 50)
    
    # Test database clearing
    if not test_clear_db():
        print("❌ Clear database test failed")
        return
    
    # Test user creation
    if not test_create_user():
        print("❌ Create user test failed")
        return
    
    # Test login
    jwt_token = test_login()
    if not jwt_token:
        print("❌ Login test failed")
        return
    
    # Test recipe creation
    recipe_id = test_create_recipe(jwt_token)
    if not recipe_id:
        print("❌ Create recipe test failed")
        return
    
    # Test viewing recipe
    if not test_view_recipe(jwt_token, recipe_id):
        print("❌ View recipe test failed")
        return
    
    # Test liking recipe
    if not test_like_recipe(jwt_token, recipe_id):
        print("❌ Like recipe test failed")
        return
    
    # Test searching recipes
    if not test_search_recipes(jwt_token):
        print("❌ Search recipes test failed")
        return
    
    # Test viewing user recipes
    if not test_view_user_recipes(jwt_token):
        print("❌ View user recipes test failed")
        return
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! Project 2 is working correctly.")

if __name__ == "__main__":
    main()
