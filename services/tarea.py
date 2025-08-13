from sqlalchemy.orm import session
from datetime import datetime

from models.tarea import Tarea
from repositories.tarea import TareaRepository

class TareaService:
    def __init__(self):
        self.repo = TareaRepository()

    def create_task(self, db_session: session, usuario_id: int, titulo: str, descripcion: str = None, fecha_vencimiento: datetime = None) -> Tarea:
        nueva_tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_vencimiento=fecha_vencimiento,
            usuario_id=usuario_id
        )
        return self.repo.create(db_session, nueva_tarea)

    def get_task(self, db_session: session, tarea_id: int) -> Tarea | None:
        return self.repo.get_by_id(db_session, tarea_id)

    def list_user_tasks(self, db_session: session, usuario_id: int) -> list[Tarea]:
        return self.repo.list_by_user(db_session, usuario_id)

    def mark_as_completed(self, db_session: session, tarea_id: int) -> Tarea | None:
        tarea = self.repo.get_by_id(db_session, tarea_id)
        if tarea:
            tarea.completada = True
            return self.repo.update(db_session, tarea)
        return None
    
    def update_task(self, db_session: session, updated_tarea: Tarea) -> Tarea | None:
        tarea = self.repo.get_by_id(db_session, updated_tarea.id)
        if tarea:
            tarea.titulo = updated_tarea.titulo 
            tarea.descripcion = updated_tarea.descripcion
            tarea.fecha_vencimiento = updated_tarea.fecha_vencimiento
            tarea.completada = updated_tarea.completada
            return self.repo.update(db_session, tarea)
        return None


    def delete_task(self, db_session: session, tarea_id: int) -> bool:
        tarea = self.repo.get_by_id(db_session, tarea_id)
        if tarea:
            self.repo.delete(db_session, tarea)
            return True
        return False
