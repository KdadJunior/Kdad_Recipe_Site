#!/usr/bin/env python3
"""
Example requests for Project 2 - The Meals LAN
Demonstrates how to use the API endpoints
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def example_create_user():
    """Example: Create a new user"""
    print("Creating a new user...")
    data = {
        'first_name': 'Alice',
        'last_name': 'Smith',
        'username': 'alice.smith',
        'email_address': 'alice@example.com',
        'password': 'SecurePass123!',
        'salt': 'randomsalt456'
    }
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    print(f"Response: {response.json()}")
    return response.json()

def example_login():
    """Example: Login and get JWT token"""
    print("\nLogging in...")
    data = {
        'username': 'alice.smith',
        'password': 'SecurePass123!'
    }
    response = requests.post(f"{BASE_URL}/login", data=data)
    print(f"Response: {response.json()}")
    
    if response.json().get('status') == 1:
        jwt_token = response.json().get('jwt')
        print(f"JWT Token: {jwt_token}")
        return jwt_token
    return None

def example_create_recipe(jwt_token):
    """Example: Create a recipe"""
    print("\nCreating a recipe...")
    data = {
        'title': 'Spaghetti Carbonara',
        'description': 'Classic Italian pasta dish',
        'ingredients': '400g spaghetti, 200g pancetta, 4 eggs, 100g parmesan cheese, black pepper, salt',
        'instructions': '1. Cook spaghetti according to package directions. 2. Fry pancetta until crispy. 3. Beat eggs with parmesan. 4. Combine hot pasta with pancetta. 5. Add egg mixture and toss quickly. 6. Season with black pepper.',
        'prep_time': '10',
        'cook_time': '15',
        'servings': '4'
    }
    headers = {'Authorization': jwt_token}
    response = requests.post(f"{BASE_URL}/create_recipe", data=data, headers=headers)
    print(f"Response: {response.json()}")
    
    if response.json().get('status') == 1:
        recipe_id = response.json().get('recipe_id')
        print(f"Recipe ID: {recipe_id}")
        return recipe_id
    return None

def example_view_recipe(jwt_token, recipe_id):
    """Example: View a recipe"""
    print(f"\nViewing recipe {recipe_id}...")
    headers = {'Authorization': jwt_token}
    response = requests.get(f"{BASE_URL}/view_recipe/{recipe_id}", headers=headers)
    print(f"Response: {response.json()}")

def example_like_recipe(jwt_token, recipe_id):
    """Example: Like a recipe"""
    print(f"\nLiking recipe {recipe_id}...")
    headers = {'Authorization': jwt_token}
    response = requests.post(f"{BASE_URL}/like_recipe/{recipe_id}", headers=headers)
    print(f"Response: {response.json()}")

def example_search_recipes(jwt_token):
    """Example: Search recipes"""
    print("\nSearching for recipes with 'pasta' in ingredients...")
    headers = {'Authorization': jwt_token}
    params = {
        'search_term': 'pasta',
        'search_type': 'ingredients'
    }
    response = requests.get(f"{BASE_URL}/search_recipes", headers=headers, params=params)
    print(f"Response: {response.json()}")

def example_view_user_recipes(jwt_token):
    """Example: View user's recipes"""
    print("\nViewing user's recipes...")
    headers = {'Authorization': jwt_token}
    params = {'username': 'alice.smith'}
    response = requests.get(f"{BASE_URL}/view_user_recipes", headers=headers, params=params)
    print(f"Response: {response.json()}")

def main():
    """Run example requests"""
    print("Project 2 - The Meals LAN Example Requests")
    print("=" * 50)
    
    # Clear database first
    print("Clearing database...")
    response = requests.get(f"{BASE_URL}/clear")
    print(f"Clear response: {response.json()}")
    
    # Create user
    user_result = example_create_user()
    if user_result.get('status') != 1:
        print("Failed to create user")
        return
    
    # Login
    jwt_token = example_login()
    if not jwt_token:
        print("Failed to login")
        return
    
    # Create recipe
    recipe_id = example_create_recipe(jwt_token)
    if not recipe_id:
        print("Failed to create recipe")
        return
    
    # View recipe
    example_view_recipe(jwt_token, recipe_id)
    
    # Like recipe
    example_like_recipe(jwt_token, recipe_id)
    
    # Search recipes
    example_search_recipes(jwt_token)
    
    # View user recipes
    example_view_user_recipes(jwt_token)
    
    print("\n" + "=" * 50)
    print("Example requests completed!")

if __name__ == "__main__":
    main()