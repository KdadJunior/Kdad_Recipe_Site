import requests

BASE = "http://127.0.0.1:5000"

def fail():
    print('Test Failed'); raise SystemExit

def ok(r): return r.json().get('status') == 1

try:
    requests.get(BASE+"/clear")

    # Boundary lengths: exactly 254 chars for fields allowed, 255 disallowed (>= max check)
    def mk(s, n): return s * n
    long254 = mk('a', 254)
    long255 = mk('a', 255)

    # Valid at 254
    u254={'first_name':long254,'last_name':long254,'username':'user254','email_address':'e254@x.com','password':'Qx7Yt9Lp','salt':long254}
    if not ok(requests.post(BASE+"/create_user", data=u254)): fail()

    # Invalid when any >=255
    bads=[
        {**u254, 'username':'user255a', 'first_name':long255},
        {**u254, 'username':'user255b', 'last_name':long255},
        {**u254, 'username':'user255c', 'email_address':('e'+long255+'@x.com')[:300]},
        {**u254, 'username':'user255d', 'password':('Qx7Yt9Lp'+long255)[:300]},
        {**u254, 'username':'user255e', 'salt':long255},
    ]
    for b in bads:
        if ok(requests.post(BASE+"/create_user", data=b)):
            fail()

    # Email and username uniqueness re-check
    if ok(requests.post(BASE+"/create_user", data={**u254, 'username':'dupU', 'email_address':'e254@x.com'})):
        fail()
    if ok(requests.post(BASE+"/create_user", data={**u254, 'username':'user254', 'email_address':'new@x.com'})):
        fail()

    print('Test Passed')
except:
    print('Test Failed')



