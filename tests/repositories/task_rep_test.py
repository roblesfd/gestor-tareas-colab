import pytest
from unittest.mock import patch, MagicMock

from utils.exceptions import UserNotFoundError
from menus import Menu, NonEmptyValidator
from config import init_config
from models.tarea import Tarea
from repositories.tarea import TareaRepository
from utils.exceptions import (
    TaskNotCreatedError, 
    TaskNotFoundError, 
    TaskNotDeletedError, 
    TaskNotUpdatedError
)
from sqlalchemy.exc import SQLAlchemyError

repo = None 
db_session = None
menu = None

@pytest.fixture 
def setup_env():
    repo, db_session = init_config()
    menu = Menu(repo, db_session)

    return menu


# Test si retorna tarea al crearla y guardarla en la db
def test_create_success():
    mock_session = MagicMock()
    tarea = Tarea(id=1, titulo="Test", descripcion="test", usuario_id=1)

    repo = TareaRepository()

    result = repo.create(mock_session, tarea)

    mock_session.add.assert_called_once_with(tarea)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(tarea)
    assert result is tarea 

    
def test_create_failure():
    mock_session = MagicMock()
    tarea = Tarea(id=1, titulo="Test", descripcion="desc", usuario_id=1)

    mock_session.commit.side_effect = SQLAlchemyError("DB error")

    repo = TareaRepository()

    with pytest.raises(TaskNotCreatedError) as excinfo:
        repo.create(mock_session, tarea)

    mock_session.rollback.assert_called_once()
    assert "Error al crear la tarea" in str(excinfo.value)


def test_list_by_user():
    mock_session = MagicMock()
    user_id = 1
    expected_tasks = [
        Tarea(id=1, titulo="Tarea 1", descripcion="Desc 1", usuario_id=user_id),
        Tarea(id=2, titulo="Tarea 2", descripcion="Desc 2", usuario_id=user_id)
    ]

    mock_query = mock_session.query.return_value
    mock_query.filter.return_value.all.return_value = expected_tasks

    repo = TareaRepository()
    result = repo.list_by_user(mock_session, user_id)

    mock_session.query.assert_called_once_with(Tarea)
    mock_query.filter.assert_called_once()
    assert result == expected_tasks


def test_list_by_user_raises_error():
    mock_session = MagicMock()
    mock_session.query.side_effect = TaskNotFoundError("No se encontraron tareas asociadas a este usuario")

    repo = TareaRepository()
    
    with pytest.raises(TaskNotFoundError):
        repo.list_by_user(mock_session, usuario_id=1)


def test_update():
    mock_session =  MagicMock()
    tarea = Tarea(id=1, titulo="Test", descripcion="test", usuario_id=1)

    repo = TareaRepository()
    result = repo.update(mock_session, tarea)

    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(tarea)
    assert result == tarea


def test_update_raises_error():
    tarea = Tarea(id=1, titulo="Test", descripcion="test", usuario_id=1)
    mock_session = MagicMock()
    mock_session.commit.side_effect = TaskNotUpdatedError(f"No se pudo actualizar la tarea con ID {tarea.id}")

    repo = TareaRepository()

    with pytest.raises(TaskNotUpdatedError):
        repo.update(mock_session, tarea)


def test_delete():
    mock_session = MagicMock()
    tarea = Tarea(id=1, titulo="Test", descripcion="test", usuario_id=1)

    repo = TareaRepository()
    repo.delete(mock_session, tarea)

    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()


def test_delete_raises_error():
    tarea = Tarea(id=1, titulo="Test", descripcion="test", usuario_id=1)
    mock_session = MagicMock()
    mock_session.commit.side_effect = TaskNotDeletedError(f"No se pudo eliminar la tarea con ID {tarea.id}")

    repo = TareaRepository()

    with pytest.raises(TaskNotDeletedError):
        repo.delete(mock_session, tarea)