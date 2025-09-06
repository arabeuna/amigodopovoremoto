# Estrutura Simplificada do Sistema Academia Amigo do Povo

## 📁 Organização dos Arquivos

### Arquivos Principais
- `app.py` - Aplicação Flask principal
- `models.py` - Modelos de dados e DAOs
- `database_local.py` - Configuração do banco SQLite local
- `database_integration_robusto.py` - Integração com MongoDB
- `requirements.txt` - Dependências Python

### 📂 config/
Arquivos de configuração do sistema:
- `config_database.py` - Configurações de banco de dados
- `__init__.py` - Inicialização do pacote

### 📂 data/
Arquivos de dados do sistema:
- `atividades_sistema.json` - Dados das atividades
- `dados_alunos.json` - Dados dos alunos
- `turmas_sistema.json` - Dados das turmas

### 📂 docs/
Documentação do sistema:
- `CHECKLIST_VARIAVEIS_RENDER.md` - Checklist para deploy
- `CORRECAO_PRODUCAO_MONGODB.md` - Correções de produção
- `ESTRUTURA_SIMPLIFICADA.md` - Este arquivo

### 📂 static/
Arquivos estáticos (CSS, JS, imagens):
- `js/` - Scripts JavaScript
- `images/` - Imagens e ícones
- `fotos/` - Fotos dos alunos
- `manifest.json` - Configuração PWA

### 📂 templates/
Templates HTML do Flask:
- `base.html` - Template base
- `login.html` - Página de login
- `dashboard.html` - Dashboard principal
- `alunos.html` - Gerenciamento de alunos
- `gerenciar_atividades.html` - Gerenciamento de atividades
- `presenca.html` - Controle de presença
- E outros templates específicos...

### 📂 uploads/
Arquivos enviados pelos usuários (planilhas, etc.)

### 📂 utils/
Utilitários e ferramentas:
- `build_executable.py` - Script para criar executável
- `__init__.py` - Inicialização do pacote

### 📂 dist/
Executável e arquivos de distribuição:
- `AcademiaAmigoDoPovo.exe` - Executável principal
- `README_EXECUTAVEL.md` - Instruções do executável
- `GUIA_INSTALACAO.md` - Guia de instalação

## 🚀 Como Usar

### Desenvolvimento
1. Instalar dependências: `pip install -r requirements.txt`
2. Executar aplicação: `python app.py`
3. Acessar: `http://localhost:5000`

### Produção (Executável)
1. Navegar para pasta `dist/`
2. Executar `AcademiaAmigoDoPovo.exe`
3. Acessar: `http://localhost:5000`

## 🔧 Configurações

### Banco de Dados
- **Local**: SQLite (arquivo `academia.db`)
- **Online**: MongoDB Atlas (configurado via variáveis de ambiente)

### Variáveis de Ambiente
- Arquivo `.env.production` para configurações de produção
- Configurações automáticas para ambiente local

## 📋 Funcionalidades Principais

1. **Gestão de Alunos**: Cadastro, edição, busca
2. **Controle de Atividades**: Criação e gerenciamento
3. **Presença**: Registro e relatórios
4. **Turmas**: Organização por horários
5. **Relatórios**: Impressão e exportação
6. **Upload de Planilhas**: Importação em lote

## 🛠️ Tecnologias

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Banco Local**: SQLite
- **Banco Online**: MongoDB
- **Deploy**: Render.com
- **Executável**: PyInstaller