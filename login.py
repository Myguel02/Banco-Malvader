import customtkinter as ctk
from database.conexao import conectar, fetchone, fetchall, exec_commit
from utils.helpers import md5_hash



def criar_tela_login():
    app = ctk.CTk()
    app.title("Banco Malvader - Login")
    app.geometry("420x360")

    ctk.CTkLabel(app, text="Login", font=("Arial", 20)).pack(pady=10)
    ctk.CTkLabel(app, text="CPF").pack(pady=(6,0))
    entry_cpf = ctk.CTkEntry(app, placeholder_text="Digite seu CPF")
    entry_cpf.pack(pady=6)
    ctk.CTkLabel(app, text="Senha").pack(pady=(6,0))
    entry_senha = ctk.CTkEntry(app, placeholder_text="Digite sua senha", show="*")
    entry_senha.pack(pady=6)
    lbl_res = ctk.CTkLabel(app, text="")
    lbl_res.pack(pady=6)

    def validar_login():
        cpf = entry_cpf.get().strip()
        senha = entry_senha.get().strip()

        if not cpf or not senha:
            lbl_res.configure(text="Preencha CPF e senha.", text_color="red")
            return

        hash_senha = md5_hash(senha)

        r = fetchone(
            "SELECT id_usuario, senha_hash, tipo_usuario FROM usuario WHERE cpf = %s",
            (cpf,)
        )
        if not r:
            lbl_res.configure(text="CPF ou senha incorretos.", text_color="red")
            return

        id_usuario, senha_db, tipo = r

        if hash_senha != senha_db:
            lbl_res.configure(text="CPF ou senha incorretos.", text_color="red")
            return

        app.destroy()  # fecha tela de login

        try:
            if tipo == 'CLIENTE':
                from cliente.menu_cliente import abrir_app_cliente
                r2 = fetchone("SELECT id_cliente FROM cliente WHERE id_usuario = %s", (id_usuario,))
                if r2:
                    abrir_app_cliente(r2[0])
                else:
                    print("Cliente não encontrado.")

            elif tipo == 'FUNCIONARIO':
                print("Área do funcionário ainda não implementada.")
                return

        except Exception as e:
            print("Erro ao abrir área do usuário:", e)

    ctk.CTkButton(app, text="Login", command=validar_login).pack(pady=12)
    app.mainloop()


if __name__ == '__main__':
    criar_tela_login()
