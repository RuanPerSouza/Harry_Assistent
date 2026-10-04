import customtkinter as ctk
from tkinter import messagebox

from backend.services.cliente_service import ClienteService
from frontend.componentes.cabecalho import Cabecalho
from frontend.telas.formulario_cliente import FormularioCliente
from frontend.tema import (
    COR_BORDA,
    COR_COMPONENTE,
    COR_COMPONENTE_HOVER,
    COR_ERRO,
    COR_PRIMARIA,
    COR_PRIMARIA_HOVER,
    COR_TEXTO_SECUNDARIO,
    FONTE_PADRAO,
    RAIO_COMPONENTE,
)


class ClientesFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, corner_radius=0)

        Cabecalho(
            self,
            titulo="Clientes",
            subtitulo="Cadastro e consulta de clientes"
        )

        self.criar_barra_acoes()
        self.criar_lista()

        self.carregar_clientes()

    def criar_barra_acoes(self):
        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(fill="x", padx=30, pady=(0, 15))
        barra.grid_columnconfigure(0, weight=1)

        self.entrada_busca = ctk.CTkEntry(
            barra,
            placeholder_text="Buscar por nome ou telefone...",
            height=38,
            fg_color=COR_COMPONENTE
        )
        self.entrada_busca.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entrada_busca.bind(
            "<KeyRelease>", lambda e: self.carregar_clientes()
        )

        botao_novo = ctk.CTkButton(
            barra,
            text="+ Novo Cliente",
            height=38,
            fg_color=COR_PRIMARIA,
            hover_color=COR_PRIMARIA_HOVER,
            command=self.abrir_novo
        )
        botao_novo.grid(row=0, column=1)

    def criar_lista(self):
        self.lista = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.lista.pack(
            fill="both", expand=True, padx=30, pady=(0, 20)
        )

    def carregar_clientes(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        clientes = ClienteService.listar()

        termo = self.entrada_busca.get().strip().lower()
        if termo:
            clientes = [
                c for c in clientes
                if termo in c["nome"].lower()
                or termo in c["telefone"].lower()
            ]

        if not clientes:
            label_vazio = ctk.CTkLabel(
                self.lista,
                text="Nenhum cliente encontrado.",
                text_color=COR_TEXTO_SECUNDARIO,
                font=ctk.CTkFont(family=FONTE_PADRAO, size=14)
            )
            label_vazio.pack(pady=30)
            return

        for cliente in clientes:
            self.criar_linha_cliente(cliente)

    def criar_linha_cliente(self, cliente):
        linha = ctk.CTkFrame(
            self.lista,
            fg_color=COR_COMPONENTE,
            corner_radius=RAIO_COMPONENTE,
            border_width=1,
            border_color=COR_BORDA
        )
        linha.pack(fill="x", pady=6)

        frame_botoes = ctk.CTkFrame(linha, fg_color="transparent")
        frame_botoes.pack(side="right", padx=20, pady=14)

        botao_excluir = ctk.CTkButton(
            frame_botoes,
            text="Excluir",
            width=80,
            height=32,
            fg_color=COR_COMPONENTE_HOVER,
            hover_color=COR_ERRO,
            command=lambda: self.excluir(cliente)
        )
        botao_excluir.pack(side="left")

        botao_editar = ctk.CTkButton(
            frame_botoes,
            text="Editar",
            width=80,
            height=32,
            fg_color=COR_COMPONENTE_HOVER,
            hover_color=COR_PRIMARIA_HOVER,
            command=lambda: self.abrir_edicao(cliente)
        )
        botao_editar.pack(side="left", padx=(0, 8))

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=20, pady=14)

        label_nome = ctk.CTkLabel(
            info,
            text=cliente["nome"],
            font=ctk.CTkFont(
                family=FONTE_PADRAO, size=15, weight="bold"
            ),
            anchor="w"
        )
        label_nome.pack(anchor="w")

        detalhes = cliente["telefone"]
        if cliente["email"]:
            detalhes += f"  •  {cliente['email']}"

        label_detalhes = ctk.CTkLabel(
            info,
            text=detalhes,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            text_color=COR_TEXTO_SECUNDARIO,
            anchor="w"
        )
        label_detalhes.pack(anchor="w", pady=(2, 0))

    def abrir_novo(self):
        FormularioCliente(
            self,
            ao_salvar=self.carregar_clientes
        )

    def abrir_edicao(self, cliente):
        FormularioCliente(
            self,
            ao_salvar=self.carregar_clientes,
            cliente=cliente
        )

    def excluir(self, cliente):
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir o cliente '{cliente['nome']}'?"
        )

        if not confirmar:
            return

        sucesso = ClienteService.excluir(cliente["id_cliente"])

        if not sucesso:
            messagebox.showerror(
                "Erro",
                "Não foi possível excluir. Verifique se o cliente "
                "possui Ordens de Serviço vinculadas."
            )
            return

        self.carregar_clientes()