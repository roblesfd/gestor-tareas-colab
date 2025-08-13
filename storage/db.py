import sqlite3 
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from modelos.usuario import Base, Usuario

connection = sqlite3.connect("example.db")

cursor = connection.cursor()

def init_db(db_url:str = "sqlite:///./storage/task-manager.db")->Session:
    engine = create_engine(db_url, echo=True, future=True)  
    create_tables(engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    return SessionLocal()

def create_tables(engine)->None:
    
    inspector = inspect(engine)
    tablas = inspector.get_table_names()

    if Usuario.__tablename__ not in tablas:
        Base.metadata.create_all(engine)

    
