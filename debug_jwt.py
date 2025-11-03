#!/usr/bin/env python3
"""Debug JWT generation"""

import hashlib
import hmac
import base64
import json

# Read the secret key
with open('key.txt', 'r') as f:
    SECRET_KEY = f.read().strip()

def generate_jwt(username):
    """Generate JWT token - payload only contains username"""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"username": username}
    
    # Encode header and payload
    header_encoded = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
    payload_encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    
    # Create signature
    message = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    return f"{header_encoded}.{payload_encoded}.{signature}"

# Expected JWT from test
expected = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJqbW0ifQ==.02838fbb9275f0c5f5f9b734d984d683be04491cd3a8cf506016c4903bbe8b4f"

# Generated JWT
generated = generate_jwt("jmm")

print(f"Expected: {expected}")
print(f"Generated: {generated}")
print(f"Match: {expected == generated}")

# Decode and compare parts
expected_parts = expected.split('.')
generated_parts = generated.split('.')

print("\nHeader:")
print(f"  Expected: {expected_parts[0]}")
print(f"  Generated: {generated_parts[0]}")
print(f"  Match: {expected_parts[0] == generated_parts[0]}")

print("\nPayload:")
print(f"  Expected: {expected_parts[1]}")
print(f"  Generated: {generated_parts[1]}")
print(f"  Match: {expected_parts[1] == generated_parts[1]}")

# Decode payloads
print("\nDecoded Payloads:")
expected_payload = base64.urlsafe_b64decode(expected_parts[1] + '==').decode()
generated_payload = base64.urlsafe_b64decode(generated_parts[1] + '==').decode()
print(f"  Expected: {expected_payload}")
print(f"  Generated: {generated_payload}")
print(f"  Match: {expected_payload == generated_payload}")

# Verify signature
message = f"{expected_parts[0]}.{expected_parts[1]}"
expected_sig = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
print(f"\nSignature:")
print(f"  Expected: {expected_parts[2]}")
print(f"  Computed: {expected_sig}")
print(f"  Match: {expected_parts[2] == expected_sig}")

