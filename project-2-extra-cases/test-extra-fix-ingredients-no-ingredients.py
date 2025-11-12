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
    
    # Create user
    u={'first_name':'Fix','last_name':'Test','username':'fixuser','email_address':'fix@x.com','password':'Qx7Yt9Lp','salt':'s'}
    if not ok(requests.post(BASE+"/create_user", data=u)): fail()
    jwt=requests.post(BASE+"/login", data={'username':'fixuser','password':'Qx7Yt9Lp'}).json()['jwt']
    h={'Authorization':jwt}
    
    # Create recipes:
    # - Recipe with ingredient 'x'
    # - Recipe with ingredients 'x' and 'y'
    # - Recipe with NO ingredients (should be excluded from ingredient searches)
    # - Recipe with ingredient 'z' (should not match 'x' search)
    
    if not ok(requests.post(BASE+"/create_recipe", data={
        'name':'HasX','description':'d','recipe_id':1000,'ingredients':json.dumps(['x'])
    }, headers=h)): fail()
    
    if not ok(requests.post(BASE+"/create_recipe", data={
        'name':'HasXY','description':'d','recipe_id':1001,'ingredients':json.dumps(['x','y'])
    }, headers=h)): fail()
    
    if not ok(requests.post(BASE+"/create_recipe", data={
        'name':'NoIngredients','description':'d','recipe_id':1002
    }, headers=h)): fail()
    
    if not ok(requests.post(BASE+"/create_recipe", data={
        'name':'HasZ','description':'d','recipe_id':1003,'ingredients':json.dumps(['z'])
    }, headers=h)): fail()
    
    # Search for 'x' - should return ONLY 1000 (has only 'x'), NOT 1001 (has 'x' and 'y'), 
    # NOT 1002 (no ingredients), NOT 1003 (has z)
    res = requests.get(BASE+"/search", params={'ingredients':json.dumps(['x'])}, headers=h).json()
    if res.get('status') != 1: fail()
    
    recipe_ids = set(res['data'].keys())
    if '1002' in recipe_ids:
        fail('Recipe with no ingredients should NOT appear')
    if '1003' in recipe_ids:
        fail('Recipe with different ingredient should NOT appear')
    if '1001' in recipe_ids:
        fail('Recipe 1001 has y which is not in search list, should NOT appear')
    if '1000' not in recipe_ids:
        fail('Recipe 1000 with only x should appear')
    
    # Search for 'x' and 'y' - should return 1000 (has x), 1001 (has x,y)
    # Still NOT 1002 (no ingredients), NOT 1003 (has z)
    res2 = requests.get(BASE+"/search", params={'ingredients':json.dumps(['x','y'])}, headers=h).json()
    if res2.get('status') != 1: fail()
    recipe_ids2 = set(res2['data'].keys())
    if '1002' in recipe_ids2:
        fail('Recipe with no ingredients should still NOT appear')
    if '1003' in recipe_ids2:
        fail('Recipe with z should NOT appear')
    if '1000' not in recipe_ids2 or '1001' not in recipe_ids2:
        fail('Both recipes with ingredients in list should appear')
    
    # Search for 'z' - should return only 1003, NOT 1002 (no ingredients)
    res3 = requests.get(BASE+"/search", params={'ingredients':json.dumps(['z'])}, headers=h).json()
    if res3.get('status') != 1: fail()
    recipe_ids3 = set(res3['data'].keys())
    if '1002' in recipe_ids3:
        fail()  # Recipe with no ingredients should NOT appear even when searching for different ingredient
    if '1003' not in recipe_ids3:
        fail()
    
    print('Test Passed')
except Exception as e:
    print(f'Test Failed: {e}')
    import traceback
    traceback.print_exc()

