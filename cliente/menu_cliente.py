import customtkinter as ctk
from database.conexao import fetchone, fetchall, exec_commit
from utils.helpers import format_currency


def abrir_app_cliente(id_cliente):
    app = ctk.CTk()
    app.title("Banco Malvader - Área do Cliente")
    app.geometry("520x460")

    ctk.CTkLabel(app, text="Área do Cliente", font=("Arial", 22)).pack(pady=10)

    # Popup
    def popup(titulo, msg):
        p = ctk.CTkToplevel(app)
        p.title(titulo)
        p.geometry("380x240")
        ctk.CTkLabel(p, text=msg, font=("Arial", 15)).pack(pady=25)
        ctk.CTkButton(p, text="OK", command=p.destroy).pack(pady=10)

    def get_id_conta():
        r = fetchone("SELECT id_conta FROM conta WHERE id_cliente=%s", (id_cliente,))
        return r[0] if r else None

    # SALDO
    def consultar_saldo():
        r = fetchone("""
            SELECT saldo, tipo_conta, status 
            FROM conta 
            WHERE id_cliente=%s
        """, (id_cliente,))
        
        if r:
            saldo, tipo, status = r
            msg = f"Conta: {tipo}\nStatus: {status}\nSaldo Atual: {format_currency(saldo)}"
        else:
            msg = "Nenhuma conta encontrada!"

        popup("Saldo", msg)

    # DEPÓSITO
    def deposito():
        win = ctk.CTkToplevel(app)
        win.title("Depósito")
        win.geometry("300x220")

        ctk.CTkLabel(win, text="Valor do depósito:").pack(pady=10)
        entry_valor = ctk.CTkEntry(win)
        entry_valor.pack(pady=5)

        def confirmar():
            try:
                valor = float(entry_valor.get())
                if valor <= 0:
                    raise ValueError()

                id_conta = get_id_conta()

                ok, erro = exec_commit("""
                    INSERT INTO transacao (id_conta_destino, tipo_transacao, valor, descricao)
                    VALUES (%s, 'DEPOSITO', %s, 'DEPÓSITO APP')
                """, (id_conta, valor))

                if ok:
                    popup("Depósito", "Depósito realizado!")
                    win.destroy()
                else:
                    popup("Erro", erro)
            except:
                popup("Erro", "Valor inválido!")

        ctk.CTkButton(win, text="Confirmar", command=confirmar).pack(pady=10)

    # SAQUE
    def saque():
        win = ctk.CTkToplevel(app)
        win.title("Saque")
        win.geometry("300x220")

        ctk.CTkLabel(win, text="Valor do saque:").pack(pady=10)
        entry_valor = ctk.CTkEntry(win)
        entry_valor.pack(pady=5)

        def confirmar():
            try:
                valor = float(entry_valor.get())
                if valor <= 0:
                    raise ValueError()

                id_conta = get_id_conta()

                ok, erro = exec_commit("""
                    INSERT INTO transacao (id_conta_origem, tipo_transacao, valor, descricao)
                    VALUES (%s, 'SAQUE', %s, 'SAQUE APP')
                """, (id_conta, valor))

                if ok:
                    popup("Saque", "Saque realizado!")
                    win.destroy()
                else:
                    popup("Erro", erro)
            except:
                popup("Erro", "Valor inválido!")

        ctk.CTkButton(win, text="Confirmar", command=confirmar).pack(pady=10)

    # TRANSFERÊNCIA
    def transferencia():
        win = ctk.CTkToplevel(app)
        win.title("Transferência")
        win.geometry("320x270")

        ctk.CTkLabel(win, text="Conta destino:").pack(pady=5)
        entry_dest = ctk.CTkEntry(win)
        entry_dest.pack(pady=5)

        ctk.CTkLabel(win, text="Valor:").pack(pady=5)
        entry_valor = ctk.CTkEntry(win)
        entry_valor.pack(pady=5)

        def confirmar():
            try:
                dest = entry_dest.get().strip()
                valor = float(entry_valor.get())

                if valor <= 0:
                    raise ValueError()

                id_origem = get_id_conta()

                r = fetchone("SELECT id_conta FROM conta WHERE numero_conta=%s", (dest,))
                if not r:
                    popup("Erro", "Conta destino não encontrada!")
                    return

                id_dest = r[0]

                ok, erro = exec_commit("""
                    INSERT INTO transacao (id_conta_origem, id_conta_destino, tipo_transacao, valor, descricao)
                    VALUES (%s, %s, 'TRANSFERENCIA', %s, 'TRANSFER APP')
                """, (id_origem, id_dest, valor))

                if ok:
                    popup("Transferência", "Transferência realizada!")
                    win.destroy()
                else:
                    popup("Erro", erro)

            except:
                popup("Erro", "Entrada inválida!")

        ctk.CTkButton(win, text="Confirmar", command=confirmar).pack(pady=10)

    # EXTRATO
    def extrato():
        id_conta = get_id_conta()

        r = fetchall("""
            SELECT tipo_transacao, valor, data_hora
            FROM transacao
            WHERE id_conta_origem=%s OR id_conta_destino=%s
            ORDER BY data_hora DESC
            LIMIT 10
        """, (id_conta, id_conta))

        if not r:
            popup("Extrato", "Nenhuma transação encontrada!")
            return

        texto = "\n".join([f"{t[0]} | {format_currency(t[1])} | {t[2]}" for t in r])

        popup("Extrato (Últimas 10)", texto)

    # LIMITE
    def consultar_limite():
        r = fetchone("""
            SELECT cc.limite 
            FROM conta_corrente cc
            JOIN conta c ON cc.id_conta = c.id_conta
            WHERE c.id_cliente=%s
        """, (id_cliente,))

        if r:
            limite = r[0]
            popup("Limite", f"Limite disponível: {format_currency(limite)}")
        else:
            popup("Limite", "Conta não é corrente ou não possui limite.")

    # BOTÕES
    frame = ctk.CTkFrame(app)
    frame.pack(pady=15)

    ctk.CTkButton(frame, text="Consultar Saldo", width=220, command=consultar_saldo).grid(row=0, column=0, pady=6)
    ctk.CTkButton(frame, text="Depósito", width=220, command=deposito).grid(row=1, column=0, pady=6)
    ctk.CTkButton(frame, text="Saque", width=220, command=saque).grid(row=2, column=0, pady=6)
    ctk.CTkButton(frame, text="Transferência", width=220, command=transferencia).grid(row=3, column=0, pady=6)
    ctk.CTkButton(frame, text="Extrato", width=220, command=extrato).grid(row=4, column=0, pady=6)
    ctk.CTkButton(frame, text="Consultar Limite", width=220, command=consultar_limite).grid(row=5, column=0, pady=6)

    ctk.CTkButton(app, text="Sair", fg_color="red", command=app.destroy).pack(pady=10)

    app.mainloop()
