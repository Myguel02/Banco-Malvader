import customtkinter as ctk
from database.conexao import fetchall


def tela_relatorios(id_funcionario):

    janela = ctk.CTkToplevel()
    janela.title("Relatórios")
    janela.geometry("550x600")

    ctk.CTkLabel(janela, text="Relatórios", font=("Arial", 20)).pack(pady=10)

    menu = ctk.CTkOptionMenu(janela, values=[
        "Movimentações (últimos 90 dias)",
        "Resumo de contas por cliente",
        "Clientes inadimplentes"
    ])
    menu.pack(pady=10)

    txt = ctk.CTkTextbox(janela, width=520, height=400)
    txt.pack(pady=10)

    def gerar():

        txt.delete("1.0", "end")
        escolha = menu.get()

        if escolha == "Movimentações (últimos 90 dias)":
            r = fetchall("SELECT * FROM vw_movimentacoes_recentes")

        elif escolha == "Resumo de contas por cliente":
            r = fetchall("SELECT * FROM vw_resumo_contas")

        else:
            r = fetchall("SELECT * FROM conta WHERE saldo < 0")

        if not r:
            txt.insert("end", "Nenhum registro encontrado.")
            return

        for linha in r:
            txt.insert("end", str(linha) + "\n")

    ctk.CTkButton(janela, text="Gerar", command=gerar).pack(pady=10)
    ctk.CTkButton(janela, text="Fechar", command=janela.destroy).pack(pady=4)
