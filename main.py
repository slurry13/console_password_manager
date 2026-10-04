import database
import session
import getpass
import secrets
import string
import commands

database.init_db()



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





while(True):
    cmd = input()

    if not commands.current_session.user_id:

        if cmd == "reg":
            commands.registration()
        elif cmd == "log":
            commands.login()
        else:
            print(f"Unexpected cmd - {cmd}")

    else:
        if cmd == "q":
            print("Scs: Quit")
            commands.current_session.clear()
        elif cmd == "new":
            commands.add_passwords()
        elif cmd == "pwds":
            commands.give_passwords()
        elif cmd == "gen":
            commands.password_generator()
        elif cmd == "help":
            cmd_list()
        else:
            print(f"Unexpected cmd - {cmd}")