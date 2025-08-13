from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import session

from models.usuario import Usuario
from utils.exceptions import UserNotFoundError, UserAlreadyExistsError


class UsuarioRepository():

    def create(self, db_session:session, user: Usuario) -> Usuario :
        try:
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            return user
        except IntegrityError as e:
            db_session.rollback()
            raise UserAlreadyExistsError("Ya existe una cuenta con ese correo") from e

    def get_by_username(self, db_session:session, username: str)->Usuario:
        usuario = db_session.query(Usuario).filter(Usuario.nombre == username).first()

        if usuario is None:
            raise UserNotFoundError("No existe un usuario con ese nombre")
        else:
            return usuario

    def get_by_email(self, db_session:session, email: str)->Usuario:
        usuario = db_session.query(Usuario).filter(Usuario.email == email).first()
        
        if usuario is None:
            raise UserNotFoundError("No existe un usuario con ese correo")
        else:
            return usuario
    
    def get_all(self, db_session:session)->[Usuario]:
        usuario_list = db_session.query(Usuario)

        if usuario_list is None:
            raise UserNotFoundError("No hay usuarios registrados")
        else:
            return usuario_list

    def update(self, db_session:session, usuario: Usuario)->Usuario:
        updated_usuario = self.get_by_email(db_session, usuario.email)

        if updated_usuario is None:
            raise UserNotFoundError("No existe el usuario")
        else:
            try: 
                updated_usuario.nombre = usuario.nombre 
                updated_usuario.email = usuario.email 
                updated_usuario.password = usuario.password
                db_session.commit()

                return updated_usuario
            except IntegrityError:
                db_session.rollback()
                raise
    
    def delete_by_id(self, db_session:session, usuario_id: int) -> bool:
        usuario = db_session.query(Usuario).filter(Usuario.id == usuario_id).first()

        if usuario is None:
            raise UserNotFoundError("No existe un usuario con ese ID")
        try:
            db_session.delete(usuario)
            db_session.commit()
            return True 
        except Except as e:
            db_session.rollback()
            return False

