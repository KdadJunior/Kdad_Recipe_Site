#!/usr/bin/env python3
"""
Comprehensive verification of implementation against test cases
"""

import json
import base64
import hashlib
import hmac

# Read key
with open('key.txt', 'r') as f:
    SECRET_KEY = f.read().strip()

def generate_jwt(username):
    """Generate JWT token - payload only contains username"""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"username": username}
    
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    
    message = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    return f"{header_encoded}.{payload_encoded}.{signature}"

def hash_password(password, salt):
    """Hash password using SHA-256 with salt"""
    combined = password + salt
    return hashlib.sha256(combined.encode()).hexdigest()

print("=" * 60)
print("Implementation Verification")
print("=" * 60)
print()

# Test 1: JWT Generation
print("1. Testing JWT Generation...")
expected_jwt = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJqbW0ifQ==.02838fbb9275f0c5f5f9b734d984d683be04491cd3a8cf506016c4903bbe8b4f"
generated_jwt = generate_jwt("jmm")
if expected_jwt == generated_jwt:
    print("   ✅ JWT generation matches expected format")
else:
    print("   ❌ JWT generation mismatch")
    print(f"   Expected: {expected_jwt}")
    print(f"   Generated: {generated_jwt}")

# Test 2: Password Hashing
print("\n2. Testing Password Hashing...")
password = 'Examplepassword1'
salt = 'FE8x1gO+7z0B'
expected_hash = "9060e88fe7f9a95839a19926d517a442da58f47c48edc2f37e1c3aea5f8956fc"
generated_hash = hash_password(password, salt)
if expected_hash == generated_hash:
    print("   ✅ Password hashing matches expected value")
else:
    print("   ❌ Password hash mismatch")
    print(f"   Expected: {expected_hash}")
    print(f"   Generated: {generated_hash}")

# Test 3: JSON Key Handling
print("\n3. Testing JSON Key Handling...")
# Simulate search result with integer recipe IDs
result_data = {
    '601': {'name': 'Test', 'likes': '1'},
    '127': {'name': 'Test2', 'likes': '0'}
}
# Simulate test solution
solution = json.dumps({'status': 1, 'data': {601: {'name': 'Test', 'likes': '1'}, 127: {'name': 'Test2', 'likes': '0'}}})
solution_dict = json.loads(solution)
# Check if keys match
solution_keys = set(solution_dict['data'].keys())
result_keys = set(result_data.keys())
if solution_keys == result_keys:
    print("   ✅ JSON key handling is correct (integer keys become strings)")
else:
    print("   ❌ JSON key mismatch")
    print(f"   Solution keys: {solution_keys}")
    print(f"   Result keys: {result_keys}")

print("\n" + "=" * 60)
print("Verification Complete")
print("=" * 60)

