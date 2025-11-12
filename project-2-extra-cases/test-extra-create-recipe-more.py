import requests
import json

BASE = "http://127.0.0.1:5000"

def fail():
    print('Test Failed'); raise SystemExit

def ok(resp):
    return resp.json().get('status') == 1

try:
    requests.get(BASE+"/clear")
    u={'first_name':'Ivy','last_name':'Rune','username':'ivy','email_address':'ivy@x.com','password':'Qx7Yt9Lp','salt':'s'}
    if not ok(requests.post(BASE+"/create_user", data=u)): fail()
    jwt=requests.post(BASE+"/login", data={'username':'ivy','password':'Qx7Yt9Lp'}).json()['jwt']
    h={'Authorization':jwt}

    # Happy path with many ingredients
    ing=[f"i{i}" for i in range(20)]
    if not ok(requests.post(BASE+"/create_recipe", data={'name':'Big','description':'desc','recipe_id':500,'ingredients':json.dumps(ing)}, headers=h)): fail()

    # Duplicate id should fail
    if ok(requests.post(BASE+"/create_recipe", data={'name':'Big2','description':'desc2','recipe_id':500}, headers=h)):
        fail()

    # Missing ingredients allowed (should still pass)
    if not ok(requests.post(BASE+"/create_recipe", data={'name':'NoIngs','description':'desc','recipe_id':501}, headers=h)):
        fail()

    # Bad json ingredients
    if ok(requests.post(BASE+"/create_recipe", data={'name':'BadJson','description':'d','recipe_id':502,'ingredients':'{"oops"'}, headers=h)):
        fail()

    # Long-ish name/description within limits
    name='N'*100; desc='D'*500
    if not ok(requests.post(BASE+"/create_recipe", data={'name':name,'description':desc,'recipe_id':503,'ingredients':json.dumps(['x'])}, headers=h)):
        fail()

    # Invalid recipe_id type
    if ok(requests.post(BASE+"/create_recipe", data={'name':'X','description':'Y','recipe_id':'notint'}, headers=h)):
        fail()

    print('Test Passed')
except:
    print('Test Failed')



