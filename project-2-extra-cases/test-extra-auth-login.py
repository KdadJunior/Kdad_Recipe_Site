import requests
import json

BASE = "http://127.0.0.1:5000"

def pr(msg):
    print(msg)

try:
    # Reset DB
    requests.get(BASE + "/clear")

    # Weak passwords (no uppercase, no digit, too short, contains name)
    weak_cases = [
        {'first_name':'A','last_name':'B','username':'u1','email_address':'u1@x.com','password':'short1A','salt':'s'}, # length 7 -> invalid
        {'first_name':'A','last_name':'B','username':'u2','email_address':'u2@x.com','password':'alllowercase1','salt':'s'}, # no uppercase
        {'first_name':'A','last_name':'B','username':'u3','email_address':'u3@x.com','password':'ALLUPPERCASE1','salt':'s'}, # no lowercase
        {'first_name':'A','last_name':'B','username':'u4','email_address':'u4@x.com','password':'NoDigitsHere','salt':'s'}, # no digit
        {'first_name':'James','last_name':'B','username':'jamesuser','email_address':'u5@x.com','password':'secretJames1','salt':'s'}, # contains first name
        {'first_name':'A','last_name':'Mariani','username':'mari','email_address':'u6@x.com','password':'goodButMariani1','salt':'s'}, # contains last name
        {'first_name':'A','last_name':'B','username':'nameinpass','email_address':'u7@x.com','password':'nameinpass1A','salt':'s'}, # contains username
    ]

    for payload in weak_cases:
        r = requests.post(BASE+"/create_user", data=payload)
        data = r.json()
        if data.get('status') == 1:
            pr('Test Failed')
            raise SystemExit

    # Valid user create and duplicate checks
    good = {'first_name':'Good','last_name':'User','username':'good','email_address':'good@x.com','password':'ValidPass1','salt':'somesalt'}
    r = requests.post(BASE+"/create_user", data=good)
    if r.json().get('status') != 1:
        pr('Test Failed')
        raise SystemExit
    # duplicate username
    r = requests.post(BASE+"/create_user", data={**good, 'email_address':'other@x.com'})
    if r.json().get('status') == 1:
        pr('Test Failed')
        raise SystemExit
    # duplicate email
    r = requests.post(BASE+"/create_user", data={**good, 'username':'othername'})
    if r.json().get('status') == 1:
        pr('Test Failed')
        raise SystemExit

    # Login bad creds
    if requests.post(BASE+"/login", data={'username':'good','password':'WrongPass1'}).json().get('status') != 2:
        pr('Test Failed')
        raise SystemExit
    if requests.post(BASE+"/login", data={'username':'nosuch','password':'ValidPass1'}).json().get('status') != 2:
        pr('Test Failed')
        raise SystemExit

    # Login success
    if requests.post(BASE+"/login", data={'username':'good','password':'ValidPass1'}).json().get('status') != 1:
        pr('Test Failed')
        raise SystemExit

    pr('Test Passed')
except:
    pr('Test Failed')


