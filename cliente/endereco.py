import customtkinter as ctk
from database.conexao import fetchone, exec_commit, fetchall

class TelaEndereco(ctk.CTkToplevel):

    def __init__(self, id_cliente):
        super().__init__()

        self.id_cliente = id_cliente
        self.title("Endereço do Cliente - Banco Malvader")
        self.geometry("650x520")
        ctk.set_appearance_mode("dark")

        ctk.CTkLabel(self, text="Gerenciar Endereço", font=("Arial", 22)).pack(pady=10)

        # Carregar dados iniciais
        self.dados_usuario = self.buscar_usuario()
        self.dados_endereco = self.buscar_endereco()

        self.criar_campos()

        self.lbl_status = ctk.CTkLabel(self, text="")
        self.lbl_status.pack(pady=10)

    # ---------------------------------------------------------------
    def buscar_usuario(self):
        sql = """
            SELECT u.id_usuario, u.nome, u.cpf
            FROM usuario u
            JOIN cliente c ON c.id_usuario = u.id_usuario
            WHERE c.id_cliente = %s
        """
        return fetchone(sql, (self.id_cliente,))  # (id_usuario, nome, cpf)

    # ---------------------------------------------------------------
    def buscar_endereco(self):
        sql = "SELECT id_endereco, cep, local, numero_casa, bairro, cidade, estado, complemento FROM endereco_usuario WHERE id_usuario = %s"
        return fetchone(sql, (self.dados_usuario[0],))

    # ---------------------------------------------------------------
    def criar_campos(self):
        uid, nome, cpf = self.dados_usuario

        frame = ctk.CTkFrame(self)
        frame.pack(pady=10)

        ctk.CTkLabel(frame, text=f"Cliente: {nome} (CPF: {cpf})", font=("Arial", 16)).pack(pady=5)

        # CAMPOS DO ENDEREÇO
        labels = ["CEP", "Rua / Logradouro", "Número", "Bairro", "Cidade", "Estado (UF)", "Complemento"]
        self.inputs = {}

        valores = ["", "", "", "", "", "", ""]

        if self.dados_endereco:  # Se já existe endereço
            _, cep, local, numero_casa, bairro, cidade, estado, complemento = self.dados_endereco
            valores = [cep, local, str(numero_casa), bairro, cidade, estado, complemento or ""]

        for label, valor in zip(labels, valores):
            ctk.CTkLabel(frame, text=label).pack()
            entrada = ctk.CTkEntry(frame, width=500)
            entrada.insert(0, valor)
            entrada.pack(pady=3)
            self.inputs[label] = entrada

        # Botão salvar
        ctk.CTkButton(self, text="Salvar Endereço", command=self.salvar).pack(pady=15)

    # ---------------------------------------------------------------
    def salvar(self):
        uid, _, _ = self.dados_usuario

        cep = self.inputs["CEP"].get().strip()
        local = self.inputs["Rua / Logradouro"].get().strip()
        numero = self.inputs["Número"].get().strip()
        bairro = self.inputs["Bairro"].get().strip()
        cidade = self.inputs["Cidade"].get().strip()
        estado = self.inputs["Estado (UF)"].get().strip().upper()
        complemento = self.inputs["Complemento"].get().strip()

        if not (cep and local and numero and bairro and cidade and estado):
            self.lbl_status.configure(text="Preencha todos os campos obrigatórios.", text_color="red")
            return

        try:
            numero = int(numero)
        except:
            self.lbl_status.configure(text="O número da residência deve ser numérico.", text_color="red")
            return

        if self.dados_endereco:  # UPDATE
            sql = """
                UPDATE endereco_usuario
                SET cep=%s, local=%s, numero_casa=%s, bairro=%s, cidade=%s, estado=%s, complemento=%s
                WHERE id_endereco=%s
            """
            ok, err = exec_commit(sql, (
                cep, local, numero, bairro, cidade, estado, complemento,
                self.dados_endereco[0]
            ))
        else:  # INSERT
            sql = """
                INSERT INTO endereco_usuario (id_usuario, cep, local, numero_casa, bairro, cidade, estado, complemento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            ok, err = exec_commit(sql, (
                uid, cep, local, numero, bairro, cidade, estado, complemento
            ))

        if ok:
            self.lbl_status.configure(text="Endereço salvo com sucesso!", text_color="green")
        else:
            self.lbl_status.configure(text=f"Erro: {err}", text_color="red")
