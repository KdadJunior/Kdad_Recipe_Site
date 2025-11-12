import requests
import json

BASE = "http://127.0.0.1:5000"

def pr(x):
    print(x)

try:
    requests.get(BASE+"/clear")
    # users
    u1={'first_name':'Vera','last_name':'Stone','username':'u1','email_address':'u1@x.com','password':'Qx7Yt9Lp','salt':'s'}
    u2={'first_name':'Orin','last_name':'Trace','username':'u2','email_address':'u2@x.com','password':'Qx7Yt9Lp','salt':'s'}
    requests.post(BASE+"/create_user", data=u1)
    requests.post(BASE+"/create_user", data=u2)
    jwt1=requests.post(BASE+"/login", data={'username':'u1','password':'Qx7Yt9Lp'}).json()['jwt']
    jwt2=requests.post(BASE+"/login", data={'username':'u2','password':'Qx7Yt9Lp'}).json()['jwt']

    # u2 creates recipes, varying likes/ingredients
    h2={'Authorization':jwt2}
    requests.post(BASE+"/create_recipe", data={'name':'A','description':'d','recipe_id':101,'ingredients':json.dumps(['x','y'])}, headers=h2)
    requests.post(BASE+"/create_recipe", data={'name':'B','description':'d','recipe_id':102,'ingredients':json.dumps(['x'])}, headers=h2)
    requests.post(BASE+"/create_recipe", data={'name':'C','description':'d','recipe_id':103,'ingredients':json.dumps(['z'])}, headers=h2)

    # likes: u1 likes 101 twice (second should fail) and 102 once
    h1={'Authorization':jwt1}
    requests.post(BASE+"/like", data={'recipe_id':101}, headers=h1)
    requests.post(BASE+"/like", data={'recipe_id':101}, headers=h1)
    requests.post(BASE+"/like", data={'recipe_id':102}, headers=h1)

    # follow u2 from u1 for feed
    requests.post(BASE+"/follow", data={'username':'u2'}, headers=h1)

    # search: popular -> top 2 by likes
    pop = requests.get(BASE+"/search", params={'popular':'True'}, headers=h1).json()
    if pop.get('status') != 1 or len(pop['data']) != 2:
        pr('Test Failed'); raise SystemExit

    # search: ingredients exact-only rule
    ing = requests.get(BASE+"/search", params={'ingredients':json.dumps(['x'])}, headers=h1).json()
    if pop.get('status') != 1: pr('Test Failed'); raise SystemExit
    # Only recipe 102 should appear (recipe 101 has y which is not allowed; 103 has z)
    if set(ing['data'].keys()) != set(['102']): pr('Test Failed'); raise SystemExit

    # search: feed returns 2 most recent from followed users
    feed = requests.get(BASE+"/search", params={'feed':'True'}, headers=h1).json()
    if feed.get('status') != 1 or len(feed['data']) != 2:
        pr('Test Failed'); raise SystemExit

    # bad JWT for search
    if requests.get(BASE+"/search", params={'popular':'True'}).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit

    # delete: only self-delete allowed and cascades
    # attempt: u1 tries to delete u2 (should fail)
    if requests.post(BASE+"/delete", data={'username':'u2'}, headers=h1).json().get('status') != 2:
        pr('Test Failed'); raise SystemExit
    # self-delete u1
    if requests.post(BASE+"/delete", data={'username':'u1'}, headers=h1).json().get('status') != 1:
        pr('Test Failed'); raise SystemExit

    pr('Test Passed')
except:
    pr('Test Failed')


