import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from models.tarea import Tarea
from services.tarea import TareaService


# ------------------------
# tests de create_task
# ------------------------
def test_create_task_success():
    mock_session = MagicMock()
    fake_tarea = Tarea(id=1, titulo="Test", descripcion="desc", usuario_id=1)

    service = TareaService()
    service.repo = MagicMock()
    service.repo.create.return_value = fake_tarea

    result = service.create_task(mock_session, 1, "Test", "desc")

    service.repo.create.assert_called_once()
    assert result == fake_tarea


def test_create_task_error():
    mock_session = MagicMock()
    service = TareaService()
    service.repo = MagicMock()
    service.repo.create.side_effect = SQLAlchemyError("Error")

    with pytest.raises(SQLAlchemyError):
        service.create_task(mock_session, 1, "Test", "desc")


# ------------------------
# get_task
# ------------------------
def test_get_task_success():
    mock_session = MagicMock()
    fake_tarea = Tarea(id=1, titulo="Test", usuario_id=1)

    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = fake_tarea

    result = service.get_task(mock_session, 1)

    assert result == fake_tarea
    service.repo.get_by_id.assert_called_once_with(mock_session, 1)


def test_get_task_not_found():
    mock_session = MagicMock()
    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = None

    result = service.get_task(mock_session, 999)
    assert result is None


# ------------------------
# list_user_tasks
# ------------------------
def test_list_user_tasks_success():
    mock_session = MagicMock()
    tareas = [Tarea(id=1, titulo="Test", usuario_id=1)]
    service = TareaService()
    service.repo = MagicMock()
    service.repo.list_by_user.return_value = tareas

    result = service.list_user_tasks(mock_session, 1)
    assert result == tareas


def test_list_user_tasks_error():
    mock_session = MagicMock()
    service = TareaService()
    service.repo = MagicMock()
    service.repo.list_by_user.side_effect = SQLAlchemyError("Error")

    with pytest.raises(SQLAlchemyError):
        service.list_user_tasks(mock_session, 1)


# ------------------------
# mark_as_completed
# ------------------------
def test_mark_as_completed_success():
    mock_session = MagicMock()
    tarea = Tarea(id=1, titulo="Test", usuario_id=1, completada=False)

    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = tarea
    service.repo.update.return_value = tarea

    result = service.mark_as_completed(mock_session, 1)

    assert result.completada is True
    service.repo.update.assert_called_once()


def test_mark_as_completed_not_found():
    mock_session = MagicMock()
    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = None

    result = service.mark_as_completed(mock_session, 999)
    assert result is None


def test_mark_as_completed_error():
    mock_session = MagicMock()
    tarea = Tarea(id=1, titulo="Test", usuario_id=1, completada=False)

    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = tarea
    service.repo.update.side_effect = SQLAlchemyError("Error")

    with pytest.raises(SQLAlchemyError):
        service.mark_as_completed(mock_session, 1)


# ------------------------
# update_task
# ------------------------
def test_update_task_success():
    mock_session = MagicMock()
    original_tarea = Tarea(id=1, titulo="Test", descripcion="desc", usuario_id=1)
    updated_tarea = Tarea(id=1, titulo="Nuevo", descripcion="nueva", usuario_id=1)

    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = original_tarea
    service.repo.update.return_value = updated_tarea

    result = service.update_task(mock_session, updated_tarea)

    assert result.titulo == "Nuevo"
    service.repo.update.assert_called_once()


def test_update_task_not_found():
    mock_session = MagicMock()
    updated_tarea = Tarea(id=1, titulo="Nuevo", descripcion="nueva", usuario_id=1)

    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = None

    result = service.update_task(mock_session, updated_tarea)
    assert result is None


def test_update_task_error():
    mock_session = MagicMock()
    original_tarea = Tarea(id=1, titulo="Test", descripcion="desc", usuario_id=1)
    updated_tarea = Tarea(id=1, titulo="Nuevo", descripcion="nueva", usuario_id=1)

    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = original_tarea
    service.repo.update.side_effect = SQLAlchemyError("Error")

    with pytest.raises(SQLAlchemyError):
        service.update_task(mock_session, updated_tarea)


# ------------------------
# delete_task
# ------------------------
def test_delete_task_success():
    mock_session = MagicMock()
    tarea = Tarea(id=1, titulo="Test", usuario_id=1)

    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = tarea

    result = service.delete_task(mock_session, 1)

    assert result is True
    service.repo.delete.assert_called_once()


def test_delete_task_not_found():
    mock_session = MagicMock()
    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = None

    result = service.delete_task(mock_session, 999)
    assert result is False


def test_delete_task_error():
    mock_session = MagicMock()
    tarea = Tarea(id=1, titulo="Test", usuario_id=1)

    service = TareaService()
    service.repo = MagicMock()
    service.repo.get_by_id.return_value = tarea
    service.repo.delete.side_effect = SQLAlchemyError("Error")

    with pytest.raises(SQLAlchemyError):
        service.delete_task(mock_session, 1)
