import database
import crypto
import session
import getpass

database.init_db()

ch_phrase = "hi_i_am_here"

def registration():
    new_username = input("Username: ")
    new_password = getpass.getpass()

    u_salt = crypto.make_salt()
    fer_us = crypto.fernet(new_password, u_salt)

    enc_phrase = fer_us.encrypt(ch_phrase.encode('utf-8'))
    a_verif = enc_phrase.decode('utf-8')

    database.new_user(new_username, u_salt, a_verif)

def login():
    username = input("Username: ")
    password = getpass.getpass()

    salt, a_verif = database.get_val(username)

    fer_check = crypto.fernet(password, salt)

    enc_phrase = fer_check.encrypt(ch_phrase.encode('utf-8'))
    verif_ph = enc_phrase.decode('utf-8')

    if a_verif == verif_ph:
        print("scs")

while(True):
    cmd = input()

    if cmd == "reg":
        registration()
    elif cmd == "log":
        login()