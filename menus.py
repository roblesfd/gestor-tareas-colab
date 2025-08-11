from cli import create_tasks_parser 
from commands.tareas import add_task, list_tasks, update_task, delete_task
from utils.helpers import clear_screen

from prompt_toolkit import prompt, print_formatted_text, HTML
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear
import time

def display_prompt(option_text, menu):
        clear_screen()
        print_formatted_text(HTML(option_text))
        option = prompt("> ", completer=menu)  

        return option


def task_menu():
    option_text = """
        <bold>Submenú Gestión de tareas</bold>

        <bold>añadir</bold>: Añadir una tarea
        <bold>regresar</bold>: Regresar

    """
    menu = WordCompleter(['añadir', 'regresar'], ignore_case=True)

    while True:
        option = display_prompt(option_text, menu) 

        match option: 
            case 'añadir':
                print(f"Añadiste una tarea")
            case 'regresar':
                break
            case _:
                print("Opción inválida")



def user_menu():
    option_text = """
        <bold>Submenú Gestión de usuarios</bold>

        <bold>añadir</bold>: Añadir un usuario
        <bold>regresar</bold>: Regresar

    """
    menu = WordCompleter(['añadir', 'regresar'], ignore_case=True)

    while True:
        option = display_prompt(option_text, menu) 

        match option.lower():
            case 'añadir': 
                print(f"Añadiste un usuario")
            case 'regresar':
                break
            case _:
                print("Opción inválida")

def main_menu():
    option_text = """
        <bold>Menú principal</bold>
        
        <bold>tareas</bold>: Gestión de Tareas
        <bold>usuarios</bold>: Gestión de Usuarios
        <bold>salir</bold>: Salir

    """
    menu = WordCompleter(['tareas', 'usuarios', 'salir'], ignore_case=True)

    while True:
        option = display_prompt(option_text, menu) 

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
