import argparse
from commands.tareas import add_task, list_tasks, update_task, delete_task


def create_tasks_parser():
    parser = argparse.ArgumentParser(
        prog="task-manager",
        description="Sistema de gestión tareas colaborativo"
    )

    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # Comando: add 
    add_task = subparsers.add_parser("addtask", help="Añadir una nueva tarea")
    add_task.add_argument("title", type=str, help="Titulo de la tarea")
    add_task.add_argument("-d", "--description", type=str, help="Descripción de la tarea")

    # Comando: list
    list_parser = subparsers.add_parser("listtasks", help="Listar todas las tareas")

    # Comando: update
    update_parser = subparsers.add_parser("updatetask", help="Actualizar tarea existente")
    update_parser.add_argument("id", type=int, help="ID de la tarea")
    update_parser.add_argument("-t", "--title", type=str, help="Nuevo título")
    update_parser.add_argument("-d", "--description", type=str, help="Nuevo título")

    # Comando delete 
    delete_parser = subparsers.add_parser("deletetasks", help="Eliminar una tarea")
    delete_parser.add_argument("id", type=int, help="ID de la tarea")

    return parser