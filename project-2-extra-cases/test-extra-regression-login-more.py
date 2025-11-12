import requests

BASE = "http://127.0.0.1:5000"

def fail():
    print('Test Failed'); raise SystemExit

def ok(r): return r.json().get('status') == 1

try:
    requests.get(BASE+"/clear")
    u={'first_name':'Nia','last_name':'Pry','username':'user','email_address':'user@x.com','password':'Qx7Yt9Lp','salt':'s'}
    if not ok(requests.post(BASE+"/create_user", data=u)): fail()

    # Case sensitivity: usernames case-sensitive, passwords exact match
    if requests.post(BASE+"/login", data={'username':'User','password':'Qx7Yt9Lp'}).json().get('status') != 2: fail()
    if requests.post(BASE+"/login", data={'username':'user','password':'qx7yt9lp'}).json().get('status') != 2: fail()

    # Missing fields
    if requests.post(BASE+"/login", data={'username':'user'}).json().get('status') != 2: fail()
    if requests.post(BASE+"/login", data={'password':'Qx7Yt9Lp'}).json().get('status') != 2: fail()

    # Success
    if not ok(requests.post(BASE+"/login", data={'username':'user','password':'Qx7Yt9Lp'})): fail()

    print('Test Passed')
except:
    print('Test Failed')



