from models.tarea import Tarea 
from sqlalchemy.orm import session 
from sqlalchemy.exc import SQLAlchemyError

from utils.exceptions import (
    TaskNotCreatedError, 
    TaskNotFoundError, 
    TaskNotDeletedError, 
    TaskNotUpdatedError
    )

class TareaRepository:
    def create(self, db_session:session, tarea:Tarea) -> Tarea:
        try:
            db_session.add(tarea)
            db_session.commit()
            db_session.refresh(tarea)
            return tarea
        except SQLAlchemyError as e:
            db_session.rollback()
            raise TaskNotCreatedError("Error al crear la tarea: ", e) from e
    
    def get_by_id(self, db_session: session, tarea_id: int) -> Tarea | None:
        tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
        if not tarea:
            raise TaskNotFoundError(f"Tarea con ID {tarea_id} no encontrada.")
        return tarea

    def list_by_user(self, db: session, usuario_id: int) -> list[Tarea]:
        try: 
            task_list = db.query(Tarea).filter(Tarea.usuario_id == usuario_id).all()
            return task_list
        except SQLAlchemyError as e:
            raise TaskNotFoundError(f"No se encontraron tareas asociadas a este usuario") from e


    def update(self, db: session, tarea: Tarea) -> Tarea:
        try:
            db.commit()
            db.refresh(tarea)
            return tarea
        except SQLAlchemyError as e:
            db.rollback()
            raise TaskNotUpdatedError(f"No se pudo actualizar la tarea con ID {tarea.id}") from e

    def delete(self, db: session, tarea: Tarea) -> None:
        try:
            db.delete(tarea)
            db.commit()
        except SQLAlchemyError as e:
            db.rollback()
            raise ErrorEliminacionTarea(f"No se pudo eliminar la tarea con ID {tarea.id}") from e
