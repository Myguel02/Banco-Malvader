import mysql.connector
from mysql.connector import Error

import os

CONFIG = {
    'host': os.getenv("DB_HOST", "localhost"),
    'user': os.getenv("DB_USER", "root"),
    'password': os.getenv("DB_PASSWORD", "M@cieira22"),
    'database': os.getenv("DB_NAME", "banco_malvader")
}


def conectar():
    """Cria conexão com banco e retorna (conn, cursor)."""
    try:
        conn = mysql.connector.connect(**CONFIG)
        cur = conn.cursor(buffered=True)  # ← CORREÇÃO IMPORTANTE
        return conn, cur
    except Error as e:
        print("Erro ao conectar ao MySQL:", e)
        return None, None


def fetchone(query, params=None):
    conn, cur = conectar()
    if not conn:
        return None
    cur.execute(query, params or ())
    r = cur.fetchone()
    cur.close()
    conn.close()
    return r


def fetchall(query, params=None):
    conn, cur = conectar()
    if not conn:
        return None
    cur.execute(query, params or ())
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def exec_commit(query, params=None):
    conn, cur = conectar()
    if not conn:
        return False, "Falha na conexão"
    try:
        cur.execute(query, params or ())
        conn.commit()
        cur.close()
        conn.close()
        return True, None
    except Error as e:
        conn.rollback()
        cur.close()
        conn.close()
        return False, str(e)
