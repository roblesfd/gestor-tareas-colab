from cli import create_tasks_parser 
from commands.tareas import add_task, list_tasks, update_task, delete_task
from utils.helpers import clear_screen

from prompt_toolkit import prompt, print_formatted_text, HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.validation import Validation, ValidationError
import time

class NonEmptyValidator(Validator):
    def validate(self, document):
        if not document.text.strip():
            raise ValidationError("Este campo no puede estar vacío", cursor_position=len(document.text))

class Menu:

    def display_prompt(self, options_text, menu_options):
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
            option = display_prompt(options_text, menu_options) 

            match option: 
                case 'añadir':
                    print(f"Añadiste una tarea")
                case 'regresar':
                    break
                case _:
                    print("Opción inválida")

    def user_menu(self):
        options_text = """
        <bold>===== Submenú Gestión de usuarios =====</bold>

        <bold>añadir</bold>: Añadir un usuario
        <bold>regresar</bold>: Regresar
        """
        menu_options = WordCompleter(['añadir', 'regresar'], ignore_case=True)

        while True:
            option = display_prompt(options_text, menu_options) 

            match option.lower():
                case 'añadir': 
                    print(f"Añadiste un usuario")
                case 'regresar':
                    break
                case _:
                    print("Opción inválida")

    def init_menu(self):
        options_text = """
        <bold> ===== Sistema de gestión de tareas y proyectos =====</bold>

        Ingresa una de las siguientes opciones:
        
        <bold>ingresar</bold>: Ingresar con cuenta de usuario
        <bold>registrar</bold>: Registrar una cuenta de usuario nueva
        <bold>salir</bold>: Salir
        """
        menu_options = WordCompleter(['ingresar', 'registrar', 'salir'], ignore_case=True)

        while True:
            option = display_prompt(options_text, menu_options) 

            match option.lower():
                case 'ingresar':
                    login_menu()
                case 'registrar':
                    signup_menu()
                case 'salir':
                    break
                case _:
                    print("Opción inválida")

    def login_menu(self):
        options_text = """
        <bold> ===== Ingresa a tu cuenta =====</bold>

        Ingresa tus credenciales para iniciar sesión
        
        """

        while True:
            print(options_text) 
            username = prompt("Usuario: ", validator=NonEmptyValidator())
            password = prompt("Contraseña: ", is_password=True, validator=NonEmptyValidator())

    def signup_menu(self):
        pass

    def main_menu():
        options_text = """
        <bold> ===== Menú principal =====</bold>

        Ingresa una de las siguientes opciones:
        
        <bold>tareas</bold>: Gestión de Tareas
        <bold>usuarios</bold>: Gestión de Usuarios
        <bold>salir</bold>: Salir

        """
        menu_options = WordCompleter(['tareas', 'usuarios', 'salir'], ignore_case=True)

        while True:
            option = display_prompt(options_text, menu_options) 

            match option.lower():
                case 'tareas':
                    task_menu()
                case 'usuarios':
                    user_menu()
                case 'salir':
                    break
                case _:
                    print("Opción inválida")




if __name__ == "__main__":
    main_menu()
