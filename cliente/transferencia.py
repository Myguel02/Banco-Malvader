import customtkinter as ctk
from decimal import Decimal, InvalidOperation

from database.conexao import (
    obter_contas_do_cliente,
    verificar_saldo_e_limite,
    buscar_conta_por_numero
)
from database.conexao import inserir_transacao


class TelaTransferencia(ctk.CTkToplevel):

    def __init__(self, id_cliente):
        super().__init__()

        self.id_cliente = id_cliente

        self.title("Transferência - Banco Malvader")
        self.geometry("520x500")

        ctk.set_appearance_mode("dark")

        titulo = ctk.CTkLabel(self, text="Transferência", font=("Arial", 22))
        titulo.pack(pady=15)

        # ----------- CONTA ORIGEM -----------
        ctk.CTkLabel(self, text="Escolha a conta de origem").pack(pady=5)

        self.combo_origem = ctk.CTkComboBox(self, width=350, values=[])
        self.combo_origem.pack(pady=5)

        self.carregar_contas()

        # ----------- CONTA DESTINO -----------
        ctk.CTkLabel(self, text="Número da conta destino").pack(pady=(20, 5))
        self.entry_destino = ctk.CTkEntry(self, placeholder_text="Ex: 100245-1", width=250)
        self.entry_destino.pack(pady=5)

        # ----------- VALOR -----------
        ctk.CTkLabel(self, text="Valor da transferência").pack(pady=(20, 5))
        self.entry_valor = ctk.CTkEntry(self, placeholder_text="Ex: 200.00", width=200)
        self.entry_valor.pack(pady=5)

        # ----------- MENSAGEM ----------
        self.lbl_msg = ctk.CTkLabel(self, text="")
        self.lbl_msg.pack(pady=10)

        # ----------- BOTÃO ------------
        ctk.CTkButton(self, text="Transferir", command=self.realizar_transferencia).pack(pady=20)

    # ----------------------------------------------------------------
    def carregar_contas(self):
        contas = obter_contas_do_cliente(self.id_cliente)

        if not contas:
            self.combo_origem.configure(values=["Nenhuma conta disponível"])
            return

        lista_fmt = []
        for idc, numero, saldo, tipo in contas:
            lista_fmt.append(f"{idc} | {numero} | {tipo} | Saldo: {saldo}")

        self.combo_origem.configure(values=lista_fmt)

    # ----------------------------------------------------------------
    def realizar_transferencia(self):
        selecionado = self.combo_origem.get()

        if "|" not in selecionado:
            self.lbl_msg.configure(text="Selecione uma conta de origem.", text_color="red")
            return

        id_origem = int(selecionado.split("|")[0].strip())

        destino = self.entry_destino.get().strip()
        if not destino:
            self.lbl_msg.configure(text="Digite o número da conta destino.", text_color="red")
            return

        # buscar conta destino
        r = buscar_conta_por_numero(destino)
        if not r:
            self.lbl_msg.configure(text="Conta destino não encontrada.", text_color="red")
            return

        id_destino = r[0]

        # valor
        try:
            valor = Decimal(self.entry_valor.get().strip())
            if valor <= 0:
                raise InvalidOperation()
        except:
            self.lbl_msg.configure(text="Valor inválido.", text_color="red")
            return

        # verificar saldo
        saldo, limite = verificar_saldo_e_limite(id_origem)
        if saldo is None:
            self.lbl_msg.configure(text="Conta origem não encontrada.", text_color="red")
            return

        disponivel = saldo + limite

        if valor > disponivel:
            self.lbl_msg.configure(
                text=f"Saldo insuficiente. Disponível: R${disponivel}",
                text_color="red"
            )
            return

        # realizar transferência
        ok, err = inserir_transacao(
            tipo="TRANSFERENCIA",
            valor=valor,
            id_conta_origem=id_origem,
            id_conta_destino=id_destino,
            descricao=f"Transferência entre contas - Cliente {self.id_cliente}"
        )

        if ok:
            self.lbl_msg.configure(text="Transferência realizada com sucesso!", text_color="green")
            self.entry_valor.delete(0, "end")
            self.entry_destino.delete(0, "end")
            self.carregar_contas()
        else:
            self.lbl_msg.configure(text=f"Erro: {err}", text_color="red")
