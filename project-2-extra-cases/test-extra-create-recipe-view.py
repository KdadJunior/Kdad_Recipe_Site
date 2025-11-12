import requests
import json

BASE = "http://127.0.0.1:5000"

def pr(x):
    print(x)

try:
    requests.get(BASE+"/clear")
    u={'first_name':'Nova','last_name':'Quade','username':'charlie','email_address':'c@x.com','password':'Qx7Yt9Lp','salt':'s'}
    requests.post(BASE+"/create_user", data=u)
    jwt = requests.post(BASE+"/login", data={'username':'charlie','password':'Qx7Yt9Lp'}).json()['jwt']

    # bad jwt
    if requests.post(BASE+"/create_recipe", data={'name':'n','description':'d','recipe_id':1}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit

    # missing fields
    if requests.post(BASE+"/create_recipe", data={'name':'n'}, headers={'Authorization':jwt}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit

    # invalid recipe_id type
    if requests.post(BASE+"/create_recipe", data={'name':'n','description':'d','recipe_id':'abc'}, headers={'Authorization':jwt}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit

    # invalid ingredients JSON
    if requests.post(BASE+"/create_recipe", data={'name':'n','description':'d','recipe_id':1,'ingredients':'notjson'}, headers={'Authorization':jwt}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit

    # happy path
    if requests.post(BASE+"/create_recipe", data={'name':'R','description':'D','recipe_id':1,'ingredients':json.dumps(['i1','i2'])}, headers={'Authorization':jwt}).json().get('status') != 1:
        pr('Test Failed'); raise SystemExit

    # duplicate id
    if requests.post(BASE+"/create_recipe", data={'name':'R2','description':'D2','recipe_id':1}, headers={'Authorization':jwt}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit

    # view_recipe flags combos
    h={'Authorization':jwt}
    r = requests.get(BASE+"/view_recipe/1", params={'name':'True','description':'True','likes':'True','ingredients':'True'}, headers=h)
    jd = r.json();
    if jd.get('status') != 1: pr('Test Failed'); raise SystemExit
    need = ['name','description','likes','ingredients']
    if any(k not in jd['data'] for k in need): pr('Test Failed'); raise SystemExit

    # bad jwt view
    if requests.get(BASE+"/view_recipe/1", params={'name':'True'}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit

    pr('Test Passed')
except:
    pr('Test Failed')


