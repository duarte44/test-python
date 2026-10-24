from werkzeug.security import check_password_hash
from config.database import DatabaseConfig
from utils.jwt_handler import generate_token

class AuthService:
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.db = self.db_config.get_db()
        self.users_col = self.db["users"]
    
    def login_user(self, email, password):
        """Autentica um usuário e retorna seus dados com token"""
        user = self.users_col.find_one({"email": email})
        if not user or not check_password_hash(user["password"], password):
            return None
        token = generate_token(user["email"], user["role"])
        # Retorna token e os dados do usuário para a sessão
        return {
            "email": user["email"],
            "name": user.get("name", ""),
            "address": user.get("address", ""),
            "role": user.get("role", "cliente"),
            "token": token
        }
    
    def verify_user_exists(self, email):
        """Verifica se um usuário existe"""
        return self.users_col.find_one({"email": email}) is not None
