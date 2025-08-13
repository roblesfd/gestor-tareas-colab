from models.usuario import Usuario

class UsuarioService:

    def __init__(self, repo, db_session):
        self.repo = repo 
        self.db_session = db_session 

    def authenticate(self, username:str, password:str):
        user = self.repo.get_by_username(self.db_session, username)
        
        if user and user.verify_password(password):
            return user
        else:
            return None

    def signup(self, nombre:str, email:str, password:str):
        new_user = Usuario()
        new_user.nombre = nombre
        new_user.email = email 
        new_user.password = password

        saved_user = self.repo.create(self.db_session, new_user)

        if saved_user:
            return saved_user
        else:
            return None
