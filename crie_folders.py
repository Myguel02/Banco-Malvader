import os
import shutil

# Pastas que devem existir
FOLDERS = ["database", "cliente"]

FILES_CLIENTE = [
    "deposito.py",
    "saque.py",
    "transferencia.py",
    "extrato.py",
    "perfil.py",
    "endereco.py",
    "helpers.py",
    "menu_cliente.py"
]

FILES_DATABASE = [
    "conexao.py"
]

def criar_pastas():
    for folder in FOLDERS:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✔ Pasta criada: {folder}")

def mover_arquivos():
    # mover arquivos do cliente
    for file in FILES_CLIENTE:
        if os.path.exists(file):
            shutil.move(file, os.path.join("cliente", file))
            print(f"✔ Arquivo movido: {file} → cliente/")

    # mover arquivos do banco de dados
    for file in FILES_DATABASE:
        if os.path.exists(file):
            shutil.move(file, os.path.join("database", file))
            print(f"✔ Arquivo movido: {file} → database/")

    # remover arquivos duplicados dentro das pastas (se existirem)
    duplicates = [
        "extrato.py", "perfil.py", "endereco.py",
        "deposito.py", "saque.py", "transferencia.py",
        "menu_cliente.py"
    ]

    for d in duplicates:
        path = os.path.join("Banco malvader", d)
        if os.path.exists(path):
            os.remove(path)
            print(f"❌ Arquivo duplicado removido: {path}")

def main():
    print("\n🚀 Organizando projeto Banco Malvader...\n")
    criar_pastas()
    mover_arquivos()
    print("\n🏁 Estrutura finalizada com sucesso!\n")

if __name__ == "__main__":
    main()
