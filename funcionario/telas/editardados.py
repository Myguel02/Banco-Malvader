import customtkinter as ctk
from database.conexao import exec_commit


def tela_editar():

    janela = ctk.CTkToplevel()
    janela.title("Alteração de Dados")
    janela.geometry("420x430")

    ctk.CTkLabel(janela, text="Alterar Dados", font=("Arial", 20)).pack(pady=10)

    entry_cpf = ctk.CTkEntry(janela, placeholder_text="CPF")
    entry_cpf.pack(pady=6)

    entry_novo = ctk.CTkEntry(janela, placeholder_text="Novo telefone/endereço")
    entry_novo.pack(pady=6)

    tipo = ctk.CTkOptionMenu(janela, values=["telefone", "endereco"])
    tipo.pack(pady=6)

    lbl = ctk.CTkLabel(janela, text="")
    lbl.pack(pady=10)

    def salvar():
        cpf = entry_cpf.get().strip()
        novo = entry_novo.get().strip()
        campo = tipo.get()

        if campo == "telefone":
            exec_commit("UPDATE usuario SET telefone=%s WHERE cpf=%s", (novo, cpf))
        else:
            exec_commit("UPDATE endereco_usuario SET local=%s WHERE id_usuario=(SELECT id_usuario FROM usuario WHERE cpf=%s)", (novo, cpf))

        lbl.configure(text="Alterado com sucesso!", text_color="green")

    ctk.CTkButton(janela, text="Salvar", command=salvar).pack(pady=10)
    ctk.CTkButton(janela, text="Fechar", command=janela.destroy).pack(pady=4)
