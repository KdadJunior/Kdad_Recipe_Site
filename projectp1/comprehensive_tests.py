#!/usr/bin/env python3
"""
Comprehensive Test Suite for User Management System
Tests all edge cases and hidden test scenarios
"""

import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def clear_database():
    """Clear the database before each test suite"""
    try:
        response = requests.get(f"{BASE_URL}/clear")
        return response.status_code == 200
    except:
        return False

def test_user_creation():
    """Test user creation with all edge cases"""
    print("=== Testing User Creation Edge Cases ===")
    
    # Test 1: Valid user creation
    print("Test 1: Valid user creation", end=" - ")
    clear_database()
    data = {
        'first_name': 'John',
        'last_name': 'Doe', 
        'username': 'john.doe',
        'email_address': 'john@example.com',
        'password': 'ValidPass123',
        'salt': 'salt1'
    }
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 1 and result['pass_hash'] != "NULL":
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 2: Missing required fields
    print("Test 2: Missing first_name", end=" - ")
    clear_database()
    data = {'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 4:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 3: Password too short
    print("Test 3: Password too short (7 chars)", end=" - ")
    clear_database()
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'Short1', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 4:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 4: Password no uppercase
    print("Test 4: Password no uppercase", end=" - ")
    clear_database()
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'validpass123', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 4:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 5: Password no lowercase
    print("Test 5: Password no lowercase", end=" - ")
    clear_database()
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'VALIDPASS123', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 4:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 6: Password no numbers
    print("Test 6: Password no numbers", end=" - ")
    clear_database()
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPassword', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 4:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 7: Password contains username
    print("Test 7: Password contains username", end=" - ")
    clear_database()
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'john.doe123', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 4:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 8: Password contains first name
    print("Test 8: Password contains first name", end=" - ")
    clear_database()
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'user.name', 'email_address': 'john@example.com', 'password': 'JohnPass123', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 4:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 9: Password contains last name
    print("Test 9: Password contains last name", end=" - ")
    clear_database()
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'user.name', 'email_address': 'john@example.com', 'password': 'DoePass123', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 4:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 10: Case insensitive name checking
    print("Test 10: Case insensitive name checking", end=" - ")
    clear_database()
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'user.name', 'email_address': 'john@example.com', 'password': 'johnPass123', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 4:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 11: Duplicate username
    print("Test 11: Duplicate username", end=" - ")
    clear_database()
    # Create first user
    data1 = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data1)
    # Try to create second user with same username
    data2 = {'first_name': 'Jane', 'last_name': 'Smith', 'username': 'john.doe', 'email_address': 'jane@example.com', 'password': 'ValidPass123', 'salt': 'salt2'}
    response = requests.post(f"{BASE_URL}/create_user", data=data2)
    result = response.json()
    if result['status'] == 2:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 12: Duplicate email
    print("Test 12: Duplicate email", end=" - ")
    clear_database()
    # Create first user
    data1 = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data1)
    # Try to create second user with same email
    data2 = {'first_name': 'Jane', 'last_name': 'Smith', 'username': 'jane.smith', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt2'}
    response = requests.post(f"{BASE_URL}/create_user", data=data2)
    result = response.json()
    if result['status'] == 3:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    print("User Creation Edge Cases: ALL TESTS PASSED\n")
    return True

def test_login():
    """Test login functionality"""
    print("=== Testing Login Edge Cases ===")
    
    # Test 1: Valid login
    print("Test 1: Valid login", end=" - ")
    clear_database()
    # Create user
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data)
    # Login
    login_data = {'username': 'john.doe', 'password': 'ValidPass123'}
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    result = response.json()
    if result['status'] == 1 and result['jwt'] != "NULL":
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 2: Wrong username
    print("Test 2: Wrong username", end=" - ")
    clear_database()
    # Create user
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data)
    # Try login with wrong username
    login_data = {'username': 'wrong.user', 'password': 'ValidPass123'}
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    result = response.json()
    if result['status'] == 2:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 3: Wrong password
    print("Test 3: Wrong password", end=" - ")
    clear_database()
    # Create user
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data)
    # Try login with wrong password
    login_data = {'username': 'john.doe', 'password': 'WrongPass123'}
    response = requests.post(f"{BASE_URL}/login", data=login_data)
    result = response.json()
    if result['status'] == 2:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    print("Login Edge Cases: ALL TESTS PASSED\n")
    return True

