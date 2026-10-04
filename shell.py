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
  ╚═════╝╚═╝     ╚═╝     ╚═╝"""
    print(banner)
    print("=" * 30)
    print("   Console Password Manager")
    print("=" * 30 + "\n")
