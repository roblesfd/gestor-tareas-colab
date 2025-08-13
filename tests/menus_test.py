import pytest
from unittest.mock import patch, MagicMock

from examples.misc import saludar
from utils.exceptions import UserNotFoundError
from menus import Menu, NonEmptyValidator
from config import init_config
from modelos.usuario import Usuario


repo = None 
db_session = None
menu = None

@pytest.fixture 
def setup_env():
    repo, db_session = init_config()
    menu = Menu(repo, db_session)

    return menu


def test_non_empty_validator():
    validator = NonEmptyValidator()
    # No debe lanzar excepcion si el texto no esta vacio
    validator.validate(MagicMock(text="hola"))

def test_non_empty_validator_fails():
    validator = NonEmptyValidator()
    with pytest.raises(Exception):
        validator.validate(MagicMock(text="   "))

# Test main_menu opción salir
@patch("menus.prompt", side_effect=["salir"])
@patch("menus.Menu.task_menu")
@patch("menus.Menu.user_menu")
def test_main_menu_exit(mock_user_menu, mock_task_menu, mock_prompt, setup_env):
    menu = setup_env
    menu.main_menu()

    mock_task_menu.assert_not_called()
    mock_user_menu.assert_not_called()

    assert True

# Test login_menu con contraseña correcta
@patch("menus.prompt", side_effect=["usuario1", "clave123"])
@patch("menus.print_formatted_text")
def test_login_menu_success(mock_print, mock_prompt, setup_env):
    menu = setup_env

    fake_user = MagicMock()
    fake_user.verify_password.return_value = True

    menu._repo = MagicMock()
    menu._repo.get_by_username.return_value = fake_user

    menu.login_menu()
    menu._repo.get_by_username.assert_called_once_with(menu._db_session, "usuario1")


# Test login_menu con usuario no encontrado
@patch("menus.prompt", side_effect=["usuario_invalido", "clave_invalida"])
@patch("menus.print_formatted_text")
def test_login_menu_invalid_credentials(mock_print, mock_prompt, setup_env):
    menu = setup_env

    fake_user = MagicMock()
    fake_user.verify_password.return_value = False

    menu._repo = MagicMock()
    menu._repo.get_by_username.return_value = fake_user

    menu.login_menu(max_attempts=1)

    error_msg = "Nombre de usuario y/o contraseña incorrectos"
    error_calls = [call for call in mock_print.call_args_list if error_msg in str(call)]
    assert len(error_calls) == 1

# Test signup_menu con registro exitoso y retorna usuario
@patch("menus.prompt", side_effect=["mock_user", "mock@example.com", "mockpass"])
@patch("menus.print_formatted_text")
def test_signup_menu_successful(mock_print, mock_prompt, setup_env):

    menu = setup_env

    fake_user = Usuario(nombre="mock_user", email="mock@example.com", password="mockpass")    
    
    repo = MagicMock()
    repo.create.return_value = fake_user

    menu._repo = repo
    result = menu.signup_menu()

    assert result.nombre == fake_user.nombre 
    assert result.email == fake_user.email

# Test que verifica si se llamo task_menu si la opcion ingresada es "tareas"
@patch("menus.Menu.task_menu", autospec=True)
@patch("menus.Menu._Menu__display_prompt", side_effect=["tareas", "salir"])
def test_main_menu_calls_task_menu(mock_display_prompt, mock_task_menu, setup_env):
    menu = setup_env
    menu.main_menu()

    mock_task_menu.assert_called_once()

# Test que verifica si se llamo user_menu si la opcion ingresada es "usuarios"
@patch("menus.Menu.user_menu")
@patch("menus.Menu._Menu__display_prompt", side_effect=["usuarios", "salir"])
def test_main_menu_calls_user_menu(mock_prompt, mock_user_menu, setup_env):
    menu = setup_env 
    menu.main_menu()
    mock_user_menu.assert_called_once()

# Test que verifica si se llamo login_menu y se ùdo autenticar el usuario
@patch("menus.Menu.login_menu")
@patch("menus.Menu._Menu__display_prompt", side_effect=["ingresar", "salir"])
def test_init_menu_calls_login_menu(mock_prompt, mock_login_menu, setup_env):

    menu = setup_env 

    menu.init_menu()
    mock_login_menu.assert_called_once()


# # Test que verifica si se llamo signup_menu si la opcion ingresada es "registrar"
@patch("menus.Menu.signup_menu")
@patch("menus.Menu._Menu__display_prompt", side_effect=["registrar", "salir"])
def test_init_menu_calls_signup_menu(mock_prompt, mock_signup_menu, setup_env):
    menu = setup_env 
    menu.init_menu()
    mock_signup_menu.assert_called_once()