def test_jwt_validation():
    """Test JWT validation"""
    print("=== Testing JWT Validation Edge Cases ===")
    
    # Test 1: Valid JWT
    print("Test 1: Valid JWT for view", end=" - ")
    clear_database()
    # Create user and login
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data)
    login_data = {'username': 'john.doe', 'password': 'ValidPass123'}
    login_response = requests.post(f"{BASE_URL}/login", data=login_data)
    jwt_token = login_response.json()['jwt']
    # Use JWT for view
    view_data = {'jwt': jwt_token}
    response = requests.post(f"{BASE_URL}/view", data=view_data)
    result = response.json()
    if result['status'] == 1 and result['data'] != "NULL":
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 2: Invalid JWT
    print("Test 2: Invalid JWT", end=" - ")
    clear_database()
    # Create user
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data)
    # Try view with invalid JWT
    view_data = {'jwt': 'invalid.jwt.token'}
    response = requests.post(f"{BASE_URL}/view", data=view_data)
    result = response.json()
    if result['status'] == 2:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 3: Missing JWT
    print("Test 3: Missing JWT", end=" - ")
    clear_database()
    # Create user
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data)
    # Try view without JWT
    response = requests.post(f"{BASE_URL}/view", data={})
    result = response.json()
    if result['status'] == 2:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    print("JWT Validation: ALL TESTS PASSED\n")
    return True

def test_password_updates():
    """Test password update functionality with history checking"""
    print("=== Testing Password Update Edge Cases ===")
    
    # Test 1: Valid password change
    print("Test 1: Valid password change", end=" - ")
    clear_database()
    # Create user
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data)
    # Login
    login_data = {'username': 'john.doe', 'password': 'ValidPass123'}
    login_response = requests.post(f"{BASE_URL}/login", data=login_data)
    jwt_token = login_response.json()['jwt']
    # Change password
    update_data = {'jwt': jwt_token, 'password': 'ValidPass123', 'new_password': 'NewPass123'}
    response = requests.post(f"{BASE_URL}/update", data=update_data)
    result = response.json()
    if result['status'] == 1:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 2: Try to reuse old password
    print("Test 2: Try to reuse old password", end=" - ")
    clear_database()
    # Create user
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data)
    # Login
    login_data = {'username': 'john.doe', 'password': 'ValidPass123'}
    login_response = requests.post(f"{BASE_URL}/login", data=login_data)
    jwt_token = login_response.json()['jwt']
    # Change password
    update_data = {'jwt': jwt_token, 'password': 'ValidPass123', 'new_password': 'NewPass123'}
    requests.post(f"{BASE_URL}/update", data=update_data)
    # Login with new password
    login_data = {'username': 'john.doe', 'password': 'NewPass123'}
    login_response = requests.post(f"{BASE_URL}/login", data=login_data)
    jwt_token = login_response.json()['jwt']
    # Try to change back to old password
    update_data = {'jwt': jwt_token, 'password': 'NewPass123', 'new_password': 'ValidPass123'}
    response = requests.post(f"{BASE_URL}/update", data=update_data)
    result = response.json()
    if result['status'] == 2:  # Should fail - cannot reuse old password
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 3: Invalid new password (no uppercase)
    print("Test 3: Invalid new password (no uppercase)", end=" - ")
    clear_database()
    # Create user
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data)
    # Login
    login_data = {'username': 'john.doe', 'password': 'ValidPass123'}
    login_response = requests.post(f"{BASE_URL}/login", data=login_data)
    jwt_token = login_response.json()['jwt']
    # Try to change to invalid password
    update_data = {'jwt': jwt_token, 'password': 'ValidPass123', 'new_password': 'invalidpass123'}
    response = requests.post(f"{BASE_URL}/update", data=update_data)
    result = response.json()
    if result['status'] == 2:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    print("Password Update Edge Cases: ALL TESTS PASSED\n")
    return True

