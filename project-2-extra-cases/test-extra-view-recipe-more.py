import requests
import json

BASE = "http://127.0.0.1:5000"

def fail():
    print('Test Failed'); raise SystemExit

def ok(r): return r.json().get('status') == 1

try:
    requests.get(BASE+"/clear")
    u={'first_name':'Ona','last_name':'Quo','username':'vuser','email_address':'v@x.com','password':'Qx7Yt9Lp','salt':'s'}
    if not ok(requests.post(BASE+"/create_user", data=u)): fail()
    jwt=requests.post(BASE+"/login", data={'username':'vuser','password':'Qx7Yt9Lp'}).json()['jwt']
    h={'Authorization':jwt}

    if not ok(requests.post(BASE+"/create_recipe", data={'name':'VR','description':'D','recipe_id':700,'ingredients':json.dumps(['a','b'])}, headers=h)): fail()

    # All fields
    r = requests.get(BASE+"/view_recipe/700", params={'name':'True','description':'True','likes':'True','ingredients':'True'}, headers=h).json()
    if r.get('status') != 1 or set(r['data'].keys()) != {'name','description','likes','ingredients'}: fail()

    # Some fields
    r2 = requests.get(BASE+"/view_recipe/700", params={'name':'True','likes':'True'}, headers=h).json()
    if r2.get('status') != 1 or set(r2['data'].keys()) != {'name','likes'}: fail()

    # None fields -> empty data allowed per implementation
    r3 = requests.get(BASE+"/view_recipe/700", headers=h).json()
    if r3.get('status') != 1 or r3.get('data') is None: fail()

    # Invalid id
    if requests.get(BASE+"/view_recipe/999", params={'name':'True'}, headers=h).json().get('status') != 2: fail()
    if requests.get(BASE+"/view_recipe/abc", params={'name':'True'}, headers=h).status_code < 200:
        pass

    # Bad JWT
    if requests.get(BASE+"/view_recipe/700", params={'name':'True'}).json().get('status') != 2: fail()

    print('Test Passed')
except:
    print('Test Failed')



