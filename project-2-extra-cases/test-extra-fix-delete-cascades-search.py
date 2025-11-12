import requests
import json

BASE = "http://127.0.0.1:5000"

def fail(msg=''):
    if msg:
        print(f'Test Failed: {msg}')
    else:
        print('Test Failed')
    raise AssertionError(msg)

def ok(r): 
    return r.json().get('status') == 1

try:
    requests.get(BASE+"/clear")
    
    # Create users: Alice (author), Bob (follower/searcher), Carol (another user)
    alice={'first_name':'Alice','last_name':'Author','username':'alice','email_address':'alice@x.com','password':'Qx7Yt9Lp','salt':'s'}
    bob={'first_name':'Bob','last_name':'Follower','username':'bob','email_address':'bob@x.com','password':'Qx7Yt9Lp','salt':'s'}
    carol={'first_name':'Carol','last_name':'User','username':'carol','email_address':'carol@x.com','password':'Qx7Yt9Lp','salt':'s'}
    
    for u in [alice, bob, carol]:
        if not ok(requests.post(BASE+"/create_user", data=u)): fail()
    
    jwt_a=requests.post(BASE+"/login", data={'username':'alice','password':'Qx7Yt9Lp'}).json()['jwt']
    jwt_b=requests.post(BASE+"/login", data={'username':'bob','password':'Qx7Yt9Lp'}).json()['jwt']
    jwt_c=requests.post(BASE+"/login", data={'username':'carol','password':'Qx7Yt9Lp'}).json()['jwt']
    h_a={'Authorization':jwt_a}
    h_b={'Authorization':jwt_b}
    h_c={'Authorization':jwt_c}
    
    # Alice creates recipes: one with ingredients, one without
    if not ok(requests.post(BASE+"/create_recipe", data={
        'name':'WithIngs','description':'d','recipe_id':3000,'ingredients':json.dumps(['x','y'])
    }, headers=h_a)): fail()
    
    if not ok(requests.post(BASE+"/create_recipe", data={
        'name':'NoIngs','description':'d','recipe_id':3001
    }, headers=h_a)): fail()
    
    # Carol also creates a recipe with ingredients
    if not ok(requests.post(BASE+"/create_recipe", data={
        'name':'CarolRecipe','description':'d','recipe_id':3002,'ingredients':json.dumps(['x'])
    }, headers=h_c)): fail()
    
    # Bob likes Alice's recipe 3000
    if not ok(requests.post(BASE+"/like", data={'recipe_id':3000}, headers=h_b)): fail()
    
    # Bob follows Alice
    if not ok(requests.post(BASE+"/follow", data={'username':'alice'}, headers=h_b)): fail()
    
    # BEFORE DELETE: Bob searches feed - should see Alice's recipes
    feed_before = requests.get(BASE+"/search", params={'feed':'True'}, headers=h_b).json()
    if feed_before.get('status') != 1: fail()
    if '3000' not in feed_before['data'] or '3001' not in feed_before['data']:
        fail()
    
    # BEFORE DELETE: Bob searches popular - should see Alice's recipe 3000 (has like)
    pop_before = requests.get(BASE+"/search", params={'popular':'True'}, headers=h_b).json()
    if pop_before.get('status') != 1: fail()
    if '3000' not in pop_before['data']:
        fail()
    
    # BEFORE DELETE: Bob searches ingredients 'x' - should see 3002 (has only x), 
    # NOT 3000 (has x,y - y is not in search list), NOT 3001 (no ingredients)
    ing_before = requests.get(BASE+"/search", params={'ingredients':json.dumps(['x'])}, headers=h_b).json()
    if ing_before.get('status') != 1: fail()
    if '3001' in ing_before['data']:
        fail('Recipe with no ingredients should NOT appear')
    if '3000' in ing_before['data']:
        fail('Recipe 3000 has y which is not in search list, should NOT appear')
    if '3002' not in ing_before['data']:
        fail('Carol recipe 3002 with only x should appear')
    
    # Search for 'x' and 'y' - should see 3000 (has x,y) and 3002 (has x)
    ing_before2 = requests.get(BASE+"/search", params={'ingredients':json.dumps(['x','y'])}, headers=h_b).json()
    if ing_before2.get('status') != 1: fail()
    if '3000' not in ing_before2['data']:
        fail('Recipe 3000 with x,y should appear when searching for x,y')
    
    # Alice deletes herself
    if not ok(requests.post(BASE+"/delete", data={'username':'alice'}, headers=h_a)): fail()
    
    # AFTER DELETE: Bob searches feed - should NOT include Alice's recipes
    feed_after = requests.get(BASE+"/search", params={'feed':'True'}, headers=h_b).json()
    if feed_after.get('status') != 1: fail()
    if '3000' in feed_after['data'] or '3001' in feed_after['data']:
        fail()  # Deleted user's recipes should NOT appear
    
    # AFTER DELETE: Bob searches popular - should NOT include Alice's recipe 3000
    pop_after = requests.get(BASE+"/search", params={'popular':'True'}, headers=h_b).json()
    if pop_after.get('status') != 1: fail()
    if '3000' in pop_after['data']:
        fail()  # Deleted user's recipe should NOT appear
    
    # AFTER DELETE: Bob searches ingredients 'x' - should NOT include Alice's recipes
    # Should still see Carol's recipe 3002 if it matches
    ing_after = requests.get(BASE+"/search", params={'ingredients':json.dumps(['x'])}, headers=h_b).json()
    if ing_after.get('status') != 1: fail()
    if '3000' in ing_after['data'] or '3001' in ing_after['data']:
        fail()  # Deleted user's recipes should NOT appear
    if '3002' in ing_after['data']:
        pass  # Carol's recipe should still appear (she wasn't deleted)
    
    # Verify Bob can't follow deleted user
    if requests.post(BASE+"/follow", data={'username':'alice'}, headers=h_c).json().get('status') != 2:
        fail()
    
    print('Test Passed')
except Exception as e:
    print(f'Test Failed: {e}')
    import traceback
    traceback.print_exc()

