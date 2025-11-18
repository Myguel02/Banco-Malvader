import customtkinter as ctk
from cliente.deposito import TelaDeposito
from cliente.saque import TelaSaque
from cliente.transferencia import TelaTransferencia
from cliente.extrato import TelaExtrato
from cliente.perfil import TelaPerfil
from cliente.endereco import TelaEndereco
from cliente.investimento import TelaInvestimento


class MenuCliente(ctk.CTk):

    def __init__(self, id_cliente, nome_cliente):
        super().__init__()

        self.id_cliente = id_cliente
        self.nome_cliente = nome_cliente

        self.title("Banco Malvader - Área do Cliente")
        self.geometry("600x500")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Cabeçalho
        titulo = ctk.CTkLabel(self, text=f"Bem-vindo, {self.nome_cliente}", font=("Arial", 20))
        titulo.pack(pady=20)

        # Frame de botões
        frame = ctk.CTkFrame(self)
        frame.pack(pady=20, fill="both", expand=True)

        # ---- Botões ----
        botoes = [
            ("Depósito", self.abrir_deposito),
            ("Saque", self.abrir_saque),
            ("Transferência", self.abrir_transferencia),
            ("Extrato", self.abrir_extrato),
            ("Perfil", self.abrir_perfil),
            ("Endereço", self.abrir_endereco),
            ("Simulador de Investimentos", self.abrir_investimento),
            ("Sair", self.sair)
        ]

        for texto, comando in botoes:
            btn = ctk.CTkButton(frame, text=texto, width=200, command=comando)
            btn.pack(pady=10)

    # -------- Telas do Cliente -------- #

    def abrir_deposito(self):
        TelaDeposito(self.id_cliente)

    def abrir_saque(self):
        TelaSaque(self.id_cliente)

    def abrir_transferencia(self):
        TelaTransferencia(self.id_cliente)

    def abrir_extrato(self):
        TelaExtrato(self.id_cliente)

    def abrir_perfil(self):
        TelaPerfil(self.id_cliente)

    def abrir_endereco(self):
        TelaEndereco(self.id_cliente)

    def abrir_investimento(self):
        TelaInvestimento(self.id_cliente)

    def sair(self):
        self.destroy()
