import requests
import json

BASE = "http://127.0.0.1:5000"

def fail():
    print('Test Failed')
    raise SystemExit

def ok(x):
    return x.json().get('status') == 1

try:
    # Reset
    requests.get(BASE+"/clear")

    # Users
    u1={'first_name':'Ada','last_name':'Zephyr','username':'ada','email_address':'ada@x.com','password':'Qx7Yt9Lp','salt':'s'}
    u2={'first_name':'Ben','last_name':'Yarrow','username':'ben','email_address':'ben@x.com','password':'Qx7Yt9Lp','salt':'s'}
    u3={'first_name':'Cy','last_name':'Xenon','username':'cy','email_address':'cy@x.com','password':'Qx7Yt9Lp','salt':'s'}
    for u in (u1,u2,u3):
        if not ok(requests.post(BASE+"/create_user", data=u)): fail()
    jwt1=requests.post(BASE+"/login", data={'username':'ada','password':'Qx7Yt9Lp'}).json()['jwt']
    jwt2=requests.post(BASE+"/login", data={'username':'ben','password':'Qx7Yt9Lp'}).json()['jwt']
    jwt3=requests.post(BASE+"/login", data={'username':'cy','password':'Qx7Yt9Lp'}).json()['jwt']

    h1={'Authorization':jwt1}
    h2={'Authorization':jwt2}
    h3={'Authorization':jwt3}

    # ben and cy create recipes with timing and ingredients; like counts to test popular tiebreakers
    # ben: 201 (2 likes), 202 (2 likes)
    # cy:  203 (1 like), 204 (0 likes)
    for rid, name, ings, hdr in [
        (201, 'B1', ['x','y'], h2),
        (202, 'B2', ['x'], h2),
        (203, 'C1', ['y'], h3),
        (204, 'C2', ['x','z'], h3),
    ]:
        if not ok(requests.post(BASE+"/create_recipe", data={'name':name,'description':'d','recipe_id':rid,'ingredients':json.dumps(ings)}, headers=hdr)):
            fail()

    # Likes (ada + the other author to build counts)
    # 201: liked by ada and cy => 2
    # 202: liked by ada and cy => 2
    # 203: liked by ada => 1
    # 204: 0
    for rid, hdr in [(201,h1),(201,h3),(202,h1),(202,h3),(203,h1)]:
        requests.post(BASE+"/like", data={'recipe_id':rid}, headers=hdr)

    # ada follows ben and cy
    if not ok(requests.post(BASE+"/follow", data={'username':'ben'}, headers=h1)): fail()
    if not ok(requests.post(BASE+"/follow", data={'username':'cy'}, headers=h1)): fail()

    # 1) popular: should return top 2 by like count; tie broken by created_at DESC then recipe_id ASC from app
    pop = requests.get(BASE+"/search", params={'popular':'True'}, headers=h1).json()
    if pop.get('status') != 1: fail()
    if len(pop['data']) != 2: fail()
    # both 201 and 202 have 2 likes; newer created should appear first, then recipe_id ASC resolves tie among equal timestamps
    ids = list(pop['data'].keys())
    if set(ids) != set(['201','202']): fail()

    # 2) ingredients: exact-only set rule
    # query ['x'] should return only 202
    ing = requests.get(BASE+"/search", params={'ingredients':json.dumps(['x'])}, headers=h1).json()
    if ing.get('status') != 1: fail()
    if set(ing['data'].keys()) != set(['202']): fail()

    # query ['x','y'] should return 201 (has x,y) but not 204 (has z)
    ing2 = requests.get(BASE+"/search", params={'ingredients':json.dumps(['x','y'])}, headers=h1).json()
    if ing2.get('status') != 1: fail()
    if '201' not in ing2['data'] or '204' in ing2['data']: fail()

    # empty ingredient list -> per implementation returns none
    ing_empty = requests.get(BASE+"/search", params={'ingredients':json.dumps([])}, headers=h1).json()
    if ing_empty.get('status') != 1 or len(ing_empty['data']) != 0: fail()

    # bad json ingredients
    bad = requests.get(BASE+"/search", params={'ingredients':'notjson'}, headers=h1).json()
    if bad.get('status') != 2 or bad.get('data') != 'NULL': fail()

    # 3) feed: last two most recent from followed users
    feed = requests.get(BASE+"/search", params={'feed':'True'}, headers=h1).json()
    if feed.get('status') != 1 or len(feed['data']) != 2: fail()

    # 4) bad JWT for any search path
    if requests.get(BASE+"/search", params={'feed':'True'}).json().get('status') != 2: fail()
    if requests.get(BASE+"/search", params={'popular':'True'}).json().get('status') != 2: fail()

    print('Test Passed')
except:
    print('Test Failed')



