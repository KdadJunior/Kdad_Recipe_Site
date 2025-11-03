#!/usr/bin/env python3
"""Manual test to debug issues"""

import requests
import json

try:
    # Test clear
    URLclear = "http://127.0.0.1:5000/clear"
    r_clear = requests.get(url=URLclear)
    print(f"Clear: {r_clear.status_code}, Text: {r_clear.text}")
    try:
        print(f"JSON: {r_clear.json()}")
    except:
        pass
    
    # Test create user
    URL = "http://127.0.0.1:5000/create_user"
    PARAMS = {'first_name': 'James', 'last_name': 'Mariani', 'username': 'jmm', 'email_address': 'james@mariani.com', 'password': 'Examplepassword1', 'salt': 'FE8x1gO+7z0B'}
    r = requests.post(url=URL, data=PARAMS)
    data = r.json()
    print(f"Create user: {r.status_code}, {data}")
    
    solution = {"status": 1, "pass_hash": "9060e88fe7f9a95839a19926d517a442da58f47c48edc2f37e1c3aea5f8956fc"}
    print(f"Expected: {solution}")
    
    for key in solution:
        if solution[key] != data.get(key):
            print(f"MISMATCH on {key}: expected {solution[key]}, got {data.get(key)}")
    
    # Test login
    URLLogin = "http://127.0.0.1:5000/login"
    LOGINPARAMS = {'username': 'jmm', 'password': 'Examplepassword1'}
    r_login = requests.post(url=URLLogin, data=LOGINPARAMS)
    login_data = r_login.json()
    print(f"\nLogin: {r_login.status_code}, {login_data}")
    
    solution = {"status": 1, "jwt": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VybmFtZSI6ICJqbW0ifQ==.02838fbb9275f0c5f5f9b734d984d683be04491cd3a8cf506016c4903bbe8b4f"}
    print(f"Expected: {solution}")
    
    for key in solution:
        if solution[key] != login_data.get(key):
            print(f"MISMATCH on {key}: expected {solution[key]}, got {login_data.get(key)}")
            
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

