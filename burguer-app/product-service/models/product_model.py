class ProductModel:
    def __init__(self, name=None, description=None, category=None, price=None, available=True, ingredients=None):
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.available = available
        self.ingredients = ingredients or []
    
    def serialize(self, product_data=None):
        """Serializa dados do produto para retorno"""
        if product_data:
            return {
                "id": str(product_data.get("_id")),
                "name": product_data.get("name"),
                "description": product_data.get("description"),
                "category": product_data.get("category"),
                "price": product_data.get("price"),
                "available": product_data.get("available", True),
                "ingredients": product_data.get("ingredients", [])
            }
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "available": self.available,
            "ingredients": self.ingredients
        }
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "available": self.available,
            "ingredients": self.ingredients
        }
    
    @staticmethod
    def from_dict(data):
        """Cria uma instância do modelo a partir de um dicionário"""
        return ProductModel(
            name=data.get("name"),
            description=data.get("description"),
            category=data.get("category"),
            price=data.get("price"),
            available=data.get("available", True),
            ingredients=data.get("ingredients", [])
        )
    
    def validate(self):
        """Valida os dados do produto"""
        if not self.name:
            return False, "Nome do produto é obrigatório"
        if not self.description:
            return False, "Descrição é obrigatória"
        if not self.category:
            return False, "Categoria é obrigatória"
        if self.price is None or self.price <= 0:
            return False, "Preço deve ser maior que zero"
        if not self.ingredients:
            return False, "Ingredientes são obrigatórios"
        return True, "Dados válidos"

# Função para compatibilidade com código antigo
def serialize_product(product):
    product_model = ProductModel()
    return product_model.serialize(product)