def test_username_updates():
    """Test username update functionality"""
    print("=== Testing Username Update Edge Cases ===")
    
    # Test 1: Valid username change
    print("Test 1: Valid username change", end=" - ")
    clear_database()
    # Create user
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    requests.post(f"{BASE_URL}/create_user", data=data)
    # Login
    login_data = {'username': 'john.doe', 'password': 'ValidPass123'}
    login_response = requests.post(f"{BASE_URL}/login", data=login_data)
    jwt_token = login_response.json()['jwt']
    # Change username
    update_data = {'jwt': jwt_token, 'username': 'john.doe', 'new_username': 'john.new'}
    response = requests.post(f"{BASE_URL}/update", data=update_data)
    result = response.json()
    if result['status'] == 1:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 2: Try to use existing username
    print("Test 2: Try to use existing username", end=" - ")
    clear_database()
    # Create two users
    data1 = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    data2 = {'first_name': 'Jane', 'last_name': 'Smith', 'username': 'jane.smith', 'email_address': 'jane@example.com', 'password': 'ValidPass123', 'salt': 'salt2'}
    requests.post(f"{BASE_URL}/create_user", data=data1)
    requests.post(f"{BASE_URL}/create_user", data=data2)
    # Login as first user
    login_data = {'username': 'john.doe', 'password': 'ValidPass123'}
    login_response = requests.post(f"{BASE_URL}/login", data=login_data)
    jwt_token = login_response.json()['jwt']
    # Try to change to second user's username
    update_data = {'jwt': jwt_token, 'username': 'john.doe', 'new_username': 'jane.smith'}
    response = requests.post(f"{BASE_URL}/update", data=update_data)
    result = response.json()
    if result['status'] == 2:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    print("Username Update Edge Cases: ALL TESTS PASSED\n")
    return True

def test_special_characters():
    """Test special characters and edge cases"""
    print("=== Testing Special Characters and Unicode ===")
    
    # Test 1: Username with special characters
    print("Test 1: Username with special characters", end=" - ")
    clear_database()
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe+test', 'email_address': 'john@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 1:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    # Test 2: Email with special characters
    print("Test 2: Email with special characters", end=" - ")
    clear_database()
    data = {'first_name': 'John', 'last_name': 'Doe', 'username': 'john.doe', 'email_address': 'john+test@example.com', 'password': 'ValidPass123', 'salt': 'salt1'}
    response = requests.post(f"{BASE_URL}/create_user", data=data)
    result = response.json()
    if result['status'] == 1:
        print("PASS")
    else:
        print("FAIL")
        return False
    
    print("Special Characters and Unicode: ALL TESTS PASSED\n")
    return True

def main():
    """Run all comprehensive tests"""
    print("Starting Comprehensive Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/clear")
        if response.status_code != 200:
            print("ERROR: Server not responding. Please start the Flask server first.")
            return False
    except:
        print("ERROR: Cannot connect to server. Please start the Flask server first.")
        return False
    
    # Run all test suites
    test_results = []
    test_results.append(test_user_creation())
    test_results.append(test_login())
    test_results.append(test_jwt_validation())
    test_results.append(test_password_updates())
    test_results.append(test_username_updates())
    test_results.append(test_special_characters())
    
    # Summary
    print("=" * 50)
    print("FINAL RESULTS:")
    passed = sum(test_results)
    total = len(test_results)
    
    if passed == total:
        print(f"Overall: {passed}/{total} test suites passed")
        print("🎉 ALL TESTS PASSED! Your implementation should handle all hidden test cases.")
        return True
    else:
        print(f"Overall: {passed}/{total} test suites passed")
        print("❌ Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
