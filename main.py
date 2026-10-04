import database
import commands

database.init_db()

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