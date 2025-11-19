import customtkinter as ctk
from database.conexao import fetchall, fetchone


def tela_consulta():

    janela = ctk.CTkToplevel()
    janela.title("Consulta de Dados")
    janela.geometry("520x600")

    ctk.CTkLabel(janela, text="Consulta de Dados", font=("Arial", 22)).pack(pady=10)

    opcoes = ["Conta", "Funcionário", "Cliente"]
    menu = ctk.CTkOptionMenu(janela, values=opcoes)
    menu.pack(pady=6)

    entry_busca = ctk.CTkEntry(janela, placeholder_text="CPF ou Número da conta")
    entry_busca.pack(pady=6)

    txt = ctk.CTkTextbox(janela, width=480, height=350)
    txt.pack(pady=10)

    def consultar():

        escolha = menu.get()
        valor = entry_busca.get().strip()

        txt.delete("1.0", "end")

        if escolha == "Conta":
            r = fetchall("""
                SELECT numero_conta, saldo, tipo_conta, status 
                FROM conta 
                WHERE numero_conta=%s
            """, (valor,))
        elif escolha == "Cliente":
            r = fetchall("""
                SELECT u.nome, u.cpf, c.score_credito
                FROM usuario u
                JOIN cliente c ON c.id_usuario = u.id_usuario
                WHERE u.cpf=%s
            """, (valor,))
        else:
            r = fetchall("""
                SELECT u.nome, u.cpf, f.cargo, f.codigo_funcionario
                FROM usuario u
                JOIN funcionario f ON f.id_usuario = u.id_usuario
                WHERE u.cpf=%s
            """, (valor,))

        if not r:
            txt.insert("end", "Nenhum dado encontrado.")
            return

        for row in r:
            txt.insert("end", str(row) + "\n")

    ctk.CTkButton(janela, text="Consultar", command=consultar).pack(pady=6)
    ctk.CTkButton(janela, text="Fechar", command=janela.destroy).pack(pady=4)
