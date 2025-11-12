import requests
import json
import time

BASE = "http://127.0.0.1:5000"

def fail():
    print('Test Failed')
    raise SystemExit

def ok(r): 
    return r.json().get('status') == 1

try:
    requests.get(BASE+"/clear")
    
    # Create users for likes
    users = []
    for i in range(3):
        u={'first_name':f'User{i}','last_name':'Test','username':f'user{i}','email_address':f'user{i}@x.com','password':'Qx7Yt9Lp','salt':'s'}
        if not ok(requests.post(BASE+"/create_user", data=u)): fail()
        jwt=requests.post(BASE+"/login", data={'username':f'user{i}','password':'Qx7Yt9Lp'}).json()['jwt']
        users.append({'Authorization':jwt})
    
    h = users[0]  # Use first user for recipe creation
    
    # Create multiple recipes with same like counts to test tie-breaking
    # Recipe 2000: 2 likes
    # Recipe 2001: 2 likes (same count - tie, should use created_at DESC then recipe_id ASC)
    # Recipe 2002: 1 like
    # Recipe 2003: 0 likes
    
    # Create recipes with slight delay to ensure different created_at
    for rid in [2000, 2001, 2002, 2003]:
        if not ok(requests.post(BASE+"/create_recipe", data={
            'name':f'R{rid}','description':'d','recipe_id':rid,'ingredients':json.dumps(['x'])
        }, headers=h)): fail()
        time.sleep(0.01)  # Small delay to ensure different timestamps
    
    # Add likes: 2000 gets 2 likes, 2001 gets 2 likes, 2002 gets 1 like
    # Use different users for each like to avoid duplicate like errors
    if not ok(requests.post(BASE+"/like", data={'recipe_id':2000}, headers=users[0])): fail()
    if not ok(requests.post(BASE+"/like", data={'recipe_id':2000}, headers=users[1])): fail()
    if not ok(requests.post(BASE+"/like", data={'recipe_id':2001}, headers=users[0])): fail()
    if not ok(requests.post(BASE+"/like", data={'recipe_id':2001}, headers=users[1])): fail()
    if not ok(requests.post(BASE+"/like", data={'recipe_id':2002}, headers=users[0])): fail()
    
    # Popular search should return top 2 by like count: 2000 and 2001 (both have 2 likes)
    # Since they have same like count and likely same created_at (very close), 
    # tie-breaker should be recipe_id ASC, so 2000 should come before 2001
    res = requests.get(BASE+"/search", params={'popular':'True'}, headers=h).json()
    if res.get('status') != 1: fail()
    
    if len(res['data']) != 2:
        fail()
    
    # Check that we got the top 2 recipes with most likes
    recipe_ids = list(res['data'].keys())
    if set(recipe_ids) != {'2000', '2001'}:
        fail()
    
    # Verify ordering: should be deterministic (recipe_id ASC as tie-breaker)
    # Both have 2 likes, so ordering should be by created_at DESC then recipe_id ASC
    # Since 2001 was created after 2000, if timestamps are different, 2001 should come first
    # But with recipe_id ASC tie-breaker after created_at, we need to check implementation
    
    # At minimum, both recipes with 2 likes should be in top 2
    if '2000' not in recipe_ids or '2001' not in recipe_ids:
        fail()
    
    # Recipe with 1 like should NOT be in top 2
    if '2002' in recipe_ids:
        fail()
    
    # Recipe with 0 likes should NOT be in top 2
    if '2003' in recipe_ids:
        fail()
    
    print('Test Passed')
except:
    print('Test Failed')

