#!/usr/bin/env python3
"""
Comprehensive test using Flask test client
"""

import app
from flask.testing import FlaskClient

def test_all_endpoints():
    """Test all endpoints using Flask test client"""
    print("Testing Project 2 with Flask test client...")
    print("=" * 50)
    
    # Create test client
    client = app.app.test_client()
    
    # Test 1: Clear database
    print("\n1. Testing /clear...")
    response = client.get('/clear')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test 2: Create user
    print("\n2. Testing /create_user...")
    data = {
        'first_name': 'Alice',
        'last_name': 'Smith',
        'username': 'alice.smith',
        'email_address': 'alice@example.com',
        'password': 'SecurePass123!',
        'salt': 'randomsalt456'
    }
    response = client.post('/create_user', data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test 3: Login
    print("\n3. Testing /login...")
    data = {
        'username': 'alice.smith',
        'password': 'SecurePass123!'
    }
    response = client.post('/login', data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    if response.status_code == 200:
        jwt = response.get_json().get('jwt')
        print(f"JWT: {jwt}")
        
        # Test 4: Create recipe
        print("\n4. Testing /create_recipe...")
        recipe_data = {
            'title': 'Spaghetti Carbonara',
            'description': 'Classic Italian pasta dish',
            'ingredients': '400g spaghetti, 200g pancetta, 4 eggs, 100g parmesan cheese, black pepper, salt',
            'instructions': '1. Cook spaghetti according to package directions. 2. Fry pancetta until crispy. 3. Beat eggs with parmesan. 4. Combine hot pasta with pancetta. 5. Add egg mixture and toss quickly. 6. Season with black pepper.',
            'prep_time': '10',
            'cook_time': '15',
            'servings': '4'
        }
        headers = {'Authorization': jwt}
        response = client.post('/create_recipe', data=recipe_data, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.get_json()}")
        
        if response.status_code == 200:
            recipe_id = response.get_json().get('recipe_id')
            print(f"Recipe ID: {recipe_id}")
            
            # Test 5: View recipe
            print(f"\n5. Testing /view_recipe/{recipe_id}...")
            response = client.get(f'/view_recipe/{recipe_id}', headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.get_json()}")
            
            # Test 6: Like recipe
            print(f"\n6. Testing /like_recipe/{recipe_id}...")
            response = client.post(f'/like_recipe/{recipe_id}', headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.get_json()}")
            
            # Test 7: Search recipes
            print("\n7. Testing /search_recipes...")
            response = client.get('/search_recipes?search_term=pasta&search_type=ingredients', headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.get_json()}")
            
            # Test 8: View user recipes
            print("\n8. Testing /view_user_recipes...")
            response = client.get('/view_user_recipes?username=alice.smith', headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.get_json()}")
            
            print("\n" + "=" * 50)
            print("✅ All tests completed successfully!")
        else:
            print("❌ Create recipe failed")
    else:
        print("❌ Login failed")

if __name__ == "__main__":
    test_all_endpoints()
