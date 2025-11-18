# utils/helpers.py
# Funções auxiliares para o Banco Malvader

import hashlib
from database.conexao import conectar

# -----------------------------
# HASH MD5
# -----------------------------
def md5_hash(texto: str) -> str:
    """Gera hash MD5 para autenticação."""
    return hashlib.md5(texto.encode('utf-8')).hexdigest()

# -----------------------------
# EXECUÇÃO DE QUERY ÚNICA
# -----------------------------
def fetchone(query: str, params=None):
    conn, cur = conectar()
    if not conn:
        print("Erro: sem conexão com o banco.")
        return None
    cur.execute(query, params or ())
    r = cur.fetchone()
    cur.close(); conn.close()
    return r

# -----------------------------
# EXECUÇÃO DE MÚLTIPLAS LINHAS
# -----------------------------
def fetchall(query: str, params=None):
    conn, cur = conectar()
    if not conn:
        return None
    cur.execute(query, params or ())
    r = cur.fetchall()
    cur.close(); conn.close()
    return r

# -----------------------------
# EXECUÇÃO DE INSERT/UPDATE/DELETE
# -----------------------------
def execute(query: str, params=None) -> bool:
    conn, cur = conectar()
    if not conn:
        print("Erro: sem conexão com o banco.")
        return False
    try:
        cur.execute(query, params or ())
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao executar SQL: {e}")
        return False
    finally:
        cur.close(); conn.close()

# -----------------------------
# FUNÇÃO GERAL PARA POP-UPS
# -----------------------------
import customtkinter as ctk

def popup(titulo: str, mensagem: str, cor="white"):
    """Janela simples de aviso ou erro."""
    win = ctk.CTk()
    win.title(titulo)
    win.geometry("380x200")

    ctk.CTkLabel(win, text=mensagem, text_color=cor, font=("Arial", 16), wraplength=300).pack(pady=35)
    ctk.CTkButton(win, text="OK", command=win.destroy).pack(pady=10)

    win.mainloop()

# -----------------------------
# VALIDAÇÃO DE CAMPOS
# -----------------------------
def validar_valor(valor_str: str):
    """Verifica se o valor pode ser convertido para float."""
    try:
        v = float(valor_str)
        return v if v >= 0 else None
    except:
        return None


def validar_cpf(cpf: str) -> bool:
    return cpf.isdigit() and len(cpf) == 11
