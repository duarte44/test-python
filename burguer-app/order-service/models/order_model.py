from datetime import datetime

class OrderModel:
    def __init__(self, user_email=None, user_id=None, items=None, total=0.0, status="pending"):
        self.user_email = user_email
        self.user_id = user_id
        self.items = items or []
        self.total = total
        self.status = status
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def serialize(self, order_data=None):
        """Serializa dados do pedido para retorno"""
        # Helper function to format datetime
        def format_datetime(dt):
            if dt and hasattr(dt, 'strftime'):
                return dt.strftime('%d/%m/%Y %H:%M')
            return None
        
        if order_data:
            return {
                "id": str(order_data["_id"]),
                "user_email": order_data.get("user_email"),
                "user_id": order_data.get("user_id"),
                "items": order_data.get("items", []),
                "total": order_data.get("total", 0.0),
                "status": order_data.get("status", "pending"),
                "created_at": order_data.get("created_at"),
                "updated_at": order_data.get("updated_at"),
                "created_at_formatted": format_datetime(order_data.get("created_at")),
                "updated_at_formatted": format_datetime(order_data.get("updated_at"))
            }
        
        return {
            "user_email": self.user_email,
            "user_id": self.user_id,
            "items": self.items,
            "total": self.total,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            "user_email": self.user_email,
            "user_id": self.user_id,
            "items": self.items,
            "total": self.total,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @staticmethod
    def from_dict(data):
        """Cria uma instância do modelo a partir de um dicionário"""
        order = OrderModel(
            user_email=data.get("user_email"),
            user_id=data.get("user_id"),
            items=data.get("items", []),
            total=data.get("total", 0.0),
            status=data.get("status", "pending")
        )
        order.created_at = data.get("created_at", datetime.utcnow())
        order.updated_at = data.get("updated_at", datetime.utcnow())
        return order
    
    def validate(self):
        """Valida os dados do pedido"""
        if not self.user_email:
            return False, "Email do usuário é obrigatório"
        if not self.items:
            return False, "Itens do pedido são obrigatórios"
        if self.total <= 0:
            return False, "Total deve ser maior que zero"
        return True, "Dados válidos"
    
    def update_status(self, new_status):
        """Atualiza o status do pedido"""
        valid_statuses = ["pending", "preparing", "ready", "completed", "cancelled"]
        if new_status not in valid_statuses:
            return False, f"Status inválido. Use: {', '.join(valid_statuses)}"
        
        self.status = new_status
        self.updated_at = datetime.utcnow()
        return True, "Status atualizado"

# Serialização para retorno de pedidos (removendo dados sensíveis) - compatibilidade
def serialize_order(order):
    order_model = OrderModel()
    return order_model.serialize(order)
