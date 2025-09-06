import os
import sys
from typing import Dict, Any

class DatabaseConfig:
    """Configuração para alternar entre MongoDB (online) e SQLite (local)"""
    
    def __init__(self):
        # Verifica se deve usar banco local (para executável)
        self.use_local_db = os.getenv('USE_LOCAL_DB', 'false').lower() == 'true'
        
        # Se estiver rodando como executável, força uso do banco local
        if getattr(sys, 'frozen', False):
            self.use_local_db = True
    
    def get_database_type(self) -> str:
        """Retorna o tipo de banco de dados a ser usado"""
        return 'sqlite' if self.use_local_db else 'mongodb'
    
    def is_local_database(self) -> bool:
        """Verifica se está usando banco de dados local"""
        return self.use_local_db
    
    def get_mongodb_config(self) -> Dict[str, Any]:
        """Retorna configuração do MongoDB"""
        return {
            'uri': os.getenv('MONGODB_URI', ''),
            'database': os.getenv('MONGODB_DATABASE', 'amigodopovoassociacao_db')
        }
    
    def get_sqlite_config(self) -> Dict[str, Any]:
        """Retorna configuração do SQLite"""
        return {
            'db_path': 'academia_local.db'
        }

# Instância global da configuração
db_config = DatabaseConfig()

# Função para verificar se é executável
import sys
def is_executable():
    """Verifica se o código está rodando como executável"""
    return getattr(sys, 'frozen', False)