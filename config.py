import os
from dotenv import load_dotenv
from repositories.usuario import UsuarioRepository
from storage.db import init_db

def init_config():
    load_dotenv()
    db_url = os.getenv("DB_URL")
    if not db_url:
        raise ValueError("La variable de entorno DB_URL no está definida en el archivo .env")
    
    repo = UsuarioRepository()
    db_session = init_db(db_url)
    return repo, db_session
