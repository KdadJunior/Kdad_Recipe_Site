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

    # Users A (author), B (follower/liker), C (bystander)
    A={'first_name':'Dora','last_name':'Mint','username':'auth','email_address':'a@x.com','password':'Qx7Yt9Lp','salt':'s'}
    B={'first_name':'Eli','last_name':'Nox','username':'fan','email_address':'b@x.com','password':'Qx7Yt9Lp','salt':'s'}
    C={'first_name':'Fia','last_name':'Orb','username':'other','email_address':'c@x.com','password':'Qx7Yt9Lp','salt':'s'}
    for u in (A,B,C):
        if not ok(requests.post(BASE+"/create_user", data=u)): fail()
    jwtA=requests.post(BASE+"/login", data={'username':'auth','password':'Qx7Yt9Lp'}).json()['jwt']
    jwtB=requests.post(BASE+"/login", data={'username':'fan','password':'Qx7Yt9Lp'}).json()['jwt']
    jwtC=requests.post(BASE+"/login", data={'username':'other','password':'Qx7Yt9Lp'}).json()['jwt']

    hA={'Authorization':jwtA}
    hB={'Authorization':jwtB}
    hC={'Authorization':jwtC}

    # A creates two recipes; B follows A and likes one
    if not ok(requests.post(BASE+"/create_recipe", data={'name':'R1','description':'d','recipe_id':301,'ingredients':json.dumps(['x'])}, headers=hA)): fail()
    if not ok(requests.post(BASE+"/create_recipe", data={'name':'R2','description':'d','recipe_id':302,'ingredients':json.dumps(['y'])}, headers=hA)): fail()
    if not ok(requests.post(BASE+"/follow", data={'username':'auth'}, headers=hB)): fail()
    if not ok(requests.post(BASE+"/like", data={'recipe_id':301}, headers=hB)): fail()

    # Pre-delete: B's feed should show A's recipes (2 most recent)
    feed_pre = requests.get(BASE+"/search", params={'feed':'True'}, headers=hB).json()
    if feed_pre.get('status') != 1 or len(feed_pre['data']) != 2: fail()

    # 1) Attempt to delete another user (should fail)
    if requests.post(BASE+"/delete", data={'username':'auth'}, headers=hB).json().get('status') != 2: fail()

    # 2) Bad JWT delete
    if requests.post(BASE+"/delete", data={'username':'auth'}).json().get('status') != 2: fail()

    # 3) Self delete for A; cascades should remove recipes, likes, follows
    if not ok(requests.post(BASE+"/delete", data={'username':'auth'}, headers=hA)): fail()

    # After delete: B's feed should no longer include A's recipes, and feed may be empty
    feed_post = requests.get(BASE+"/search", params={'feed':'True'}, headers=hB).json()
    if feed_post.get('status') != 1:
        fail()

    # View deleted recipe should fail
    vr = requests.get(BASE+"/view_recipe/301", params={'name':'True'}, headers=hB).json()
    if vr.get('status') != 2 or vr.get('data') != 'NULL': fail()

    # Like on deleted recipe should fail
    if requests.post(BASE+"/like", data={'recipe_id':301}, headers=hB).json().get('status') != 2: fail()

    # C tries to follow deleted user
    if requests.post(BASE+"/follow", data={'username':'auth'}, headers=hC).json().get('status') != 2: fail()

    print('Test Passed')
except:
    print('Test Failed')



