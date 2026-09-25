import database
import crypto
import session
import getpass

database.init_db()

def registration():
    new_username = input("Username: ")
    new_password = getpass.getpass()

    u_salt = crypto.make_salt()
    fer_us = crypto.fernet(new_password, u_salt)

    ch_phrase = "hi_i_am_here"
    enc_phrase = fer_us.encrypt(ch_phrase.encode('utf-8'))
    a_verif = enc_phrase.decode('utf-8')

    database.new_user(new_username, u_salt, a_verif)

def login():
    username = print(f"Username: {input()}")
    password = print(f"Password: {getpass(input())}")

while(True):
    cmd = input()

    if cmd == "reg":
        registration()