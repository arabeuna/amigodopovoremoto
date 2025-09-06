import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

class LocalDatabase:
    def __init__(self, db_path="academia_local.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados SQLite com as tabelas necessárias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de alunos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                data_nascimento TEXT,
                telefone TEXT,
                endereco TEXT,
                cpf TEXT UNIQUE,
                rg TEXT,
                titulo_eleitor TEXT,
                titulo_secao TEXT,
                titulo_zona TEXT,
                titulo_municipio TEXT,
                email TEXT,
                contato_emergencia TEXT,
                observacoes TEXT,
                ativo INTEGER DEFAULT 1,
                data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP,
                atividades TEXT DEFAULT '[]',
                frequencia TEXT DEFAULT '{}'
            )
        ''')
        
        # Tabela de atividades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                instrutor TEXT,
                horario TEXT,
                dias_semana TEXT,
                capacidade_maxima INTEGER,
                ativa INTEGER DEFAULT 1,
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de turmas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS turmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                atividade_id INTEGER,
                instrutor TEXT,
                horario TEXT,
                dias_semana TEXT,
                capacidade_maxima INTEGER,
                alunos_inscritos TEXT DEFAULT '[]',
                ativa INTEGER DEFAULT 1,
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (atividade_id) REFERENCES atividades (id)
            )
        ''')
        
        # Tabela de usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nome TEXT,
                email TEXT,
                tipo TEXT DEFAULT 'usuario',
                ativo INTEGER DEFAULT 1,
                data_criacao TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabela de presença
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presenca (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                aluno_id INTEGER,
                atividade_id INTEGER,
                data_presenca TEXT,
                presente INTEGER DEFAULT 0,
                observacoes TEXT,
                FOREIGN KEY (aluno_id) REFERENCES alunos (id),
                FOREIGN KEY (atividade_id) REFERENCES atividades (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Banco de dados SQLite inicializado com sucesso")
    
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
        return conn
    
    # Métodos para Alunos
    def inserir_aluno(self, aluno_data: Dict) -> int:
        """Insere um novo aluno no banco de dados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alunos (
                nome, data_nascimento, telefone, endereco, cpf, rg,
                titulo_eleitor, titulo_secao, titulo_zona, titulo_municipio,
                email, contato_emergencia, observacoes, atividades, frequencia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            aluno_data.get('nome'),
            aluno_data.get('data_nascimento'),
            aluno_data.get('telefone'),
            aluno_data.get('endereco'),
            aluno_data.get('cpf'),
            aluno_data.get('rg'),
            aluno_data.get('titulo_eleitor'),
            aluno_data.get('titulo_secao'),
            aluno_data.get('titulo_zona'),
            aluno_data.get('titulo_municipio'),
            aluno_data.get('email'),
            aluno_data.get('contato_emergencia'),
            aluno_data.get('observacoes'),
            json.dumps(aluno_data.get('atividades', [])),
            json.dumps(aluno_data.get('frequencia', {}))
        ))
        
        aluno_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return aluno_id
    
    def listar_alunos(self) -> List[Dict]:
        """Lista todos os alunos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM alunos WHERE ativo = 1')
        rows = cursor.fetchall()
        
        alunos = []
        for row in rows:
            aluno = dict(row)
            aluno['atividades'] = json.loads(aluno['atividades'] or '[]')
            aluno['frequencia'] = json.loads(aluno['frequencia'] or '{}')
            alunos.append(aluno)
        
        conn.close()
        return alunos
    
    def buscar_aluno_por_id(self, aluno_id: int) -> Optional[Dict]:
        """Busca um aluno por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM alunos WHERE id = ? AND ativo = 1', (aluno_id,))
        row = cursor.fetchone()
        
        if row:
            aluno = dict(row)
            aluno['atividades'] = json.loads(aluno['atividades'] or '[]')
            aluno['frequencia'] = json.loads(aluno['frequencia'] or '{}')
            conn.close()
            return aluno
        
        conn.close()
        return None
    
    def atualizar_aluno(self, aluno_id: int, aluno_data: Dict) -> bool:
        """Atualiza os dados de um aluno"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE alunos SET
                nome = ?, data_nascimento = ?, telefone = ?, endereco = ?,
                cpf = ?, rg = ?, titulo_eleitor = ?, titulo_secao = ?,
                titulo_zona = ?, titulo_municipio = ?, email = ?,
                contato_emergencia = ?, observacoes = ?, atividades = ?, frequencia = ?
            WHERE id = ?
        ''', (
            aluno_data.get('nome'),
            aluno_data.get('data_nascimento'),
            aluno_data.get('telefone'),
            aluno_data.get('endereco'),
            aluno_data.get('cpf'),
            aluno_data.get('rg'),
            aluno_data.get('titulo_eleitor'),
            aluno_data.get('titulo_secao'),
            aluno_data.get('titulo_zona'),
            aluno_data.get('titulo_municipio'),
            aluno_data.get('email'),
            aluno_data.get('contato_emergencia'),
            aluno_data.get('observacoes'),
            json.dumps(aluno_data.get('atividades', [])),
            json.dumps(aluno_data.get('frequencia', {})),
            aluno_id
        ))
        
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # Métodos para Atividades
    def inserir_atividade(self, atividade_data: Dict) -> int:
        """Insere uma nova atividade"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO atividades (
                nome, descricao, instrutor, horario, dias_semana, capacidade_maxima
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            atividade_data.get('nome'),
            atividade_data.get('descricao'),
            atividade_data.get('instrutor'),
            atividade_data.get('horario'),
            atividade_data.get('dias_semana'),
            atividade_data.get('capacidade_maxima')
        ))
        
        atividade_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return atividade_id
    
    def listar_atividades(self) -> List[Dict]:
        """Lista todas as atividades ativas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM atividades WHERE ativa = 1')
        rows = cursor.fetchall()
        
        atividades = [dict(row) for row in rows]
        conn.close()
        return atividades
    
    # Métodos para Usuários
    def inserir_usuario(self, usuario_data: Dict) -> int:
        """Insere um novo usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO usuarios (username, password, nome, email, tipo)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            usuario_data.get('username'),
            usuario_data.get('password'),
            usuario_data.get('nome'),
            usuario_data.get('email'),
            usuario_data.get('tipo', 'usuario')
        ))
        
        usuario_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return usuario_id
    
    def buscar_usuario_por_username(self, username: str) -> Optional[Dict]:
        """Busca um usuário por username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM usuarios WHERE username = ? AND ativo = 1', (username,))
        row = cursor.fetchone()
        
        if row:
            usuario = dict(row)
            conn.close()
            return usuario
        
        conn.close()
        return None
    
    def contar_alunos(self) -> int:
        """Conta o total de alunos ativos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM alunos WHERE ativo = 1')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    
    def contar_atividades(self) -> int:
        """Conta o total de atividades ativas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM atividades WHERE ativa = 1')
        count = cursor.fetchone()[0]
        
        conn.close()
        return count

# Instância global do banco de dados
local_db = LocalDatabase()