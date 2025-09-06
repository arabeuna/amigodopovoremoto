# Sistema de Gestão - Associação Amigo do Povo

Sistema web para gestão de alunos, atividades, turmas e matrículas da Associação Amigo do Povo.

## 🚀 Características

- **Gestão de Alunos**: Cadastro, edição e controle de alunos
- **Gestão de Atividades**: Controle das atividades oferecidas
- **Gestão de Turmas**: Organização de turmas por atividade
- **Gestão de Matrículas**: Controle de inscrições dos alunos
- **Relatórios**: Relatórios detalhados com filtros
- **Interface Responsiva**: Design moderno com Tailwind CSS
- **Segurança**: Sistema de login com sessões seguras

## 📋 Pré-requisitos

- PHP 7.4 ou superior
- MySQL 5.7 ou superior (ou MariaDB)
- Servidor web (Apache, Nginx, etc.)
- Extensões PHP: PDO, PDO_MySQL

## 🔧 Instalação

### 1. Clone ou baixe o projeto
```bash
git clone [url-do-repositorio]
# ou extraia os arquivos para o diretório do servidor web
```

### 2. Configure o banco de dados

1. Crie um banco de dados MySQL:
```sql
CREATE DATABASE associacao_amigo_povo;
```

2. Execute o script SQL:
```bash
mysql -u seu_usuario -p associacao_amigo_povo < database.sql
```

### 3. Configure a conexão com o banco

Edite o arquivo `config/database.php` e ajuste as configurações:

```php
$host = 'localhost';        // Servidor do banco
$dbname = 'associacao_amigo_povo';  // Nome do banco
$username = 'seu_usuario';  // Usuário do banco
$password = 'sua_senha';    // Senha do banco
```

### 4. Configure o servidor web

**Apache (.htaccess já incluído)**
- Certifique-se de que o mod_rewrite está habilitado
- Aponte o DocumentRoot para a pasta do projeto

**Nginx**
```nginx
server {
    listen 80;
    server_name seu-dominio.com;
    root /caminho/para/associacao-php;
    index index.php;
    
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    location ~ \.php$ {
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

## 🔑 Primeiro Acesso

**Usuário padrão:**
- **Usuário:** admin
- **Senha:** admin123

⚠️ **IMPORTANTE:** Altere a senha padrão após o primeiro login!

## 📁 Estrutura do Projeto

```
associacao-php/
├── assets/
│   └── css/
│       └── tailwind.min.css    # Tailwind CSS local
├── auth/
│   ├── login.php               # Página de login
│   └── logout.php              # Logout
├── config/
│   └── database.php            # Configurações do banco
├── pages/
│   ├── dashboard.php           # Dashboard principal
│   ├── alunos.php             # Gestão de alunos
│   ├── atividades.php         # Gestão de atividades
│   ├── turmas.php             # Gestão de turmas
│   ├── matriculas.php         # Gestão de matrículas
│   └── relatorios.php         # Relatórios
├── database.sql               # Script de criação do banco
├── index.php                  # Página inicial
└── README.md                  # Este arquivo
```

## 🎯 Funcionalidades

### Dashboard
- Visão geral com estatísticas
- Cards informativos
- Navegação rápida

### Gestão de Alunos
- Cadastro completo de alunos
- Controle de responsáveis
- Busca e filtros
- Status ativo/inativo

### Gestão de Atividades
- Cadastro de atividades
- Categorização
- Controle de faixa etária
- Status ativa/inativa

### Gestão de Turmas
- Vinculação com atividades
- Controle de horários
- Limite de vagas
- Acompanhamento de ocupação

### Gestão de Matrículas
- Inscrição de alunos em turmas
- Controle de status
- Histórico de matrículas
- Validação de duplicatas

### Relatórios
- Relatório de alunos com filtros
- Relatório de turmas
- Relatório de matrículas
- Função de impressão

## 🔒 Segurança

- Senhas criptografadas com `password_hash()`
- Controle de sessões
- Validação de entrada
- Proteção contra SQL Injection (PDO)
- Escape de saída HTML

## 🎨 Interface

- Design responsivo
- Tailwind CSS local (sem CDN)
- Interface intuitiva
- Compatível com dispositivos móveis

## 🔧 Manutenção

### Backup do Banco de Dados
```bash
mysqldump -u usuario -p associacao_amigo_povo > backup_$(date +%Y%m%d).sql
```

### Atualização do Tailwind CSS
Se necessário atualizar o Tailwind CSS:
```bash
curl -o assets/css/tailwind.min.css https://unpkg.com/tailwindcss@latest/dist/tailwind.min.css
```

## 🐛 Solução de Problemas

### Erro de Conexão com Banco
1. Verifique as configurações em `config/database.php`
2. Confirme se o MySQL está rodando
3. Teste a conexão manualmente

### Erro 500 - Internal Server Error
1. Verifique os logs do servidor web
2. Confirme as permissões dos arquivos
3. Verifique se todas as extensões PHP estão instaladas

### Problemas de Login
1. Verifique se as tabelas foram criadas corretamente
2. Confirme se o usuário padrão foi inserido
3. Teste com: admin / admin123

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o sistema, entre em contato com a equipe de desenvolvimento.

## 📄 Licença

Este projeto foi desenvolvido especificamente para a Associação Amigo do Povo.

---

**Desenvolvido com ❤️ para a Associação Amigo do Povo**