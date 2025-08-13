from dotenv import load_dotenv
import os

from menus import Menu
from repositories.usuario import UsuarioRepository
from storage.db import init_db
from config import init_config


def main():
    repo, db_session = init_config()

    menu = Menu(repo, db_session)
    menu.init_menu()

if __name__ == "__main__":
    main()
