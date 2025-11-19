import customtkinter as ctk
from database.conexao import fetchone
from utils.helpers import md5_hash


def criar_tela_login():
    app = ctk.CTk()
    app.title("Banco Malvader - Login")
    app.geometry("420x360")

    ctk.CTkLabel(app, text="Login", font=("Arial", 20)).pack(pady=10)

    # CPF
    ctk.CTkLabel(app, text="CPF").pack(pady=(6, 0))
    entry_cpf = ctk.CTkEntry(app, placeholder_text="Digite seu CPF")
    entry_cpf.pack(pady=6)

    # SENHA
    ctk.CTkLabel(app, text="Senha").pack(pady=(6, 0))
    entry_senha = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*")
    entry_senha.pack(pady=6)

    lbl_res = ctk.CTkLabel(app, text="")
    lbl_res.pack(pady=6)

    # -----------------------------
    # Função validar login
    # -----------------------------
    def validar_login():
        cpf = entry_cpf.get().strip()
        senha = entry_senha.get().strip()

        if not cpf or not senha:
            lbl_res.configure(text="Preencha CPF e senha.", text_color="red")
            return

        hash_senha = md5_hash(senha)

        # Buscar usuário
        r = fetchone(
            "SELECT id_usuario, senha_hash, tipo_usuario FROM usuario WHERE cpf = %s",
            (cpf,)
        )

        if not r:
            lbl_res.configure(text="CPF ou senha incorretos.", text_color="red")
            return

        id_usuario, senha_db, tipo = r

        # Verificar senha
        if hash_senha != senha_db:
            lbl_res.configure(text="CPF ou senha incorretos.", text_color="red")
            return

        lbl_res.configure(text="Login realizado!", text_color="green")
        app.destroy()  # fecha a tela de login

        # -----------------------------------------
        # ÁREA DO CLIENTE
        # -----------------------------------------
        if tipo == "CLIENTE":
            r2 = fetchone(
                "SELECT id_cliente FROM cliente WHERE id_usuario = %s",
                (id_usuario,)
            )

            if r2:
                from cliente.menu_cliente import abrir_app_cliente
                abrir_app_cliente(r2[0])
            else:
                print("Cliente não encontrado no banco.")

        # -----------------------------------------
        # ÁREA DO FUNCIONÁRIO
        # -----------------------------------------
        elif tipo == "FUNCIONARIO":
            from funcionario.Menu import abrir_app_funcionario
            abrir_app_funcionario(id_usuario)

    # Botão LOGIN
    ctk.CTkButton(app, text="Login", command=validar_login).pack(pady=12)

    app.mainloop()


if __name__ == '__main__':
    criar_tela_login()
