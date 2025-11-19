import importlib
import customtkinter as ctk
from database.conexao import fetchone, exec_commit

def _safe_import(module_path: str, attr_name: str):
    """
    Tenta importar attr_name de module_path.
    Retorna a função/objeto ou None e a mensagem de erro.
    """
    try:
        mod = importlib.import_module(module_path)
        if not hasattr(mod, attr_name):
            return None, f"O módulo '{module_path}' foi encontrado, mas não contém '{attr_name}'."
        return getattr(mod, attr_name), None
    except Exception as e:
        return None, f"Falha ao importar '{module_path}': {e}"

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
    # Funções chamando telas separadas (robustas)
    # -----------------------------------------------
    def abrir_abrir_conta():
        fn, err = _safe_import("funcionario.telas.abrirconta", "tela_abrir_conta")
        if err:
            popup("Erro", err); return
        fn(id_funcionario)

    def abrir_encerrar_conta():
        fn, err = _safe_import("funcionario.telas.encerramentoconta", "tela_encerrar_conta")
        if err:
            popup("Erro", err); return
        fn(id_funcionario)

    def abrir_consulta():
        fn, err = _safe_import("funcionario.telas.consulta", "tela_consulta")
        if err:
            popup("Erro", err); return
        fn()

    def abrir_editar():
        fn, err = _safe_import("funcionario.telas.editardados", "tela_editar_dados")
        if err:
            popup("Erro", err); return
        fn()

    def abrir_cadastro_func():
        if cargo != "GERENTE":
            popup("Acesso negado", "Somente GERENTE pode cadastrar funcionários.")
            return

        fn, err = _safe_import("funcionario.telas.cadastro", "tela_cadastrar_func")
        if err:
            popup("Erro", err); return
        fn(id_funcionario)

    def abrir_relatorios():
        fn, err = _safe_import("funcionario.telas.relatorio", "tela_relatorios")
        if err:
            popup("Erro", err); return
        fn(id_funcionario)

    def popup(titulo, mensagem):
        p = ctk.CTkToplevel(app)
        p.title(titulo)
        p.geometry("360x180")
        ctk.CTkLabel(p, text=mensagem, font=("Arial", 14), wraplength=320).pack(pady=16)
        ctk.CTkButton(p, text="OK", command=p.destroy).pack(pady=6)

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
