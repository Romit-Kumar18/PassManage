import json
import base64
import bcrypt

def encrypt(passwd):
    bpasswd = passwd.encode('utf-8')
    salt = bcrypt.gensalt(rounds=10)
    hashed_passwd = bcrypt.hashpw(bpasswd, salt)
    return hashed_passwd

def save_profile(userid,passwd): 
    with open('Profiles.json','r+') as dbfile:
        try:
            profiles=json.load(dbfile)
        except json.JSONDecodeError:
            profiles={}
        profiles[userid]=base64.b64encode(encrypt(passwd)).decode('utf-8')
        dbfile.seek(0)
        json.dump(profiles, dbfile, indent=2)
        dbfile.truncate()

def verify_profile(userid,passwd):
    verification=False
    with open('Profiles.json','r') as dbfile:
        try:
            profiles=json.load(dbfile)
            hashed_passwd_str=profiles[userid]
            hashed_passwd=base64.b64decode(hashed_passwd_str.encode('utf-8'))
            bpasswd=passwd.encode('utf-8')
            if bcrypt.checkpw(bpasswd, hashed_passwd):
                verification=True
        except (KeyError,json.JSONDecodeError):
            print("User does not exist or JSON decode error")
    dbfile.close()
    return verification