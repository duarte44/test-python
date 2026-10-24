from flask import Flask
from controllers.user_controller import user_bp
from dotenv import load_dotenv
import os

class UserApp:
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
        # Registra o blueprint de usuários
        self.app.register_blueprint(user_bp, url_prefix='/user')
        
        # Rota raiz
        @self.app.route('/')
        def index():
            return '<a href="/user/create">Cadastrar novo usuário</a>'
    
    def run(self, host='127.0.0.1', port=5001, debug=True):
        """Executa a aplicação Flask"""
        self.app.run(host=host, port=port, debug=debug)
    
    def get_app(self):
        """Retorna a instância da aplicação Flask"""
        return self.app

# Criação da instância da aplicação
user_app = UserApp()
app = user_app.get_app()  # Para compatibilidade

if __name__ == '__main__':
    user_app.run(port=5001, debug=True)
