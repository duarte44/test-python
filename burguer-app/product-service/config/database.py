# Conecta ao  banco de dados MongoDB utilizando as variáveis de ambiente

from pymongo import MongoClient
import os
from dotenv import load_dotenv

class DatabaseConfig:
    def __init__(self):
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()
        
        # Cria a conexão com o banco de dados MongoDB
        self.client = MongoClient(os.getenv("MONGO_URI"))
        
        # Seleciona o banco de dados
        self.db = self.client["burguer_app_db"]
    
    def get_db(self):
        """Retorna a instância do banco de dados"""
        return self.db
    
    def get_client(self):
        """Retorna o cliente MongoDB"""
        return self.client
    
    def close_connection(self):
        """Fecha a conexão com o banco de dados"""
        self.client.close()

# Função para retornar a instância do banco de dados (compatibilidade com código antigo)
def get_db():
    db_config = DatabaseConfig()
    return db_config.get_db()
