import customtkinter as ctk

from backend.models.cliente import Cliente
from backend.services.cliente_service import ClienteService
from frontend.tema import (
    COR_COMPONENTE,
    COR_ERRO,
    COR_FUNDO,
    COR_PRIMARIA,
    COR_PRIMARIA_HOVER,
    FONTE_PADRAO,
)


class FormularioCliente(ctk.CTkToplevel):
    """
    Janela modal para cadastro ou edição de um cliente.

    Se `cliente` for informado, o formulário abre em modo edição.
    `ao_salvar` é chamado (sem argumentos) após salvar com sucesso,
    para a tela de listagem se atualizar.
    """

    def __init__(self, master, ao_salvar, cliente=None):
        super().__init__(master)

        self.ao_salvar = ao_salvar
        self.cliente = cliente
        self.modo_edicao = cliente is not None

        self.title(
            "Editar Cliente" if self.modo_edicao else "Novo Cliente"
        )
        self.geometry("420x560")
        self.resizable(True, True)
        self.minsize(400, 460)
        self.configure(fg_color=COR_FUNDO)

        # Mantém a janela sempre na frente da principal
        self.transient(master)

        self.after(10, self.lift)
        self.after(10, self.focus_force)
        self.after(10, self.grab_set)

        self.criar_campos()

        if self.modo_edicao:
            self.preencher_campos()

    def criar_campo(self, label_texto, obrigatorio=False):
        texto = f"{label_texto} *" if obrigatorio else label_texto

        label = ctk.CTkLabel(
            self,
            text=texto,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            anchor="w"
        )
        label.pack(fill="x", padx=30, pady=(14, 4))

        entrada = ctk.CTkEntry(
            self,
            height=36,
            fg_color=COR_COMPONENTE
        )
        entrada.pack(fill="x", padx=30)

        return entrada

    def criar_campos(self):
        self.entrada_nome = self.criar_campo("Nome", obrigatorio=True)
        self.entrada_telefone = self.criar_campo(
            "Telefone", obrigatorio=True
        )
        self.entrada_complemento = self.criar_campo("Complemento")
        self.entrada_email = self.criar_campo("E-mail")
        self.entrada_cpf = self.criar_campo("CPF")

        self.label_erro = ctk.CTkLabel(
            self,
            text="",
            text_color=COR_ERRO,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=12)
        )
        self.label_erro.pack(fill="x", padx=30, pady=(10, 0))

        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=30, pady=(20, 20), side="bottom")

        botao_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            command=self.destroy
        )
        botao_cancelar.pack(side="left", expand=True, fill="x", padx=(0, 8))

        botao_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            fg_color=COR_PRIMARIA,
            hover_color=COR_PRIMARIA_HOVER,
            command=self.salvar
        )
        botao_salvar.pack(side="left", expand=True, fill="x", padx=(8, 0))

    def preencher_campos(self):
        self.entrada_nome.insert(0, self.cliente["nome"] or "")
        self.entrada_telefone.insert(0, self.cliente["telefone"] or "")
        self.entrada_complemento.insert(
            0, self.cliente["complemento"] or ""
        )
        self.entrada_email.insert(0, self.cliente["email"] or "")
        self.entrada_cpf.insert(0, self.cliente["cpf"] or "")

    def salvar(self):
        nome = self.entrada_nome.get().strip()
        telefone = self.entrada_telefone.get().strip()
        complemento = self.entrada_complemento.get().strip() or None
        email = self.entrada_email.get().strip() or None
        cpf = self.entrada_cpf.get().strip() or None

        if not nome or not telefone:
            self.label_erro.configure(
                text="Nome e telefone são obrigatórios."
            )
            return

        cliente = Cliente(
            nome=nome,
            telefone=telefone,
            complemento=complemento,
            email=email,
            cpf=cpf
        )

        if self.modo_edicao:
            sucesso = ClienteService.atualizar(
                self.cliente["id_cliente"], cliente
            )
        else:
            sucesso = ClienteService.cadastrar(cliente)

        if not sucesso:
            self.label_erro.configure(
                text="Não foi possível salvar. Tente novamente."
            )
            return

        self.ao_salvar()
        self.destroy()