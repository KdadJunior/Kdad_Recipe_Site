import requests
import json

BASE = "http://127.0.0.1:5000"

def pr(m):
    print(m)

try:
    requests.get(BASE+"/clear")
    # users
    a={'first_name':'Quill','last_name':'Zen','username':'alice','email_address':'a@x.com','password':'Qx7Yt9Lp','salt':'s'}
    b={'first_name':'Rook','last_name':'Volt','username':'bob','email_address':'b@x.com','password':'Qx7Yt9Lp','salt':'s'}
    requests.post(BASE+"/create_user", data=a)
    requests.post(BASE+"/create_user", data=b)
    jwt_a = requests.post(BASE+"/login", data={'username':'alice','password':'Qx7Yt9Lp'}).json()['jwt']
    jwt_b = requests.post(BASE+"/login", data={'username':'bob','password':'Qx7Yt9Lp'}).json()['jwt']

    # follow: bad JWT
    if requests.post(BASE+"/follow", data={'username':'bob'}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit
    # follow: self follow
    if requests.post(BASE+"/follow", data={'username':'alice'}, headers={'Authorization':jwt_a}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit
    # follow: non-existent target
    if requests.post(BASE+"/follow", data={'username':'nope'}, headers={'Authorization':jwt_a}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit
    # follow: happy path then duplicate
    if requests.post(BASE+"/follow", data={'username':'bob'}, headers={'Authorization':jwt_a}).json().get('status') != 1:
        pr('Test Failed'); raise SystemExit
    if requests.post(BASE+"/follow", data={'username':'bob'}, headers={'Authorization':jwt_a}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit

    # create recipes by bob
    h_b={'Authorization':jwt_b}
    for rid,name in [(10,'R1'),(11,'R2')]:
        if requests.post(BASE+"/create_recipe", data={'name':name,'description':'d','recipe_id':rid,'ingredients':json.dumps(['x'])}, headers=h_b).json().get('status') != 1:
            pr('Test Failed'); raise SystemExit

    # like: bad jwt
    if requests.post(BASE+"/like", data={'recipe_id':10}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit
    # like: non-existent recipe
    if requests.post(BASE+"/like", data={'recipe_id':999}, headers={'Authorization':jwt_a}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit
    # like: missing recipe_id
    if requests.post(BASE+"/like", data={}, headers={'Authorization':jwt_a}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit
    # like: ok then duplicate like
    if requests.post(BASE+"/like", data={'recipe_id':10}, headers={'Authorization':jwt_a}).json().get('status') != 1:
        pr('Test Failed'); raise SystemExit
    if requests.post(BASE+"/like", data={'recipe_id':10}, headers={'Authorization':jwt_a}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit

    pr('Test Passed')
except:
    pr('Test Failed')


