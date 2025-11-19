import customtkinter as ctk
from database.conexao import fetchone
from utils.helpers import md5_hash


def criar_tela_login_funcionario():
    app = ctk.CTk()
    app.title("Banco Malvader - Login Funcionário")
    app.geometry("420x360")

    ctk.CTkLabel(app, text="Login Funcionário", font=("Arial", 22)).pack(pady=10)

    # -------- CPF --------
    ctk.CTkLabel(app, text="CPF").pack(pady=4)
    entry_cpf = ctk.CTkEntry(app, placeholder_text="Digite seu CPF")
    entry_cpf.pack(pady=6)

    # -------- SENHA --------
    ctk.CTkLabel(app, text="Senha").pack(pady=4)
    entry_senha = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*")
    entry_senha.pack(pady=6)

    lbl_res = ctk.CTkLabel(app, text="")
    lbl_res.pack(pady=8)

    # ----------------------------------------------------
    #              FUNÇÃO VALIDAR FUNCIONÁRIO
    # ----------------------------------------------------
    def validar():
        cpf = entry_cpf.get().strip()
        senha = entry_senha.get().strip()

        if not cpf or not senha:
            lbl_res.configure(text="Preencha todos os campos!", text_color="red")
            return

        r = fetchone("""
            SELECT id_usuario, senha_hash, tipo_usuario 
            FROM usuario 
            WHERE cpf = %s
        """, (cpf,))

        if not r:
            lbl_res.configure(text="CPF ou senha inválidos!", text_color="red")
            return

        id_usuario, senha_hash_db, tipo = r

        if tipo != "FUNCIONARIO":
            lbl_res.configure(text="Usuário não é funcionário!", text_color="red")
            return

        if md5_hash(senha) != senha_hash_db:
            lbl_res.configure(text="Senha incorreta!", text_color="red")
            return

        # LOGIN OK
        app.destroy()

        from funcionario.Menu import abrir_menu_funcionario
        abrir_menu_funcionario(id_usuario)

    ctk.CTkButton(app, text="Entrar", command=validar).pack(pady=12)

    app.mainloop()


if __name__ == "__main__":
    criar_tela_login_funcionario()
