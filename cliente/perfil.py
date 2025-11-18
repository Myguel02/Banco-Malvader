import customtkinter as ctk
from database.helpers import md5_hash
from database.conexao import fetchone, exec_commit


class TelaPerfil(ctk.CTkToplevel):

    def __init__(self, id_cliente):
        super().__init__()

        self.id_cliente = id_cliente

        self.title("Perfil do Cliente - Banco Malvader")
        self.geometry("620x520")
        ctk.set_appearance_mode("dark")

        ctk.CTkLabel(self, text="Meu Perfil", font=("Arial", 22)).pack(pady=10)

        # Buscar dados do cliente
        self.user_data = self.buscar_dados()

        # ---- CAMPOS ----
        self.criar_campos()

        # LABEL DE STATUS
        self.lbl_status = ctk.CTkLabel(self, text="")
        self.lbl_status.pack(pady=10)

    # -------------------------------------------------------------------
    def buscar_dados(self):
        sql = """
            SELECT u.id_usuario, u.nome, u.cpf, u.telefone, u.data_nascimento
            FROM usuario u
            JOIN cliente c ON c.id_usuario = u.id_usuario
            WHERE c.id_cliente = %s
        """
        r = fetchone(sql, (self.id_cliente,))
        return r  # (id_usuario, nome, cpf, telefone, data_nascimento)

    # -------------------------------------------------------------------
    def criar_campos(self):

        uid, nome, cpf, tel, data_nasc = self.user_data

        # Nome
        ctk.CTkLabel(self, text="Nome completo").pack()
        self.ent_nome = ctk.CTkEntry(self, width=480)
        self.ent_nome.insert(0, nome)
        self.ent_nome.pack(pady=4)

        # CPF (não editável)
        ctk.CTkLabel(self, text="CPF (não editável)").pack()
        self.ent_cpf = ctk.CTkEntry(self, width=480)
        self.ent_cpf.insert(0, cpf)
        self.ent_cpf.configure(state="disabled")
        self.ent_cpf.pack(pady=4)

        # Telefone
        ctk.CTkLabel(self, text="Telefone").pack()
        self.ent_tel = ctk.CTkEntry(self, width=480)
        self.ent_tel.insert(0, tel)
        self.ent_tel.pack(pady=4)

        # Data de nascimento
        ctk.CTkLabel(self, text="Data Nascimento (yyyy-mm-dd)").pack()
        self.ent_data = ctk.CTkEntry(self, width=480)
        self.ent_data.insert(0, str(data_nasc))
        self.ent_data.pack(pady=4)

        # Trocar senha
        ctk.CTkLabel(self, text="Nova senha (opcional)").pack()
        self.ent_senha = ctk.CTkEntry(self, width=480, show="*")
        self.ent_senha.pack(pady=4)

        # Botão salvar
        ctk.CTkButton(self, text="Salvar alterações", command=self.salvar).pack(pady=15)

    # -------------------------------------------------------------------
    def salvar(self):
        uid, _, _, _, _ = self.user_data

        nome = self.ent_nome.get().strip()
        telefone = self.ent_tel.get().strip()
        data_nasc = self.ent_data.get().strip()
        nova_senha = self.ent_senha.get().strip()

        if not nome or not telefone or not data_nasc:
            self.lbl_status.configure(text="Todos os campos devem ser preenchidos (exceto senha).", text_color="red")
            return

        # Atualizar nome / telefone / nascimento
        sql = "UPDATE usuario SET nome=%s, telefone=%s, data_nascimento=%s WHERE id_usuario=%s"
        ok, err = exec_commit(sql, (nome, telefone, data_nasc, uid))

        if not ok:
            self.lbl_status.configure(text=f"Erro ao atualizar: {err}", text_color="red")
            return

        # Atualizar senha (caso preenchida)
        if nova_senha:
            senha_hash = md5_hash(nova_senha)
            sql2 = "UPDATE usuario SET senha_hash=%s WHERE id_usuario=%s"
            ok2, err2 = exec_commit(sql2, (senha_hash, uid))

            if not ok2:
                self.lbl_status.configure(text=f"Dados salvos, mas erro ao trocar senha: {err2}", text_color="orange")
                return

        self.lbl_status.configure(text="Dados atualizados com sucesso!", text_color="green")
