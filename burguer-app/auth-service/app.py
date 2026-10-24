from flask import Flask, session, redirect, url_for
from controllers.auth_controller import auth_bp
from dotenv import load_dotenv
import os

class AuthApp:
    def __init__(self):
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()
        
        # Cria a instância da aplicação Flask
        self.app = Flask(__name__)
        
        # Configura a chave secreta para a sessão
        secret_key = os.getenv("SECRET_KEY")
        print(f"SECRET_KEY carregada: {secret_key}")  # DEBUG: deve imprimir o valor correto
        self.app.secret_key = secret_key
        
        # Configura as rotas
        self._setup_routes()
    
    def _setup_routes(self):
        """Configura as rotas da aplicação"""
        # Registra o blueprint de autenticação
        self.app.register_blueprint(auth_bp, url_prefix='/auth')
        
        # Redireciona a rota raiz para a página de login
        @self.app.route('/')
        def index():
            return redirect(url_for('auth.login_page'))
    
    def run(self, host='127.0.0.1', port=5000, debug=True):
        """Executa a aplicação Flask"""
        self.app.run(host=host, port=port, debug=debug)
    
    def get_app(self):
        """Retorna a instância da aplicação Flask"""
        return self.app

# Criação da instância da aplicação
auth_app = AuthApp()
app = auth_app.get_app()  # Para compatibilidade

if __name__ == '__main__':
    # Executa a aplicação Flask
    auth_app.run(port=5000, debug=True)
    # O debug=True permite recarregar automaticamente a aplicação ao fazer alterações no código