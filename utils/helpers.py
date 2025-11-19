import hashlib

def md5_hash(texto: str):
    """Gera hash MD5 para senhas."""
    return hashlib.md5(texto.encode()).hexdigest()

def format_currency(v):
    """Formata valores numéricos no padrão brasileiro."""
    try:
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"
