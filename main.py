import database
import crypto
import session
import getpass
from cryptography.fernet import Fernet

database.init_db()

CHECK_PHRASE = "hi_i_am_here"

def registration():
    new_username = input("Username: ")
    new_password = getpass.getpass()

    u_salt = crypto.make_salt()
    fer_us = crypto.fernet(new_password, u_salt)

    enc_phrase = fer_us.encrypt(CHECK_PHRASE.encode('utf-8'))
    a_verif = enc_phrase.decode('utf-8')

    print(a_verif)

    database.new_user(new_username, u_salt, a_verif)

def login():
    username = input("Username: ")
    password = getpass.getpass()

    salt, a_db_verif, id_us = database.get_val(username)

    try:
        fer_user = crypto.fernet(password, salt)
        decrypted_phrase = fer_user.decrypt(a_db_verif.encode('utf-8')).decode('utf-8')

        if decrypted_phrase == CHECK_PHRASE:
            print("Scs: Enter")
            session.Session.user_id = id_us
            session.Session.fernet_user = username
            session.Session.is_active = True

        else:
            print("Err: Anexpected master pass")

    except Exception:
        print("Err: Anexpected master pass")


while(True):
    cmd = input()

    if cmd == "reg":
        registration()
    elif cmd == "log":
        login()