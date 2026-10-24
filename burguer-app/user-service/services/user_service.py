from config.database import DatabaseConfig
from werkzeug.security import generate_password_hash
from models.user_model import UserModel

class UserService:
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.db = self.db_config.get_db()
        self.users_col = self.db["users"]
        self.user_model = UserModel()
    
    def create_user(self, email, password, name, address, role="cliente"):
        """Cria um novo usuário"""
        # Verifica se email já existe
        if self.users_col.find_one({"email": email}):
            return {"error": "Usuário já existe"}, 400

        # Cria instância do modelo
        user = UserModel(email=email, name=name, address=address, role=role)
        
        # Valida os dados
        is_valid, message = user.validate()
        if not is_valid:
            return {"error": message}, 400

        # Hash da senha
        hashed_pw = generate_password_hash(password)
        user.password = hashed_pw
        
        # Salva no banco
        user_data = user.to_dict(include_password=True)
        self.users_col.insert_one(user_data)
        
        return {"message": "Usuário criado com sucesso"}, 201
    
    def get_user_by_email(self, email):
        """Busca um usuário pelo email"""
        user_data = self.users_col.find_one({"email": email})
        if user_data:
            user = UserModel.from_dict(user_data)
            return user.serialize(user_data)
        return None
    
    def update_user(self, email, name, address):
        """Atualiza os dados de um usuário"""
        user = UserModel(email=email, name=name, address=address)
        
        # Valida os dados básicos
        if not name or not address:
            return {"error": "Nome e endereço são obrigatórios"}, 400
        
        # Atualiza no banco
        result = self.users_col.update_one(
            {"email": email},
            {"$set": {"name": name, "address": address}}
        )
        
        if result.matched_count == 0:
            return {"error": "Usuário não encontrado"}, 404
        
        return {"message": "Usuário atualizado com sucesso"}, 200
    
    def delete_user(self, email):
        """Remove um usuário"""
        result = self.users_col.delete_one({"email": email})
        
        if result.deleted_count == 0:
            return {"error": "Usuário não encontrado"}, 404
        
        return {"message": "Usuário removido com sucesso"}, 200
    
    def get_all_users(self):
        """Retorna todos os usuários"""
        users = self.users_col.find({}, {"password": 0})  # Exclui senhas
        return [self.user_model.serialize(user) for user in users]

# Funções para compatibilidade com código antigo
def create_user(email, password, name, address, role="cliente"):
    service = UserService()
    return service.create_user(email, password, name, address, role)

def get_user_by_email(email):
    service = UserService()
    return service.get_user_by_email(email)

def update_user(email, name, address):
    service = UserService()
    return service.update_user(email, name, address)

def delete_user(email):
    service = UserService()
    return service.delete_user(email)
