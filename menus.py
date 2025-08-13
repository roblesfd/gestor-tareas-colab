from utils.helpers import clear_screen
from repositories.usuario import UsuarioRepository
from storage.db import init_db
from utils.exceptions import UserNotFoundError
from models.usuario import Usuario
from services.usuario import UsuarioService

from prompt_toolkit import prompt, print_formatted_text, HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.validation import Validator, ValidationError

from sqlalchemy.orm import session
import time
import textwrap
import os

class NonEmptyValidator(Validator):
    def validate(self, document):
        if not document.text.strip():
            raise ValidationError("Este campo no puede estar vacío", cursor_position=len(document.text))

class Menu:

    _db_url = None
    _repo = UsuarioRepository()
    _db_session = None
    _user_service = None

    def __init__(self, db_url:str, db_session:session):
        self._db_url = db_url
        self._db_session = db_session
        self._user_service = UsuarioService(self._repo, self._db_session)


    def __display_prompt(self, options_text, menu_options):
        clear_screen()
        print_formatted_text(HTML(options_text))
        option = prompt("> ", completer=menu_options)

        return option


    def task_menu(self):
        options_text = """
        <bold>===== Submenú Gestión de tareas =====</bold>

        <bold>añadir</bold>: Añadir una tarea
        <bold>regresar</bold>: Regresar

        """
        menu_options = WordCompleter(['añadir', 'regresar'], ignore_case=True)

        while True:
            option = self.__display_prompt(options_text, menu_options) 

            match option: 
                case 'añadir':
                    print(f"Añadiste una tarea")
                case 'regresar':
                    break
                case _:
                    print_formatted_text("Opción inválida")

    def addtask_menu(self):
        title_text = """
        <bold>===== Añadir una tareas =====</bold>
        """
        menu_options = WordCompleter(['añadir', 'regresar'], ignore_case=True)

        while True:
            print_formatted_text(HTML(title_text))
            titulo = prompt("Titulo: ", validator=NonEmptyValidator())
            descripcion = prompt("Descripción: ", is_password=True, validator=NonEmptyValidator())
            fecha_vencimiento = prompt("Fecha de vencimiento (dia-mes-año:horas-minutos): ", is_password=True, validator=NonEmptyValidator())

            # match option: 
            #     case 'añadir':
            #         print(f"Añadiste una tarea")
            #     case 'regresar':
            #         break
            #     case _:
            #         print_formatted_text("Opción inválida")



    def user_menu(self):
        options_text = """
        <bold>===== Submenú Gestión de usuarios =====</bold>

        <bold>añadir</bold>: Añadir un usuario
        <bold>regresar</bold>: Regresar
        """
        menu_options = WordCompleter(['añadir', 'regresar'], ignore_case=True)

        while True:
            option = self.__display_prompt(options_text, menu_options) 

            match option.lower():
                case 'añadir': 
                    print(f"Añadiste un usuario")
                case 'regresar':
                    break
                case _:
                    print("Opción inválida")


    # Menu principal del sistema, para usuarios sin autenticar/registrar
    def init_menu(self):
        options_text = textwrap.dedent("""
        <bold> ===== Sistema de gestión de tareas y proyectos =====</bold>

        Ingresa una de las siguientes opciones:
        
        <bold>ingresar</bold>: Ingresar con cuenta de usuario
        <bold>registrar</bold>: Registrar una cuenta de usuario nueva
        <bold>salir</bold>: Salir del sistema
        """)
        menu_options = WordCompleter(['ingresar', 'registrar', 'salir'], ignore_case=True)

        while True:
            option = self.__display_prompt(options_text, menu_options) 

            match option.lower():
                case 'ingresar':
                    self.login_menu()
                case 'registrar':
                    self.signup_menu()
                case 'salir':
                    break
                case _:
                    print_formatted_text("Opción inválida")


    def login_menu(self, max_attempts=5):
        title_text = textwrap.dedent("""
        <bold> ===== Ingresa a tu cuenta =====</bold>

        Ingresa tus credenciales para iniciar sesión
        
        """)
        count = 0

        while count < max_attempts:

            print_formatted_text(HTML(title_text))
            username = prompt("Usuario: ", validator=NonEmptyValidator())
            password = prompt("Contraseña: ", is_password=True, validator=NonEmptyValidator())

            usuario = self._user_service.authenticate(username, password)
            
            if usuario:
                print_formatted_text("Iniciaste sesión")
                self.main_menu()
                break
            else:
                print_formatted_text("Nombre de usuario y/o contraseña incorrectos")
                count += 1


    def signup_menu(self, max_attempts=5):
        title_text = textwrap.dedent("""
        <bold> ===== Registra una cuenta =====</bold>

        Ingresa tus datos para crear una cuenta de usuario
        
        """)
        count = 0

        while count < max_attempts:
            print_formatted_text(HTML(title_text))
            nombre = prompt("Usuario: ", validator=NonEmptyValidator())
            email = prompt("Correo electrónico: ", validator=NonEmptyValidator())
            password = prompt("Contraseña: ", is_password=True, validator=NonEmptyValidator())

            saved_user = self._user_service.signup(self, nombre, email, password)

            if saved_user:
                return saved_user
            else:
                print("error")
                count += 1


    # Menu para el usuario autenticado    
    def main_menu(self):
        options_text = textwrap.dedent("""
        <bold> ===== Menú principal =====</bold>

        Ingresa una de las siguientes opciones:
        
        <bold>tareas</bold>: Gestión de Tareas
        <bold>usuarios</bold>: Gestión de Usuarios
        <bold>salir</bold>: Salir

        """)
        menu_options = WordCompleter(['tareas', 'usuarios', 'salir'], ignore_case=True)

        while True:
            option = self.__display_prompt(options_text, menu_options) 

            match option.lower():
                case 'tareas':
                    self.task_menu()
                case 'usuarios':
                    self.user_menu()
                case 'salir':
                    break
                case _:
                    print_formatted_text("Opción inválida")
 

