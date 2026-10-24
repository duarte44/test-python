class UserModel:
    def __init__(self, email=None, name=None, address=None, role="cliente", password=None):
        self.email = email
        self.name = name
        self.address = address
        self.role = role
        self.password = password
    
    def serialize(self, user_data=None):
        """Serializa dados do usuário para retorno (removendo dados sensíveis)"""
        if user_data:
            return {
                "email": user_data.get("email"),
                "name": user_data.get("name"),
                "address": user_data.get("address"),
                "role": user_data.get("role", "cliente")
            }
        return {
            "email": self.email,
            "name": self.name,
            "address": self.address,
            "role": self.role
        }
    
    def to_dict(self, include_password=False):
        """Converte o modelo para dicionário"""
        data = {
            "email": self.email,
            "name": self.name,
            "address": self.address,
            "role": self.role
        }
        if include_password and self.password:
            data["password"] = self.password
        return data
    
    @staticmethod
    def from_dict(data):
        """Cria uma instância do modelo a partir de um dicionário"""
        return UserModel(
            email=data.get("email"),
            name=data.get("name"),
            address=data.get("address"),
            role=data.get("role", "cliente"),
            password=data.get("password")
        )
    
    def validate(self):
        """Valida os dados do usuário"""
        if not self.email:
            return False, "Email é obrigatório"
        if not self.name:
            return False, "Nome é obrigatório"
        if not self.address:
            return False, "Endereço é obrigatório"
        return True, "Dados válidos"

# Função para compatibilidade com código antigo
def serialize_user(user):
    user_model = UserModel()
    return user_model.serialize(user)
