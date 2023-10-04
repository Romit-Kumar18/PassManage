import json
import base64
import bcrypt
import EncryptDecrypt

def hashing(passwd):
    bpasswd = passwd.encode('utf-8')
    salt = bcrypt.gensalt(rounds=10)
    hashed_passwd = bcrypt.hashpw(bpasswd, salt)
    return hashed_passwd,salt

def save_profile(userid,passwd):
    with open('Profiles.json','r+') as dbfile:
        hashed_passwd,salt=hashing(passwd)
        key=EncryptDecrypt.generate_key(passwd,salt)
        try:
            profiles=json.load(dbfile)
        except json.JSONDecodeError:
            profiles={}
        passwd_and_key=[base64.b64encode(hashed_passwd).decode('utf-8'),base64.b64encode(key).decode('utf-8')]
        profiles[userid]=passwd_and_key
        dbfile.seek(0)
        json.dump(profiles, dbfile, indent=2)
        dbfile.truncate()

def verify_profile(userid,passwd):
    verification=False
    with open('Profiles.json','r') as dbfile:
        try:
            profiles=json.load(dbfile)
            hashed_passwd_str=profiles[userid[0]]
            hashed_passwd=base64.b64decode(hashed_passwd_str[0].encode('utf-8'))
            bpasswd=passwd.encode('utf-8')
            if bcrypt.checkpw(bpasswd, hashed_passwd):
                verification=True
                dbfile.close()
            return verification
        except (KeyError,json.JSONDecodeError):
            print("User does not exist or JSON decode error")
            dbfile.close()
            return verification