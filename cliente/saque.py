import customtkinter as ctk
from decimal import Decimal, InvalidOperation

from database.db_conta import obter_contas_do_cliente, verificar_saldo_e_limite, contar_saques_mes
from database.db_transacao import inserir_transacao


class TelaSaque(ctk.CTkToplevel):

    def __init__(self, id_cliente):
        super().__init__()

        self.id_cliente = id_cliente

        self.title("Saque - Banco Malvader")
        self.geometry("500x420")

        ctk.set_appearance_mode("dark")

        titulo = ctk.CTkLabel(self, text="Saque", font=("Arial", 22))
        titulo.pack(pady=15)

        # ----------- SELEÇÃO DE CONTA -----------
        ctk.CTkLabel(self, text="Selecione a conta de origem").pack(pady=5)

        self.combo_contas = ctk.CTkComboBox(self, width=300, values=[])
        self.combo_contas.pack(pady=5)

        self.atualizar_contas()

        # ----------- VALOR -----------
        ctk.CTkLabel(self, text="Valor do saque").pack(pady=(20, 5))
        self.entry_valor = ctk.CTkEntry(self, placeholder_text="Ex: 50.00", width=200)
        self.entry_valor.pack(pady=5)

        # ----------- MENSAGEM ----------
        self.lbl_msg = ctk.CTkLabel(self, text="")
        self.lbl_msg.pack(pady=10)

        # ----------- BOTÃO ------------
        ctk.CTkButton(self, text="Sacar", command=self.realizar_saque).pack(pady=20)

    # ------------------------------------------------------------
    def atualizar_contas(self):
        contas = obter_contas_do_cliente(self.id_cliente)

        if not contas:
            self.combo_contas.configure(values=["Nenhuma conta encontrada"])
            return

        lista_fmt = []
        for idc, numero, saldo, tipo in contas:
            lista_fmt.append(f"{idc} | {numero} | {tipo} | Saldo: {saldo}")

        self.combo_contas.configure(values=lista_fmt)

    # ------------------------------------------------------------
    def realizar_saque(self):
        selecionado = self.combo_contas.get()

        if "|" not in selecionado:
            self.lbl_msg.configure(text="Selecione uma conta válida.", text_color="red")
            return

        id_conta = int(selecionado.split("|")[0].strip())

        # Valor do saque
        try:
            valor = Decimal(self.entry_valor.get().strip())
            if valor <= 0:
                raise InvalidOperation()
        except:
            self.lbl_msg.configure(text="Valor inválido.", text_color="red")
            return

        # Saldo + limite
        saldo, limite = verificar_saldo_e_limite(id_conta)

        if saldo is None:
            self.lbl_msg.configure(text="Conta não encontrada.", text_color="red")
            return

        disponivel = saldo + limite

        if valor > disponivel:
            self.lbl_msg.configure(
                text=f"Saldo insuficiente. Disponível: R${disponivel}",
                text_color="red"
            )
            return

        # Conta quantos saques já fez no mês
        saques_mes = contar_saques_mes(id_conta)
        taxa_extra = Decimal("2.00")  # taxa após 5 saques

        # Realizar o saque
        ok, err = inserir_transacao(
            tipo="SAQUE",
            valor=valor,
            id_conta_origem=id_conta,
            id_conta_destino=None,
            descricao=f"Saque realizado pelo cliente {self.id_cliente}"
        )

        if not ok:
            self.lbl_msg.configure(text=f"Erro: {err}", text_color="red")
            return

        # Aplicar taxa se necessário
        if saques_mes + 1 > 5:
            inserir_transacao(
                tipo="TAXA",
                valor=taxa_extra,
                id_conta_origem=id_conta,
                id_conta_destino=None,
                descricao="Taxa de saque excedente"
            )

        self.lbl_msg.configure(text="Saque realizado com sucesso!", text_color="green")
        self.entry_valor.delete(0, "end")
        self.atualizar_contas()
