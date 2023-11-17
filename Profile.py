import mysql.connector
import json
import base64
import bcrypt
import EncryptDecrypt

def get_db_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS passmanage")
    cursor.execute("USE passmanage")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            userid VARCHAR(255),
            passwd_and_key VARCHAR(255),
            PRIMARY KEY (userid)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            userid VARCHAR(255),
            label VARCHAR(255),
            encrypted_passwd VARCHAR(255),
            PRIMARY KEY (userid, label),
            FOREIGN KEY (userid) REFERENCES profiles(userid)
        )
    """)
    return db

def hashing(passwd):
    bpasswd = passwd.encode('utf-8')
    salt = bcrypt.gensalt(rounds=10)
    hashed_passwd = bcrypt.hashpw(bpasswd, salt)
    return hashed_passwd,salt

def save_profile(userid, passwd):
    db = get_db_connection()
    cursor = db.cursor()
    hashed_passwd, salt = hashing(passwd)
    key = EncryptDecrypt.generate_key(passwd, salt)
    passwd_and_key = [base64.b64encode(hashed_passwd).decode('utf-8'), base64.b64encode(key).decode('utf-8')]
    # Convert the list to a string
    passwd_and_key_str = json.dumps(passwd_and_key)
    query = "INSERT INTO profiles (userid, passwd_and_key) VALUES (%s, %s)"
    cursor.execute(query, (userid, passwd_and_key_str))
    db.commit()

def verify_profile(userid, passwd):
    db = get_db_connection()
    cursor = db.cursor()
    query = "SELECT passwd_and_key FROM profiles WHERE userid = %s"
    cursor.execute(query, (userid,))
    result = cursor.fetchone()
    if result is None:
        raise Exception("User does not exist")
    passwd_and_key = json.loads(result[0])
    hashed_passwd_str = passwd_and_key[0]
    hashed_passwd = base64.b64decode(hashed_passwd_str.encode('utf-8'))
    bpasswd = passwd.encode('utf-8')
    if bcrypt.checkpw(bpasswd, hashed_passwd):
        return True
    return False

def retrieve_key(userid):
    db = get_db_connection()
    cursor = db.cursor()
    query = "SELECT passwd_and_key FROM profiles WHERE userid = %s"
    cursor.execute(query, (userid,))
    result = cursor.fetchone()
    if result is None:
        print("User does not exist")
        return None
    passwd_and_key = json.loads(result[0])
    key_str = passwd_and_key[1]
    key = base64.b64decode(key_str.encode('utf-8'))
    return key

def passfile_store(userid, label, stored_passwd):
    db = get_db_connection()
    cursor = db.cursor()
    key = retrieve_key(userid)
    if key is None:
        print("User does not exist")
        return
    encrypted_passwd = EncryptDecrypt.encrypt(stored_passwd, key)
    encrypted_passwd_64 = base64.b64encode(encrypted_passwd).decode('utf-8')
    query = "INSERT INTO passwords (userid, label, encrypted_passwd) VALUES (%s, %s, %s)"
    cursor.execute(query, (userid, label, encrypted_passwd_64))
    db.commit()

def passfile_retrieve(userid, label):
    db = get_db_connection()
    cursor = db.cursor()
    query = "SELECT encrypted_passwd FROM passwords WHERE userid = %s AND label = %s"
    cursor.execute(query, (userid, label))
    result = cursor.fetchone()
    if result is None:
        return None
    encrypted_passwd_64 = result[0]
    encrypted_passwd = base64.b64decode(encrypted_passwd_64.encode('utf-8'))
    key = retrieve_key(userid)
    if key is None:
        return None
    decrypted_passwd = EncryptDecrypt.decrypt(encrypted_passwd, key)
    return decrypted_passwd