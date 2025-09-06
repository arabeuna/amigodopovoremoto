-- Banco de dados para Associação Amigo do Povo
-- Execute este script para criar as tabelas necessárias

CREATE DATABASE IF NOT EXISTS associacao_amigo_povo;
USE associacao_amigo_povo;

-- Tabela de usuários para login
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    status ENUM('ativo', 'inativo') DEFAULT 'ativo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de alunos
CREATE TABLE IF NOT EXISTS alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    endereco TEXT,
    responsavel VARCHAR(100),
    telefone_responsavel VARCHAR(20),
    observacoes TEXT,
    status ENUM('ativo', 'inativo') DEFAULT 'ativo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de atividades
CREATE TABLE IF NOT EXISTS atividades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50),
    idade_minima INT,
    idade_maxima INT,
    status ENUM('ativa', 'inativa') DEFAULT 'ativa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de turmas
CREATE TABLE IF NOT EXISTS turmas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    atividade_id INT,
    instrutor VARCHAR(100) NOT NULL,
    horario TIME NOT NULL,
    dia_semana VARCHAR(20) NOT NULL,
    vagas INT NOT NULL DEFAULT 20,
    status ENUM('ativa', 'inativa', 'lotada') DEFAULT 'ativa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (atividade_id) REFERENCES atividades(id) ON DELETE SET NULL
);

-- Tabela de matrículas
CREATE TABLE IF NOT EXISTS matriculas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT NOT NULL,
    turma_id INT NOT NULL,
    data_matricula DATE NOT NULL,
    status ENUM('ativa', 'inativa', 'cancelada', 'concluida') DEFAULT 'ativa',
    observacoes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id) ON DELETE CASCADE,
    FOREIGN KEY (turma_id) REFERENCES turmas(id) ON DELETE CASCADE,
    UNIQUE KEY unique_matricula (aluno_id, turma_id)
);

-- Inserir usuário padrão (admin/admin123)
INSERT INTO usuarios (usuario, senha, nome, email) VALUES 
('admin', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Administrador', 'admin@associacao.com')
ON DUPLICATE KEY UPDATE usuario = usuario;

-- Inserir algumas atividades de exemplo
INSERT INTO atividades (nome, descricao, categoria, idade_minima, idade_maxima) VALUES 
('Futebol Infantil', 'Aulas de futebol para crianças e adolescentes', 'Esporte', 6, 17),
('Dança Contemporânea', 'Aulas de dança contemporânea para todas as idades', 'Dança', 8, NULL),
('Artesanato', 'Oficinas de artesanato e trabalhos manuais', 'Artesanato', 10, NULL),
('Reforço Escolar', 'Aulas de reforço escolar em matemática e português', 'Educação', 6, 15),
('Violão', 'Aulas de violão para iniciantes', 'Música', 8, NULL)
ON DUPLICATE KEY UPDATE nome = nome;

-- Inserir algumas turmas de exemplo
INSERT INTO turmas (nome, atividade_id, instrutor, horario, dia_semana, vagas) VALUES 
('Futebol Manhã', 1, 'João Silva', '09:00:00', 'Sábado', 25),
('Dança Tarde', 2, 'Maria Santos', '14:00:00', 'Quarta-feira', 20),
('Artesanato Noite', 3, 'Ana Costa', '19:00:00', 'Terça-feira', 15),
('Reforço Matemática', 4, 'Pedro Oliveira', '15:00:00', 'Segunda-feira', 12),
('Violão Iniciante', 5, 'Carlos Mendes', '16:00:00', 'Quinta-feira', 10)
ON DUPLICATE KEY UPDATE nome = nome;

-- Inserir alguns alunos de exemplo
INSERT INTO alunos (nome, cpf, data_nascimento, telefone, responsavel, telefone_responsavel) VALUES 
('Lucas Silva Santos', '123.456.789-01', '2010-05-15', '(11) 98765-4321', 'Maria Silva Santos', '(11) 91234-5678'),
('Ana Beatriz Costa', '987.654.321-02', '2008-12-03', '(11) 87654-3210', 'José Costa', '(11) 98765-4321'),
('Gabriel Oliveira', '456.789.123-03', '2012-08-20', '(11) 76543-2109', 'Fernanda Oliveira', '(11) 87654-3210'),
('Sophia Mendes', '789.123.456-04', '2009-03-10', '(11) 65432-1098', 'Roberto Mendes', '(11) 76543-2109'),
('Miguel Santos', '321.654.987-05', '2011-11-25', '(11) 54321-0987', 'Carla Santos', '(11) 65432-1098')
ON DUPLICATE KEY UPDATE cpf = cpf;

-- Inserir algumas matrículas de exemplo
INSERT INTO matriculas (aluno_id, turma_id, data_matricula) VALUES 
(1, 1, '2024-01-15'),
(2, 2, '2024-01-20'),
(3, 1, '2024-01-18'),
(4, 3, '2024-02-01'),
(5, 4, '2024-02-05'),
(1, 4, '2024-02-10'),
(2, 5, '2024-02-15')
ON DUPLICATE KEY UPDATE data_matricula = data_matricula;

-- Criar índices para melhor performance
CREATE INDEX idx_alunos_cpf ON alunos(cpf);
CREATE INDEX idx_alunos_nome ON alunos(nome);
CREATE INDEX idx_matriculas_aluno ON matriculas(aluno_id);
CREATE INDEX idx_matriculas_turma ON matriculas(turma_id);
CREATE INDEX idx_matriculas_status ON matriculas(status);
CREATE INDEX idx_turmas_atividade ON turmas(atividade_id);
CREATE INDEX idx_turmas_status ON turmas(status);

-- Comentários sobre o uso:
-- 1. Execute este script no seu servidor MySQL/MariaDB
-- 2. Ajuste as configurações de conexão no arquivo config/database.php
-- 3. O usuário padrão é: admin / admin123
-- 4. As senhas são criptografadas com password_hash() do PHP