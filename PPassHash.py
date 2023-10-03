import bcrypt

def encrypt(passwd):
    bpasswd = passwd.encode('utf-8')
    salt = bcrypt.gensalt(rounds=10)
    hashed_passwd = bcrypt.hashpw(bpasswd, salt)
    return hashed_passwd

def verify(passwd,hashed_passwd):
    bpasswd = passwd.encode('utf-8')
    if bcrypt.checkpw(bpasswd, hashed_passwd):
        return True
    else:
        return False