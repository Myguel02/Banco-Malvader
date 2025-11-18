import customtkinter as ctk
from decimal import Decimal, InvalidOperation

from database.db_conta import obter_contas_do_cliente, buscar_conta_por_numero
from database.db_transacao import inserir_transacao


class TelaDeposito(ctk.CTkToplevel):
    
    def __init__(self, id_cliente):
        super().__init__()

        self.id_cliente = id_cliente

        self.title("Depósito - Banco Malvader")
        self.geometry("500x420")

        ctk.set_appearance_mode("dark")

        titulo = ctk.CTkLabel(self, text="Depósito", font=("Arial", 22))
        titulo.pack(pady=15)

        # ---------- SELEÇÃO CONTA DESTINO ----------
        ctk.CTkLabel(self, text="Selecione a conta destino").pack(pady=5)

        self.combo_contas = ctk.CTkComboBox(self, width=300, values=[])
        self.combo_contas.pack(pady=5)

        self.atualizar_contas()

        # ---------- VALOR ----------
        ctk.CTkLabel(self, text="Valor do depósito").pack(pady=(20, 5))
        self.entry_valor = ctk.CTkEntry(self, placeholder_text="Ex: 100.00", width=200)
        self.entry_valor.pack(pady=5)

        # ---------- BOTÃO ----------
        self.lbl_msg = ctk.CTkLabel(self, text="")
        self.lbl_msg.pack(pady=10)

        btn = ctk.CTkButton(self, text="Depositar", command=self.realizar_deposito)
        btn.pack(pady=20)

    # -----------------------------------------------------
    def atualizar_contas(self):
        contas = obter_contas_do_cliente(self.id_cliente)
        
        if not contas:
            self.combo_contas.configure(values=["Nenhuma conta encontrada"])
            return
        
        lista_fmt = []
        for idc, numero, saldo, tipo in contas:
            lista_fmt.append(f"{idc} | {numero} | {tipo} | Saldo: {saldo}")
        
        self.combo_contas.configure(values=lista_fmt)

    # -----------------------------------------------------
    def realizar_deposito(self):
        selecionado = self.combo_contas.get()

        if "|" not in selecionado:
            self.lbl_msg.configure(text="Selecione uma conta válida.", text_color="red")
            return

        id_conta = int(selecionado.split("|")[0].strip())

        # Valor
        try:
            valor = Decimal(self.entry_valor.get().strip())
            if valor <= 0:
                raise InvalidOperation()
        except:
            self.lbl_msg.configure(text="Valor inválido.", text_color="red")
            return

        # Inserir transação
        ok, err = inserir_transacao(
            tipo="DEPOSITO",
            valor=valor,
            id_conta_origem=None,
            id_conta_destino=id_conta,
            descricao=f"Depósito realizado pelo cliente {self.id_cliente}"
        )

        if ok:
            self.lbl_msg.configure(text="Depósito realizado com sucesso!", text_color="green")
            self.entry_valor.delete(0, "end")
            self.atualizar_contas()
        else:
            self.lbl_msg.configure(text=f"Erro: {err}", text_color="red")
