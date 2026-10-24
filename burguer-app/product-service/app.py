from flask import Flask
from controllers.product_controller import product_bp
from dotenv import load_dotenv
import os

class ProductApp:
    def __init__(self):
        # Carrega as variáveis de ambiente
        load_dotenv()
        
        # Cria a instância da aplicação Flask
        self.app = Flask(__name__)
        self.app.secret_key = os.getenv("SECRET_KEY")
        
        # Configura as rotas
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura as rotas da aplicação"""
        # Registra o blueprint de produtos
        self.app.register_blueprint(product_bp, url_prefix='/product')
        
        # Rota raiz
        @self.app.route('/')
        def index():
            return '<a href="/product/list">Ver produtos disponíveis</a>'
    
    def run(self, host='127.0.0.1', port=5003, debug=True):
        """Executa a aplicação Flask"""
        self.app.run(host=host, port=port, debug=debug)
    
    def get_app(self):
        """Retorna a instância da aplicação Flask"""
        return self.app

# Criação da instância da aplicação
product_app = ProductApp()
app = product_app.get_app()  # Para compatibilidade

if __name__ == '__main__':
    product_app.run(port=5003, debug=True)
