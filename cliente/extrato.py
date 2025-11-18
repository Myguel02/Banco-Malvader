import customtkinter as ctk
from database.db_conta import obter_contas_do_cliente
from database.db_extrato import gerar_extrato, exportar_extrato_csv
from decimal import Decimal
from datetime import datetime


class TelaExtrato(ctk.CTkToplevel):

    def __init__(self, id_cliente):
        super().__init__()

        self.id_cliente = id_cliente

        self.title("Extrato Bancário - Banco Malvader")
        self.geometry("780x600")

        ctk.set_appearance_mode("dark")

        titulo = ctk.CTkLabel(self, text="Extrato de Conta", font=("Arial", 22))
        titulo.pack(pady=10)

        # ----------- SELEÇÃO DE CONTA -----------
        ctk.CTkLabel(self, text="Selecione a conta").pack(pady=5)

        self.combo_conta = ctk.CTkComboBox(self, values=[], width=500)
        self.combo_conta.pack(pady=5)

        self.carregar_contas()

        # ----------- BOTÃO GERAR EXTRATO -----------
        ctk.CTkButton(self, text="Gerar Extrato", command=self.exibir_extrato).pack(pady=10)

        # ----------- ÁREA DO EXTRATO -----------
        self.txt_extrato = ctk.CTkTextbox(self, width=740, height=380)
        self.txt_extrato.pack(pady=10)

        # ----------- EXPORTAR CSV -----------
        self.lbl_export = ctk.CTkLabel(self, text="")
        self.lbl_export.pack(pady=5)

        ctk.CTkButton(self, text="Exportar CSV", command=self.exportar).pack(pady=10)

    # ---------------------------------------------------------------
    def carregar_contas(self):
        contas = obter_contas_do_cliente(self.id_cliente)

        if not contas:
            self.combo_conta.configure(values=["Nenhuma conta disponível"])
            return

        lista_fmt = []

        for idc, numero, saldo, tipo in contas:
            lista_fmt.append(f"{idc} | {numero} | {tipo} | Saldo: {saldo}")

        self.combo_conta.configure(values=lista_fmt)

    # ---------------------------------------------------------------
    def exibir_extrato(self):
        selecionado = self.combo_conta.get()

        if "|" not in selecionado:
            self.txt_extrato.delete("0.0", "end")
            self.txt_extrato.insert("0.0", "Selecione uma conta válida.")
            return

        id_conta = int(selecionado.split("|")[0].strip())

        linhas = gerar_extrato(id_conta, limite=10)

        self.txt_extrato.delete("0.0", "end")

        if not linhas:
            self.txt_extrato.insert("0.0", "Nenhuma movimentação encontrada.")
            return

        for mov in linhas:
            idtx, tipo, valor, dh, orig, dest, desc = mov

            texto = (
                f"{dh} | {tipo} | R${valor} | "
                f"Origem: {orig} | Destino: {dest} | {desc}\n"
            )

            self.txt_extrato.insert("end", texto)

    # ---------------------------------------------------------------
    def exportar(self):
        selecionado = self.combo_conta.get()

        if "|" not in selecionado:
            self.lbl_export.configure(text="Selecione uma conta primeiro.", text_color="red")
            return

        id_conta = int(selecionado.split("|")[0].strip())

        ok, caminho = exportar_extrato_csv(id_conta)

        if ok:
            self.lbl_export.configure(
                text=f"Arquivo exportado com sucesso:\n{caminho}",
                text_color="green"
            )
        else:
            self.lbl_export.configure(
                text=f"Erro ao exportar: {caminho}",
                text_color="red"
            )
