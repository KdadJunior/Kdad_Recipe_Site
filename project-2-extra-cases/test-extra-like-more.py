import requests
import json

BASE = "http://127.0.0.1:5000"

def fail():
    print('Test Failed'); raise SystemExit

def ok(r): return r.json().get('status') == 1

try:
    requests.get(BASE+"/clear")
    # Users
    for u in [
        {'first_name':'Kai','last_name':'Sol','username':'a','email_address':'a@x.com','password':'Qx7Yt9Lp','salt':'s'},
        {'first_name':'Lia','last_name':'Ter','username':'b','email_address':'b@x.com','password':'Qx7Yt9Lp','salt':'s'},
        {'first_name':'Moe','last_name':'Uma','username':'c','email_address':'c@x.com','password':'Qx7Yt9Lp','salt':'s'}
    ]:
        if not ok(requests.post(BASE+"/create_user", data=u)): fail()
    jwt_a=requests.post(BASE+"/login", data={'username':'a','password':'Qx7Yt9Lp'}).json()['jwt']
    jwt_b=requests.post(BASE+"/login", data={'username':'b','password':'Qx7Yt9Lp'}).json()['jwt']
    jwt_c=requests.post(BASE+"/login", data={'username':'c','password':'Qx7Yt9Lp'}).json()['jwt']
    h_a={'Authorization':jwt_a}; h_b={'Authorization':jwt_b}; h_c={'Authorization':jwt_c}

    # Create two recipes by user b
    if not ok(requests.post(BASE+"/create_recipe", data={'name':'R1','description':'d','recipe_id':600,'ingredients':json.dumps(['x'])}, headers=h_b)): fail()
    if not ok(requests.post(BASE+"/create_recipe", data={'name':'R2','description':'d','recipe_id':601,'ingredients':json.dumps(['y'])}, headers=h_b)): fail()

    # a likes both; c likes one; duplicate like attempts fail
    if not ok(requests.post(BASE+"/like", data={'recipe_id':600}, headers=h_a)): fail()
    if not ok(requests.post(BASE+"/like", data={'recipe_id':601}, headers=h_a)): fail()
    if not ok(requests.post(BASE+"/like", data={'recipe_id':600}, headers=h_c)): fail()
    if requests.post(BASE+"/like", data={'recipe_id':600}, headers=h_c).json().get('status') != 2: fail()

    # invalid inputs
    if requests.post(BASE+"/like", data={'recipe_id':'notint'}, headers=h_a).json().get('status') != 2: fail()
    if requests.post(BASE+"/like", data={'recipe_id':999}, headers=h_a).json().get('status') != 2: fail()
    if requests.post(BASE+"/like", data={}, headers=h_a).json().get('status') != 2: fail()
    if requests.post(BASE+"/like", data={'recipe_id':600}).json().get('status') != 2: fail()

    print('Test Passed')
except:
    print('Test Failed')



