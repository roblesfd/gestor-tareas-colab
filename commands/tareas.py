import argparse 

def add_task(args):
    """ Añadir una nueva tarea """
    title = args.title
    description = args.description or ""
    print(f"✅ Tarea añadida: {title} - {description}")

def list_tasks(args):
    """ Listar tareas """
    print("📋 Lista de tareas:")
    print("1. Estudiar Python")
    print("2. Terminar Proyecto CLI")
    
def update_task(args):
    task_id = args.id
    title = args.title 
    description = args.description or " "
    print(f"✏️ Tarea {task_id} actualizada a: {title} - {description}")

def delete_task(args):
    task_id = args.id 
    print(f"🗑️ Tarea {task_id} eliminada")