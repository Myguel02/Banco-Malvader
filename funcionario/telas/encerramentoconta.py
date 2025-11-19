import customtkinter as ctk
from database.conexao import fetchone, exec_commit


def tela_abrir_conta(id_funcionario):

    janela = ctk.CTkToplevel()
    janela.title("Abertura de Conta")
    janela.geometry("420x520")

    ctk.CTkLabel(janela, text="Abertura de Conta", font=("Arial", 20)).pack(pady=10)

    entry_cpf = ctk.CTkEntry(janela, placeholder_text="CPF do Cliente")
    entry_cpf.pack(pady=6)

    entry_agencia = ctk.CTkEntry(janela, placeholder_text="ID da Agência")
    entry_agencia.pack(pady=6)

    tipo_conta = ctk.CTkOptionMenu(janela, values=["POUPANCA", "CORRENTE", "INVESTIMENTO"])
    tipo_conta.pack(pady=6)

    entry_extra1 = ctk.CTkEntry(janela, placeholder_text="Dado Extra (ex: taxa, limite, risco)")
    entry_extra1.pack(pady=6)

    entr
