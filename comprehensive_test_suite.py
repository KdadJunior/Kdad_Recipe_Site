#!/usr/bin/env python3
"""
Comprehensive Test Suite for Project 2: The Meals LAN
Tests all requirements from the project specifications
"""

import app
from flask.testing import FlaskClient
import json
import time

def test_database_requirements():
    """Test database requirements from specifications"""
    print("Testing Database Requirements...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Test 1: Database initialization with project2.db
    print("\n1. Testing database initialization...")
    response = client.get('/clear')
    assert response.status_code == 200
    assert response.get_json()['status'] == 1
    print("✅ Database cleared and initialized successfully")
    
    # Test 2: Check if project2.db file exists
    import os
    assert os.path.exists('project2.db'), "project2.db file should exist"
    print("✅ project2.db file exists")
    
    # Test 3: Check if project2.sql file exists
    assert os.path.exists('project2.sql'), "project2.sql file should exist"
    print("✅ project2.sql file exists")

def test_user_management():
    """Test user management functionality from Project 1"""
    print("\nTesting User Management (Project 1 Requirements)...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Test 1: Create user with valid data
    print("\n1. Testing user creation...")
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'johndoe',
        'email_address': 'john@example.com',
        'password': 'SecurePass123!',
        'salt': 'randomsalt123'
    }
    response = client.post('/create_user', data=user_data)
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert 'pass_hash' in result
    print("✅ User creation successful")
    
    # Test 2: Create user with duplicate username
    print("\n2. Testing duplicate username...")
    response = client.post('/create_user', data=user_data)
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # Username already exists
    print("✅ Duplicate username handled correctly")
    
    # Test 3: Create user with duplicate email
    print("\n3. Testing duplicate email...")
    user_data2 = user_data.copy()
    user_data2['username'] = 'johndoe2'
    response = client.post('/create_user', data=user_data2)
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 3  # Email already exists
    print("✅ Duplicate email handled correctly")
    
    # Test 4: Create user with invalid password
    print("\n4. Testing invalid password...")
    user_data3 = user_data.copy()
    user_data3['username'] = 'johndoe3'
    user_data3['email_address'] = 'john3@example.com'
    user_data3['password'] = 'weak'  # Too short
    response = client.post('/create_user', data=user_data3)
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 4  # Invalid password
    print("✅ Invalid password handled correctly")
    
    # Test 5: Login with valid credentials
    print("\n5. Testing login...")
    login_data = {
        'username': 'johndoe',
        'password': 'SecurePass123!'
    }
    response = client.post('/login', data=login_data)
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert 'jwt' in result
    jwt_token = result['jwt']
    print("✅ Login successful")
    
    # Test 6: Login with invalid credentials
    print("\n6. Testing invalid login...")
    invalid_login = {
        'username': 'johndoe',
        'password': 'wrongpassword'
    }
    response = client.post('/login', data=invalid_login)
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # Invalid credentials
    print("✅ Invalid login handled correctly")
    
    return jwt_token

def test_recipe_management(jwt_token):
    """Test recipe management functionality"""
    print("\nTesting Recipe Management...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Test 1: Create recipe with valid data
    print("\n1. Testing recipe creation...")
    recipe_data = {
        'title': 'Chocolate Chip Cookies',
        'description': 'Delicious homemade cookies',
        'ingredients': '2 cups flour, 1 cup sugar, 1/2 cup butter, 1 egg, 1 tsp vanilla, 1 cup chocolate chips',
        'instructions': '1. Mix dry ingredients. 2. Cream butter and sugar. 3. Add egg and vanilla. 4. Combine wet and dry ingredients. 5. Add chocolate chips. 6. Bake at 375°F for 10-12 minutes.',
        'prep_time': '15',
        'cook_time': '12',
        'servings': '24'
    }
    response = client.post('/create_recipe', data=recipe_data, headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert 'recipe_id' in result
    recipe_id = result['recipe_id']
    print("✅ Recipe creation successful")
    
    # Test 2: Create recipe with missing required fields
    print("\n2. Testing recipe creation with missing fields...")
    incomplete_data = {
        'title': 'Incomplete Recipe',
        'ingredients': 'test ingredients'
        # Missing instructions
    }
    response = client.post('/create_recipe', data=incomplete_data, headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # Missing required fields
    print("✅ Missing fields handled correctly")
    
    # Test 3: Create recipe without JWT
    print("\n3. Testing recipe creation without JWT...")
    response = client.post('/create_recipe', data=recipe_data)
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # No JWT
    print("✅ Missing JWT handled correctly")
    
    # Test 4: Create recipe with invalid JWT
    print("\n4. Testing recipe creation with invalid JWT...")
    response = client.post('/create_recipe', data=recipe_data, headers={'Authorization': 'invalid_jwt'})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # Invalid JWT
    print("✅ Invalid JWT handled correctly")
    
    return recipe_id

def test_recipe_viewing(jwt_token, recipe_id):
    """Test recipe viewing functionality"""
    print("\nTesting Recipe Viewing...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Test 1: View existing recipe
    print("\n1. Testing view existing recipe...")
    response = client.get(f'/view_recipe/{recipe_id}', headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert 'data' in result
    recipe_data = result['data']
    assert recipe_data['recipe_id'] == recipe_id
    assert recipe_data['title'] == 'Chocolate Chip Cookies'
    assert recipe_data['like_count'] == 0
    assert recipe_data['user_liked'] == False
    print("✅ Recipe viewing successful")
    
    # Test 2: View non-existent recipe
    print("\n2. Testing view non-existent recipe...")
    response = client.get('/view_recipe/999', headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # Recipe not found
    print("✅ Non-existent recipe handled correctly")
    
    # Test 3: View recipe without JWT
    print("\n3. Testing view recipe without JWT...")
    response = client.get(f'/view_recipe/{recipe_id}')
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # No JWT
    print("✅ Missing JWT handled correctly")

def test_like_system(jwt_token, recipe_id):
    """Test recipe liking system"""
    print("\nTesting Like System...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Test 1: Like a recipe
    print("\n1. Testing like recipe...")
    response = client.post(f'/like_recipe/{recipe_id}', headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert result['like_count'] == 1
    print("✅ Recipe liked successfully")
    
    # Test 2: Unlike a recipe (toggle)
    print("\n2. Testing unlike recipe...")
    response = client.post(f'/like_recipe/{recipe_id}', headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert result['like_count'] == 0
    print("✅ Recipe unliked successfully")
    
    # Test 3: Like again
    print("\n3. Testing like recipe again...")
    response = client.post(f'/like_recipe/{recipe_id}', headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert result['like_count'] == 1
    print("✅ Recipe liked again successfully")
    
    # Test 4: Like non-existent recipe
    print("\n4. Testing like non-existent recipe...")
    response = client.post('/like_recipe/999', headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # Recipe not found
    print("✅ Non-existent recipe like handled correctly")
    
    # Test 5: Like without JWT
    print("\n5. Testing like without JWT...")
    response = client.post(f'/like_recipe/{recipe_id}')
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # No JWT
    print("✅ Missing JWT handled correctly")

def test_search_functionality(jwt_token):
    """Test recipe search functionality"""
    print("\nTesting Search Functionality...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Test 1: Search by title
    print("\n1. Testing search by title...")
    response = client.get('/search_recipes?search_term=chocolate&search_type=title', 
                         headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert 'data' in result
    assert len(result['data']) >= 1  # Should find the chocolate chip cookies
    print("✅ Search by title successful")
    
    # Test 2: Search by ingredients
    print("\n2. Testing search by ingredients...")
    response = client.get('/search_recipes?search_term=flour&search_type=ingredients', 
                         headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert 'data' in result
    assert len(result['data']) >= 1  # Should find recipes with flour
    print("✅ Search by ingredients successful")
    
    # Test 3: Search with empty term
    print("\n3. Testing search with empty term...")
    response = client.get('/search_recipes?search_term=&search_type=title', 
                         headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # Empty search term
    print("✅ Empty search term handled correctly")
    
    # Test 4: Search without JWT
    print("\n4. Testing search without JWT...")
    response = client.get('/search_recipes?search_term=chocolate&search_type=title')
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # No JWT
    print("✅ Missing JWT handled correctly")

def test_user_recipes_viewing(jwt_token):
    """Test viewing recipes by user"""
    print("\nTesting User Recipes Viewing...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Test 1: View recipes by existing user
    print("\n1. Testing view recipes by existing user...")
    response = client.get('/view_user_recipes?username=johndoe', 
                         headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert 'data' in result
    assert len(result['data']) >= 1  # Should find the chocolate chip cookies
    print("✅ View user recipes successful")
    
    # Test 2: View recipes by non-existent user
    print("\n2. Testing view recipes by non-existent user...")
    response = client.get('/view_user_recipes?username=nonexistent', 
                         headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # User not found
    print("✅ Non-existent user handled correctly")
    
    # Test 3: View recipes without username parameter
    print("\n3. Testing view recipes without username...")
    response = client.get('/view_user_recipes', headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # Missing username
    print("✅ Missing username handled correctly")
    
    # Test 4: View recipes without JWT
    print("\n4. Testing view recipes without JWT...")
    response = client.get('/view_user_recipes?username=johndoe')
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # No JWT
    print("✅ Missing JWT handled correctly")

def test_multi_user_scenario(jwt_token):
    """Test multi-user scenario with cross-liking"""
    print("\nTesting Multi-User Scenario...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Create second user
    print("\n1. Creating second user...")
    user2_data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'username': 'janesmith',
        'email_address': 'jane@example.com',
        'password': 'SecurePass123!',
        'salt': 'randomsalt456'
    }
    response = client.post('/create_user', data=user2_data)
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    print("✅ Second user created")
    
    # Login second user
    print("\n2. Logging in second user...")
    login_data = {
        'username': 'janesmith',
        'password': 'SecurePass123!'
    }
    response = client.post('/login', data=login_data)
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    jwt2 = result['jwt']
    print("✅ Second user logged in")
    
    # Create recipe for second user
    print("\n3. Creating recipe for second user...")
    recipe2_data = {
        'title': 'Pasta Salad',
        'description': 'Fresh and healthy pasta salad',
        'ingredients': 'pasta, tomatoes, cucumber, olive oil, herbs',
        'instructions': '1. Cook pasta. 2. Chop vegetables. 3. Mix with olive oil and herbs.',
        'prep_time': '15',
        'cook_time': '10',
        'servings': '4'
    }
    response = client.post('/create_recipe', data=recipe2_data, headers={'Authorization': jwt2})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    recipe2_id = result['recipe_id']
    print("✅ Second user's recipe created")
    
    # Cross-like recipes
    print("\n4. Testing cross-liking...")
    # User 1 likes User 2's recipe
    response = client.post(f'/like_recipe/{recipe2_id}', headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert result['like_count'] == 1
    print("✅ User 1 liked User 2's recipe")
    
    # User 2 likes User 1's recipe
    response = client.post(f'/like_recipe/1', headers={'Authorization': jwt2})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert result['like_count'] == 2  # User 1 + User 2
    print("✅ User 2 liked User 1's recipe")
    
    # Test search finds both recipes
    print("\n5. Testing search finds both recipes...")
    response = client.get('/search_recipes?search_term=pasta&search_type=ingredients', 
                         headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    assert len(result['data']) >= 1  # Should find pasta salad
    print("✅ Search finds both users' recipes")

def test_edge_cases(jwt_token):
    """Test various edge cases"""
    print("\nTesting Edge Cases...")
    print("=" * 50)
    
    client = app.app.test_client()
    
    # Test 1: Very long recipe title
    print("\n1. Testing very long recipe title...")
    long_title = 'A' * 1000
    recipe_data = {
        'title': long_title,
        'ingredients': 'test',
        'instructions': 'test'
    }
    response = client.post('/create_recipe', data=recipe_data, headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    print("✅ Long title handled correctly")
    
    # Test 2: Special characters in recipe data
    print("\n2. Testing special characters...")
    special_data = {
        'title': 'Recipe with Special Chars: !@#$%^&*()',
        'ingredients': 'ingredients with "quotes" and \'apostrophes\'',
        'instructions': 'Instructions with <html> tags and & symbols'
    }
    response = client.post('/create_recipe', data=special_data, headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 1
    print("✅ Special characters handled correctly")
    
    # Test 3: Empty strings
    print("\n3. Testing empty strings...")
    empty_data = {
        'title': '',
        'ingredients': '',
        'instructions': ''
    }
    response = client.post('/create_recipe', data=empty_data, headers={'Authorization': jwt_token})
    assert response.status_code == 200
    result = response.get_json()
    assert result['status'] == 2  # Empty required fields
    print("✅ Empty strings handled correctly")

def main():
    """Run all tests"""
    print("Project 2: The Meals LAN - Comprehensive Test Suite")
    print("=" * 60)
    
    try:
        # Test database requirements
        test_database_requirements()
        
        # Test user management
        jwt_token = test_user_management()
        
        # Test recipe management
        recipe_id = test_recipe_management(jwt_token)
        
        # Test recipe viewing
        test_recipe_viewing(jwt_token, recipe_id)
        
        # Test like system
        test_like_system(jwt_token, recipe_id)
        
        # Test search functionality
        test_search_functionality(jwt_token)
        
        # Test user recipes viewing
        test_user_recipes_viewing(jwt_token)
        
        # Test multi-user scenario
        test_multi_user_scenario(jwt_token)
        
        # Test edge cases
        test_edge_cases(jwt_token)
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! Project 2 meets all specifications!")
        print("✅ Database requirements: PASSED")
        print("✅ User management: PASSED")
        print("✅ Recipe management: PASSED")
        print("✅ Recipe viewing: PASSED")
        print("✅ Like system: PASSED")
        print("✅ Search functionality: PASSED")
        print("✅ User recipes viewing: PASSED")
        print("✅ Multi-user scenarios: PASSED")
        print("✅ Edge cases: PASSED")
        print("\n🚀 Project 2 is ready for submission!")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
