import bcrypt
from src.backend.database import Database
from src.backend.user import User

class Login:

    def __init__(self, session_state):
        self.db = Database()
        self.session_state = session_state

    def login(self, email, password):
        user = self.db.get_user_by_email(email)
        if user and self.check_password(password, user.pwd):
            self.session_state.usuario = email
            self.session_state.pagina = "login" 
            self.session_state.user = user
            return user
        return False
    
    def create_user(self, email, password, name, role, company_name, cpf_user):
        id_company, _ = self.db.get_company(company_name)
        last_id = self.db.get_last_id("users")
        id_user = last_id + 1
        cpf_user = cpf_user.replace(".", "").replace("-", "")

        if not cpf_user.isdigit() or len(cpf_user) != 11:
            raise ValueError("CPF inválido")
        
        user = User(
            id_user=id_user,
            name=name,
            user_type=role,
            id_company=id_company,
            cpf_user=cpf_user,
            email=email,
            pwd=self.hash_password(password)
        )

        return user

    def insert_user(self, user):
        if not self.db.search_user(user):
            self.db.insert_user(user)
            self.session_state.usuario = user.name
            self.session_state.pagina = user.user_type
            self.session_state.user = user
            return True
        return False

    def get_user(self, email, password):
        return self.db.get_user(email, password)

    def get_companies(self):
        return self.db.get_companies()

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))        

