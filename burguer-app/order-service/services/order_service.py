from config.database import DatabaseConfig
from models.order_model import OrderModel
from datetime import datetime
from bson import ObjectId

class OrderService:
    def __init__(self):
        self.db_config = DatabaseConfig()
        self.db = self.db_config.get_db()
        self.orders_col = self.db["orders"]
        self.users_col = self.db["users"]
        self.order_model = OrderModel()
    
    def create_order(self, user_email, items, total):
        """Cria um novo pedido no banco de dados"""
        # Validate that user exists
        user = self.users_col.find_one({"email": user_email})
        if not user:
            return {"error": f"Usuário com email '{user_email}' não encontrado. Verifique se o email está correto."}, 404
        
        # Cria instância do modelo
        order = OrderModel(
            user_email=user_email,
            user_id=str(user["_id"]),
            items=items,
            total=total,
            status="pending"
        )
        
        # Valida os dados
        is_valid, message = order.validate()
        if not is_valid:
            return {"error": message}, 400
        
        # Salva no banco
        order_data = order.to_dict()
        result = self.orders_col.insert_one(order_data)
        return {"message": "Pedido criado com sucesso", "order_id": str(result.inserted_id)}, 201
    
    def get_order_by_id(self, order_id):
        """Busca um pedido pelo ID"""
        try:
            order = self.orders_col.find_one({"_id": ObjectId(order_id)})
            if order:
                return self.order_model.serialize(order)
            return None
        except:
            return None
    
    def get_orders_by_user(self, user_email):
        """Busca todos os pedidos de um usuário"""
        orders = self.orders_col.find({"user_email": user_email}).sort("created_at", -1)
        return [self.order_model.serialize(order) for order in orders]
    
    def get_all_orders(self):
        """Busca todos os pedidos"""
        orders = self.orders_col.find().sort("created_at", -1)
        return [self.order_model.serialize(order) for order in orders]
    
    def update_order_status(self, order_id, status):
        """Atualiza o status de um pedido"""
        try:
            # Valida o status
            order = OrderModel()
            is_valid, message = order.update_status(status)
            if not is_valid:
                return {"error": message}, 400
            
            # Atualiza no banco
            result = self.orders_col.update_one(
                {"_id": ObjectId(order_id)},
                {
                    "$set": {
                        "status": status,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            
            if result.matched_count == 0:
                return {"error": "Pedido não encontrado"}, 404
            
            return {"message": "Status atualizado com sucesso"}, 200
        except Exception as e:
            return {"error": f"Erro ao atualizar status: {str(e)}"}, 500
    
    def delete_order(self, order_id):
        """Deleta um pedido"""
        try:
            result = self.orders_col.delete_one({"_id": ObjectId(order_id)})
            if result.deleted_count == 0:
                return {"error": "Pedido não encontrado"}, 404
            return {"message": "Pedido deletado com sucesso"}, 200
        except Exception as e:
            return {"error": f"Erro ao deletar pedido: {str(e)}"}, 500
    
    def get_all_users(self):
        """Busca todos os usuários cadastrados para referência"""
        try:
            users = list(self.users_col.find({}, {"password": 0}))  # Exclui senhas
            return [{"email": user.get("email"), "name": user.get("name", "")} for user in users]
        except Exception as e:
            print(f"Erro ao buscar usuários: {e}")
            return []

# Funções para compatibilidade com código antigo
def create_order(user_email, items, total):
    service = OrderService()
    return service.create_order(user_email, items, total)

def get_order_by_id(order_id):
    service = OrderService()
    return service.get_order_by_id(order_id)

def get_orders_by_user(user_email):
    service = OrderService()
    return service.get_orders_by_user(user_email)

def get_all_orders():
    service = OrderService()
    return service.get_all_orders()

def update_order_status(order_id, status):
    service = OrderService()
    return service.update_order_status(order_id, status)

def delete_order(order_id):
    service = OrderService()
    return service.delete_order(order_id)

def get_all_users():
    service = OrderService()
    return service.get_all_users()
