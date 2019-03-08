def loadMatrix(path2file = None):
    pass

def face(program):
    from pyfiglet import figlet_format
    import os
    import shutil
    from colorama import init
    from os import sys
    init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
    from termcolor import cprint
    columns = shutil.get_terminal_size().columns
    os.system('clear')
    cprint(figlet_format('VISIO Golden',font='speed'),'yellow',attrs=['bold'])
    print(program.center(columns))
    print("\n")
