#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar executável da Academia Amigo do Povo
Usa PyInstaller para gerar um executável standalone
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_executable():
    """Cria o executável usando PyInstaller"""
    
    print("🚀 Iniciando criação do executável...")
    
    # Configurações do PyInstaller
    app_name = "AcademiaAmigoDoPovo"
    main_script = "app.py"
    
    # Verificar se o arquivo principal existe
    if not os.path.exists(main_script):
        print(f"❌ Arquivo {main_script} não encontrado!")
        return False
    
    # Criar diretório de build se não existir
    build_dir = Path("build")
    dist_dir = Path("dist")
    
    # Limpar builds anteriores
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print("🧹 Limpando build anterior...")
    
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
        print("🧹 Limpando distribuição anterior...")
    
    # Comando PyInstaller
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",  # Criar um único arquivo executável
        "--windowed",  # Sem console (para Windows)
        f"--name={app_name}",
        "--add-data=templates;templates",  # Incluir templates
        "--add-data=static;static",  # Incluir arquivos estáticos
        "--add-data=*.json;.",  # Incluir arquivos JSON
        "--hidden-import=flask",
        "--hidden-import=sqlite3",
        "--hidden-import=pandas",
        "--hidden-import=pymongo",
        "--hidden-import=werkzeug",
        "--hidden-import=jinja2",
        "--collect-all=flask",
        "--collect-all=jinja2",
        "--collect-all=werkzeug",
        main_script
    ]
    
    try:
        print("⚙️ Executando PyInstaller...")
        print(f"Comando: {' '.join(pyinstaller_cmd)}")
        
        # Executar PyInstaller
        result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executável criado com sucesso!")
            
            # Verificar se o executável foi criado
            exe_path = dist_dir / f"{app_name}.exe"
            if exe_path.exists():
                print(f"📁 Executável localizado em: {exe_path.absolute()}")
                
                # Criar arquivo de configuração para executável
                create_executable_config()
                
                # Copiar arquivos necessários
                copy_required_files()
                
                print("🎉 Build concluído com sucesso!")
                print(f"📦 Executável: {exe_path.absolute()}")
                return True
            else:
                print("❌ Executável não foi encontrado após o build")
                return False
        else:
            print("❌ Erro durante o build:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar PyInstaller: {e}")
        return False

def create_executable_config():
    """Cria arquivo de configuração para o executável"""
    config_content = """
# Configuração para executável
USE_LOCAL_DB=true
FLASK_ENV=production
SECRET_KEY=associacao_amigo_do_povo_2024_secure_key_executable
"""
    
    with open("dist/.env", "w", encoding="utf-8") as f:
        f.write(config_content)
    
    print("⚙️ Arquivo de configuração criado")

def copy_required_files():
    """Copia arquivos necessários para o diretório de distribuição"""
    dist_path = Path("dist")
    
    # Arquivos a serem copiados
    files_to_copy = [
        "README.md",
        "requirements.txt"
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, dist_path / file_name)
            print(f"📄 Copiado: {file_name}")
    
    # Criar arquivo de instruções
    instructions = """
# Academia Amigo do Povo - Executável

## Como usar:

1. Execute o arquivo AcademiaAmigoDoPovo.exe
2. O sistema abrirá automaticamente no navegador
3. Use as credenciais padrão para fazer login:
   - Usuário: admin
   - Senha: admin123

## Características:

- ✅ Funciona completamente offline
- ✅ Banco de dados local SQLite
- ✅ Todos os dados são salvos localmente
- ✅ Não requer instalação do Python
- ✅ Não requer conexão com internet

## Localização dos dados:

Os dados são salvos no arquivo 'academia_local.db' no mesmo diretório do executável.

## Suporte:

Para suporte técnico, entre em contato com a equipe de desenvolvimento.
"""
    
    with open(dist_path / "LEIA-ME.txt", "w", encoding="utf-8") as f:
        f.write(instructions)
    
    print("📋 Instruções criadas")

def main():
    """Função principal"""
    print("🏗️ Academia Amigo do Povo - Build Executável")
    print("=" * 50)
    
    # Verificar se PyInstaller está instalado
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ PyInstaller não encontrado. Instale com: pip install pyinstaller")
        return False
    
    # Criar executável
    success = create_executable()
    
    if success:
        print("\n🎉 Build concluído com sucesso!")
        print("📁 Verifique o diretório 'dist' para o executável")
    else:
        print("\n❌ Falha no build")
    
    return success

if __name__ == "__main__":
    main()