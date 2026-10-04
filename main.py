import database
import commands
import shell
import session

current_session = session.Session()

database.init_db()

shell.print_banner()
shell.cmd_list()

while(True):
    cmd = input()

    if not current_session.user_id:

        if cmd == "reg":
            commands.registration()
        elif cmd == "log":
            commands.login()
        else:
            print(f"Unexpected cmd - {cmd}")

    else:
        if cmd == "q":
            print("Scs: Quit")
            current_session.clear()
        elif cmd == "new":
            commands.add_passwords()
        elif cmd == "pwds":
            commands.give_passwords()
        elif cmd == "gen":
            commands.password_generator()
        elif cmd == "help":
            shell.cmd_list()
        else:
            print(f"Unexpected cmd - {cmd}")