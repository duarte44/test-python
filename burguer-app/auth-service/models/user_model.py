class UserModel:
    def __init__(self, email=None, name=None, address=None, role="cliente"):
        self.email = email
        self.name = name
        self.address = address
        self.role = role
    
    def serialize(self, user_data=None):
        """Serializa dados do usuário para retorno (removendo dados sensíveis)"""
        if user_data:
            return {
                "email": user_data.get("email"),
                "name": user_data.get("name", ""),
                "address": user_data.get("address", ""),
                "role": user_data.get("role", "cliente")
            }
        return {
            "email": self.email,
            "name": self.name,
            "address": self.address,
            "role": self.role
        }
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            "email": self.email,
            "name": self.name,
            "address": self.address,
            "role": self.role
        }
    
    @staticmethod
    def from_dict(data):
        """Cria uma instância do modelo a partir de um dicionário"""
        return UserModel(
            email=data.get("email"),
            name=data.get("name", ""),
            address=data.get("address", ""),
            role=data.get("role", "cliente")
        )

# Função para compatibilidade com código antigo
def serialize_user(user):
    user_model = UserModel()
    return user_model.serialize(user)
