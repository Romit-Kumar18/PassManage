import json
import base64
import PPassHash as ph

def saveprofile(userid,passwd):    
    with open('Profiles.json','r+') as dbfile:
        try:
            profiles=json.load(dbfile)
        except json.JSONDecodeError:
            profiles={}
        profiles[userid]=base64.b64encode(ph.encrypt(passwd)).decode('utf-8')
        dbfile.seek(0)
        json.dump(profiles, dbfile, indent=2)
        dbfile.truncate()

def verifypass(userid,passwd):
    with open('Profiles.json','r') as dbfile:
        profiles=json.load(dbfile)
        hashed_passwd=profiles[userid]
        hashed_passwd = base64.b64decode(hashed_passwd.encode('utf-8'))
        verification=ph.verify(passwd,hashed_passwd)
    dbfile.close()
    return verification