from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

menu_completer = WordCompleter(['Agregar', 'Listar', 'Actualizar', 'Eliminar', 'Salir'], ignore_case=True)

def main():
    while True:
        opcion = prompt('Selecciona una opción: ', completer=menu_completer)
        
        if opcion.lower() == 'agregar':
            print("Has seleccionado Agregar")
        elif opcion.lower() == 'listar':
            print("Has seleccionado Listar")
        elif opcion.lower() == 'actualizar':
            print("Has seleccionado Actualizar")
        elif opcion.lower() == 'eliminar':
            print("Has seleccionado Eliminar")
        elif opcion.lower() == 'salir':
            print("Saliendo...")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == '__main__':
    main()
