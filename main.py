import database
import session
import getpass
import secrets
import string
import businesslogic

database.init_db()

current_session = session.Session()

def cmd_list():
    print('''
    q - quit from user;
    reg - reg new user;
    log - login in your acc;
    new - add new pass;
    pwds - show your passwords;
    gen - generate passwords;
    help - show all commands;
    ''')

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


def add_passwords():
    new_service = input("URL/NAME: ")
    new_login = input("Login: ")
    new_password = getpass.getpass()

    enc_url = current_session.fernet_user.encrypt(new_service.encode('utf-8')).decode('utf-8')
    enc_login = current_session.fernet_user.encrypt(new_login.encode('utf-8')).decode('utf-8')
    enc_pass = current_session.fernet_user.encrypt(new_password.encode('utf-8')).decode('utf-8')

    database.add_password(current_session.user_id, enc_url, enc_login, enc_pass)

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

            print(f"{url:<40} | {log:<40} | {passw:<40}")
        except Exception:
            print("Err: Decrypt values")

def password_generator():
    password_length = int(input("Length: "))
    
    flag_special_symbols = input("Special symbols(0/1): ") == "1"
    flag_numbers = input("Numbers(0/1): ") == "1"

    password_alphabet = string.ascii_letters

    if flag_numbers:
        password_alphabet += string.digits

    if flag_special_symbols:
        password_alphabet += string.punctuation

    generated_password = "".join(
        secrets.choice(password_alphabet) for _ in range(password_length)
    )

    print(f"Your password: {generated_password}")




while(True):
    cmd = input()

    if not current_session.user_id:

        if cmd == "reg":
            businesslogic.registration()
        elif cmd == "log":
            businesslogic.login()
        else:
            print(f"Unexpected cmd - {cmd}")

    else:
        if cmd == "q":
            print("Scs: Quit")
            current_session.clear()
        elif cmd == "new":
            add_passwords()
        elif cmd == "pwds":
            give_passwords()
        elif cmd == "gen":
            password_generator()
        elif cmd == "help":
            cmd_list()
        else:
            print(f"Unexpected cmd - {cmd}")