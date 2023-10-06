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
        print(passwd_and_key)
        profiles[userid]=passwd_and_key
        dbfile.seek(0)
        json.dump(profiles, dbfile, indent=2)
        dbfile.truncate()
        passfile_create(userid)

def verify_profile(userid,passwd):
    verification=False
    with open('Profiles.json','r') as dbfile:
        try:
            profiles=json.load(dbfile)
            hashed_passwd_str=profiles[userid][0]
            hashed_passwd=base64.b64decode(hashed_passwd_str.encode('utf-8'))
            bpasswd=passwd.encode('utf-8')
            if bcrypt.checkpw(bpasswd,hashed_passwd):
                verification=True
                print("True")
            return verification
        except (KeyError,json.JSONDecodeError):
            print("User does not exist or JSON decode error")
            return verification
        
def retrieve_key(userid):
    with open('Profiles.json','r+') as dbfile:
        try:
            profiles=json.load(dbfile)
            key_str=profiles[userid][1]
            key=base64.b64decode(key_str.encode('utf-8'))
            return key
        except (KeyError,json.JSONDecodeError):
            print("User does not exist or JSON decode error")

def passfile_create(userid):
    with open(f'ProfilePasswords/{userid}.json','w') as psfile:
        passwds={}
        json.dump(passwds,psfile,indent=2)

def passfile_store(userid,label,stored_passwd,key):
    try:
        with open(f'ProfilePasswords/{userid}.json','r+') as psfile:
            encrypted_passwd=EncryptDecrypt.encrypt(stored_passwd,key)
            stored_passwds=json.load(psfile)
            encrypted_passwd_64=base64.b64encode(encrypted_passwd).decode('utf-8')
            stored_passwds[label]=encrypted_passwd_64
            psfile.seek(0)
            json.dump(stored_passwds,psfile,indent=2)
            psfile.truncate()
    except FileNotFoundError:
        print("User does not exist")