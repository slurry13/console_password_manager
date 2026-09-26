import database
import crypto
import session
import getpass
from cryptography.fernet import Fernet

database.init_db()

CHECK_PHRASE = "hi_i_am_here"

current_session = session.Session()

def registration():
    new_username = input("Username: ")
    new_password = getpass.getpass()

    u_salt = crypto.make_salt()
    fer_us = crypto.fernet(new_password, u_salt)

    enc_phrase = fer_us.encrypt(CHECK_PHRASE.encode('utf-8'))
    a_verif = enc_phrase.decode('utf-8')

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
            current_session.user_id = id_us
            current_session.fernet_user = fer_user
            current_session.is_active = True

        else:
            print("Err: Anexpected master pass")

    except Exception:
        print("Err: Anexpected master pass")

def add_passwords():
    new_service = input("URL/NAME: ")
    new_login = input("Login: ")
    new_password = getpass.getpass()

    enc_url = current_session.fernet_user.encrypt(new_service.encode('utf-8')).decode('utf-8')
    enc_login = current_session.fernet_user.encrypt(new_login.encode('utf-8')).decode('utf-8')
    enc_pass = current_session.fernet_user.encrypt(new_password.encode('utf-8')).decode('utf-8')

    database.add_password(current_session.user_id, enc_url, enc_login, enc_pass)

while(True):
    cmd = input()

    if not current_session.user_id:

        if cmd == "reg":
            registration()
        elif cmd == "log":
            login()
        else:
            print(f"Unexpected cmd - {cmd}")

    else:
        if cmd == "q":
            print("Scs: Quit")
            current_session.clear()
        else:
            print(f"Unexpected cmd - {cmd}")