from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import session
from modelos.usuario import Usuario
from utils.exceptions import UserNotFoundError, UserAlreadyExistsError


class UsuarioRepository():

    def create(self, db:session, user: Usuario) -> Usuario :
        try:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError as e:
            db.rollback()
            raise UserAlreadyExistsError("Ya existe una cuenta con ese correo") from e

    def get_by_username(self, db:session, username: str)->Usuario:
        usuario = db.query(Usuario).filter(Usuario.nombre == username).first()

        if usuario is None:
            raise UserNotFoundError("No existe un usuario con ese nombre")
        else:
            return usuario

    def get_by_email(self, db:session, email: str)->Usuario:
        usuario = db.query(Usuario).filter(Usuario.email == email).first()
        
        if usuario is None:
            raise UserNotFoundError("No existe un usuario con ese correo")
        else:
            return usuario
    
    def get_all(self, db:session)->[Usuario]:
        usuario_list = db.query(Usuario)

        if usuario_list is None:
            raise UserNotFoundError("No hay usuarios registrados")
        else:
            return usuario_list

    def update(self, db:session, usuario: Usuario)->Usuario:
        updated_usuario = self.get_by_email(db, usuario.email)

        if updated_usuario is None:
            raise UserNotFoundError("No existe el usuario")
        else:
            try: 
                updated_usuario.nombre = usuario.nombre 
                updated_usuario.email = usuario.email 
                updated_usuario.password = usuario.password
                db.commit()

                return updated_usuario
            except IntegrityError:
                db.rollback()
                raise
    
    def delete_by_id(self, db:session, usuario_id: int) -> bool:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        if usuario is None:
            raise UserNotFoundError("No existe un usuario con ese ID")
        try:
            db.delete(usuario)
            db.commit()
            return True 
        except Except as e:
            db.rollback()
            return False

