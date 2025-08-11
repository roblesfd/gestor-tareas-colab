import os

def clear_screen():
    # Para Windows
    if os.name == 'nt':
        os.system('cls')
    else:
        # Para Linux y macOS
        os.system('clear')
