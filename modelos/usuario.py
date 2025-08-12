from sqlalchemy import create_engine, Column, Integer, String 
from sqlalchemy.orm import declarative_base 
import bcrypt

Base = declarative_base()
engine = create_engine("sqlite:///./storage/example.db")  


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String(55), nullable=False)

    def set_password(self, plain_pwd: str):
        hashed = bcrypt.hashpw(plain_pwd.encode('utf-8'), bcrypt.gensalt())
        self.password = hashed.decode('utf-8')

    def verify_password(self, plain_pwd:str) -> bool:
        return bcrypt.checkpw(plain_pwd.encode('utf-8'). self.password.encode('utf-8'))

# Base.metadata.create_all(engine)
