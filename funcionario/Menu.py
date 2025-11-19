import customtkinter as ctk
from database.conexao import fetchone, exec_commit


def abrir_app_funcionario(id_usuario):
    # -----------------------------------------------
    # Buscar ID do funcionário + cargo
    # -----------------------------------------------
    r = fetchone("""
        SELECT id_funcionario, cargo
        FROM funcionario
        WHERE id_usuario = %s
    """, (id_usuario,))

    if not r:
        print("Funcionário não encontrado no banco.")
        return

    id_funcionario, cargo = r

    # Registro de sessão SQL (para triggers de auditoria)
    exec_commit("SET @current_funcionario_id = %s", (id_funcionario,))

    # -----------------------------------------------
    # Tela principal
    # -----------------------------------------------
    app = ctk.CTk()
    app.title(f"Banco Malvader - Funcionário ({cargo})")
    app.geometry("520x430")

    ctk.CTkLabel(app, text=f"Bem-vindo, {cargo}", font=("Arial", 22)).pack(pady=10)

    # -----------------------------------------------
    # Funções chamando telas separadas
    # -----------------------------------------------
    def abrir_abrir_conta():
        from funcionario.telas.abrirconta import tela_abrir_conta
        tela_abrir_conta(id_funcionario)

    def abrir_encerrar_conta():
        from funcionario.telas.encerramentoconta import tela_encerrar_conta
        tela_encerrar_conta(id_funcionario)

    def abrir_consulta():
        from funcionario.telas.consulta import tela_consulta
        tela_consulta()

    def abrir_editar():
        from funcionario.telas.editardados import tela_editar
        tela_editar()

    def abrir_cadastro_func():
        if cargo != "GERENTE":
            popup("Acesso negado", "Somente GERENTE pode cadastrar funcionários.")
            return

        from funcionario.telas.cadastro import tela_cadastrar_func
        tela_cadastrar_func(id_funcionario)

    def abrir_relatorios():
        from funcionario.telas.relatorio import tela_relatorios
        tela_relatorios(id_funcionario)

    def popup(titulo, msg):
        p = ctk.CTkToplevel(app)
        p.title(titulo)
        p.geometry("350x200")
        ctk.CTkLabel(p, text=msg, font=("Arial", 16)).pack(pady=20)
        ctk.CTkButton(p, text="OK", command=p.destroy).pack(pady=10)

    # -----------------------------------------------
    # BOTOES DO MENU
    # -----------------------------------------------
    frame = ctk.CTkFrame(app)
    frame.pack(pady=20)

    ctk.CTkButton(frame, text="Abertura de Conta", width=250, command=abrir_abrir_conta).grid(row=0, column=0, pady=5)
    ctk.CTkButton(frame, text="Encerramento de Conta", width=250, command=abrir_encerrar_conta).grid(row=1, column=0, pady=5)
    ctk.CTkButton(frame, text="Consulta de Dados", width=250, command=abrir_consulta).grid(row=2, column=0, pady=5)
    ctk.CTkButton(frame, text="Alteração de Dados", width=250, command=abrir_editar).grid(row=3, column=0, pady=5)
    ctk.CTkButton(frame, text="Cadastro de Funcionário", width=250, command=abrir_cadastro_func).grid(row=4, column=0, pady=5)
    ctk.CTkButton(frame, text="Relatórios", width=250, command=abrir_relatorios).grid(row=5, column=0, pady=5)

    ctk.CTkButton(app, text="Logout", fg_color="red", command=app.destroy).pack(pady=12)

    app.mainloop()
