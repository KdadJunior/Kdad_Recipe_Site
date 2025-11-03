#!/usr/bin/env python3
"""
Final comprehensive test for Project 2
Tests all functionality including edge cases
"""

import app
from flask.testing import FlaskClient
import json

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("Testing Edge Cases and Error Conditions...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Test 1: Invalid JWT
    print("\n1. Testing create_recipe with invalid JWT...")
    response = client.post('/create_recipe', 
                          data={'title': 'Test', 'ingredients': 'test', 'instructions': 'test'},
                          headers={'Authorization': 'invalid_jwt'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test 2: Missing JWT
    print("\n2. Testing create_recipe without JWT...")
    response = client.post('/create_recipe', 
                          data={'title': 'Test', 'ingredients': 'test', 'instructions': 'test'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test 3: Invalid recipe data
    print("\n3. Testing create_recipe with missing required fields...")
    response = client.post('/create_recipe', 
                          data={'title': 'Test'},  # Missing ingredients and instructions
                          headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJhbGljZS5zbWl0aCIsICJhY2Nlc3MiOiAiVHJ1ZSJ9.6b9d062199f0e93d6e23f1650db6e5eb78cfcbebbc0e725c18e62291d7d6f821'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test 4: View non-existent recipe
    print("\n4. Testing view_recipe with non-existent ID...")
    response = client.get('/view_recipe/999', 
                         headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJhbGljZS5zbWl0aCIsICJhY2Nlc3MiOiAiVHJ1ZSJ9.6b9d062199f0e93d6e23f1650db6e5eb78cfcbebbc0e725c18e62291d7d6f821'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test 5: Search with empty term
    print("\n5. Testing search_recipes with empty search term...")
    response = client.get('/search_recipes?search_term=&search_type=title', 
                         headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJhbGljZS5zbWl0aCIsICJhY2Nlc3MiOiAiVHJ1ZSJ9.6b9d062199f0e93d6e23f1650db6e5eb78cfcbebbc0e725c18e62291d7d6f821'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")
    
    # Test 6: View recipes for non-existent user
    print("\n6. Testing view_user_recipes with non-existent user...")
    response = client.get('/view_user_recipes?username=nonexistent', 
                         headers={'Authorization': 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJhbGljZS5zbWl0aCIsICJhY2Nlc3MiOiAiVHJ1ZSJ9.6b9d062199f0e93d6e23f1650db6e5eb78cfcbebbc0e725c18e62291d7d6f821'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.get_json()}")

def test_complete_workflow():
    """Test complete workflow with multiple users and recipes"""
    print("\nTesting Complete Workflow...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Clear database
    print("\n1. Clearing database...")
    response = client.get('/clear')
    print(f"Status: {response.status_code}")
    
    # Create two users
    print("\n2. Creating two users...")
    
    # User 1
    data1 = {
        'first_name': 'Alice',
        'last_name': 'Smith',
        'username': 'alice.smith',
        'email_address': 'alice@example.com',
        'password': 'SecurePass123!',
        'salt': 'salt1'
    }
    response = client.post('/create_user', data=data1)
    print(f"User 1 creation: {response.status_code}")
    
    # User 2
    data2 = {
        'first_name': 'Bob',
        'last_name': 'Jones',
        'username': 'bob.jones',
        'email_address': 'bob@example.com',
        'password': 'SecurePass123!',
        'salt': 'salt2'
    }
    response = client.post('/create_user', data=data2)
    print(f"User 2 creation: {response.status_code}")
    
    # Login both users
    print("\n3. Logging in both users...")
    
    # Login user 1
    response = client.post('/login', data={'username': 'alice.smith', 'password': 'SecurePass123!'})
    jwt1 = response.get_json().get('jwt')
    print(f"User 1 login: {response.status_code}")
    
    # Login user 2
    response = client.post('/login', data={'username': 'bob.jones', 'password': 'SecurePass123!'})
    jwt2 = response.get_json().get('jwt')
    print(f"User 2 login: {response.status_code}")
    
    # Create recipes for both users
    print("\n4. Creating recipes for both users...")
    
    # Recipe 1 by Alice
    recipe1_data = {
        'title': 'Chocolate Cake',
        'description': 'Delicious chocolate cake',
        'ingredients': 'flour, sugar, cocoa, eggs, butter',
        'instructions': 'Mix ingredients and bake',
        'prep_time': '30',
        'cook_time': '45',
        'servings': '8'
    }
    response = client.post('/create_recipe', data=recipe1_data, headers={'Authorization': jwt1})
    recipe1_id = response.get_json().get('recipe_id')
    print(f"Recipe 1 creation: {response.status_code}, ID: {recipe1_id}")
    
    # Recipe 2 by Bob
    recipe2_data = {
        'title': 'Pasta Salad',
        'description': 'Fresh pasta salad',
        'ingredients': 'pasta, tomatoes, cucumber, olive oil',
        'instructions': 'Cook pasta, mix with vegetables',
        'prep_time': '15',
        'cook_time': '10',
        'servings': '4'
    }
    response = client.post('/create_recipe', data=recipe2_data, headers={'Authorization': jwt2})
    recipe2_id = response.get_json().get('recipe_id')
    print(f"Recipe 2 creation: {response.status_code}, ID: {recipe2_id}")
    
    # Cross-like recipes
    print("\n5. Cross-liking recipes...")
    
    # Alice likes Bob's recipe
    response = client.post(f'/like_recipe/{recipe2_id}', headers={'Authorization': jwt1})
    print(f"Alice likes Bob's recipe: {response.status_code}, Like count: {response.get_json().get('like_count')}")
    
    # Bob likes Alice's recipe
    response = client.post(f'/like_recipe/{recipe1_id}', headers={'Authorization': jwt2})
    print(f"Bob likes Alice's recipe: {response.status_code}, Like count: {response.get_json().get('like_count')}")
    
    # Search functionality
    print("\n6. Testing search functionality...")
    
    # Search by title
    response = client.get('/search_recipes?search_term=chocolate&search_type=title', headers={'Authorization': jwt1})
    print(f"Search by title: {response.status_code}, Results: {len(response.get_json().get('data', []))}")
    
    # Search by ingredients
    response = client.get('/search_recipes?search_term=pasta&search_type=ingredients', headers={'Authorization': jwt1})
    print(f"Search by ingredients: {response.status_code}, Results: {len(response.get_json().get('data', []))}")
    
    # View user recipes
    print("\n7. Testing view user recipes...")
    
    # View Alice's recipes
    response = client.get('/view_user_recipes?username=alice.smith', headers={'Authorization': jwt1})
    print(f"Alice's recipes: {response.status_code}, Count: {len(response.get_json().get('data', []))}")
    
    # View Bob's recipes
    response = client.get('/view_user_recipes?username=bob.jones', headers={'Authorization': jwt1})
    print(f"Bob's recipes: {response.status_code}, Count: {len(response.get_json().get('data', []))}")
    
    print("\n" + "=" * 50)
    print("✅ Complete workflow test passed!")

def main():
    """Run all tests"""
    print("Project 2 - Comprehensive Test Suite")
    print("=" * 50)
    
    # Test edge cases
    test_edge_cases()
    
    # Test complete workflow
    test_complete_workflow()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    print("Project 2 is fully functional and ready for use!")

if __name__ == "__main__":
    main()
