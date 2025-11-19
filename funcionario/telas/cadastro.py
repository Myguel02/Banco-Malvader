import customtkinter as ctk
from database.conexao import fetchone, exec_commit
from utils.helpers import md5_hash


def tela_cadastrar_func(id_funcionario):

    janela = ctk.CTkToplevel()
    janela.title("Cadastrar Funcionário")
    janela.geometry("420x520")

    ctk.CTkLabel(janela, text="Cadastro de Funcionário", font=("Arial", 20)).pack(pady=10)

    entry_nome = ctk.CTkEntry(janela, placeholder_text="Nome")
    entry_nome.pack(pady=6)

    entry_cpf = ctk.CTkEntry(janela, placeholder_text="CPF")
    entry_cpf.pack(pady=6)

    entry_tel = ctk.CTkEntry(janela, placeholder_text="Telefone")
    entry_tel.pack(pady=6)

    entry_nasc = ctk.CTkEntry(janela, placeholder_text="Data nascimento (AAAA-MM-DD)")
    entry_nasc.pack(pady=6)

    cargo = ctk.CTkOptionMenu(janela, values=["ESTAGIARIO", "ATENDENTE", "GERENTE"])
    cargo.pack(pady=6)

    entry_senha = ctk.CTkEntry(janela, placeholder_text="Senha", show="*")
    entry_senha.pack(pady=6)

    lbl = ctk.CTkLabel(janela, text="")
    lbl.pack(pady=10)

    def salvar():

        exec_commit("""
            INSERT INTO usuario (nome, cpf, data_nascimento, telefone, tipo_usuario, senha_hash)
            VALUES (%s, %s, %s, %s, 'FUNCIONARIO', %s)
        """, (
            entry_nome.get(),
            entry_cpf.get(),
            entry_nasc.get(),
            entry_tel.get(),
            md5_hash(entry_senha.get())
        ))

        r = fetchone("SELECT id_usuario FROM usuario WHERE cpf=%s", (entry_cpf.get(),))
        id_usuario = r[0]

        exec_commit("""
            INSERT INTO funcionario (id_usuario, id_agencia, cargo)
            VALUES (%s, 1, %s)
        """, (id_usuario, cargo.get()))

        lbl.configure(text="Funcionário cadastrado!", text_color="green")

    ctk.CTkButton(janela, text="Cadastrar", command=salvar).pack(pady=10)
    ctk.CTkButton(janela, text="Fechar", command=janela.destroy).pack(pady=4)
