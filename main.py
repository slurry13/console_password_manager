import database
import crypto
import session
import getpass

database.init_db()

CHECK_PHRASE = "hi_i_am_here"

current_session = session.Session()

def print_banner():
    banner = r"""
  ██████╗██████╗ ███╗   ███╗
 ██╔════╝██╔══██╗████╗ ████║
 ██║     ██████╔╝██╔████╔██║
 ██║     ██╔═══╝ ██║ ╚═╝ ██║
 ╚██████╗██║     ██║     ██║
  ╚═════╝╚═╝     ╚═╝     ╚═╝
    """
    print(banner)
    print("=" * 30)
    print("   Console Password Manager")
    print("=" * 30 + "\n")

print_banner()

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

            give_passwords()

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

    give_passwords()

def give_passwords():
    records = database.get_passwords(current_session.user_id)

    if not records:
        print("Err: You dont have PWDs, to add one use - new")
        return None

    for enc_url, enc_login, enc_pass in records:
        try:
            url = current_session.fernet_user.decrypt(enc_url.encode('utf-8')).decode('utf-8')
            log = current_session.fernet_user.decrypt(enc_login.encode('utf-8')).decode('utf-8')
            passw = current_session.fernet_user.decrypt(enc_pass.encode('utf-8')).decode('utf-8')

            print(f"{url:<20} | {log:<20} | {passw:<20}")
        except Exception:
            print("Err: Decrypt values")



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
        elif cmd == "new":
            add_passwords()
        else:
            print(f"Unexpected cmd - {cmd}")