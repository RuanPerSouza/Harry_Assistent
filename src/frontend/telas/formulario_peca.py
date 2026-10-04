from decimal import Decimal, InvalidOperation

import customtkinter as ctk

from backend.models.peca import Peca
from backend.services.peca_service import PecaService
from frontend.tema import (
    COR_COMPONENTE,
    COR_ERRO,
    COR_FUNDO,
    COR_PRIMARIA,
    COR_PRIMARIA_HOVER,
    FONTE_PADRAO,
)


class FormularioPeca(ctk.CTkToplevel):
    """
    Janela modal para cadastro ou edição de uma peça vinculada
    a uma Ordem de Serviço específica (id_os).
    """

    def __init__(self, master, id_os, ao_salvar, peca=None):
        super().__init__(master)

        self.id_os = id_os
        self.ao_salvar = ao_salvar
        self.peca = peca
        self.modo_edicao = peca is not None

        self.title("Editar Peça" if self.modo_edicao else "Nova Peça")
        self.geometry("380x420")
        self.resizable(True, True)
        self.minsize(360, 380)
        self.configure(fg_color=COR_FUNDO)

        self.transient(master)

        self.after(10, self.lift)
        self.after(10, self.focus_force)
        self.after(10, self.grab_set)

        self.criar_campos()

        if self.modo_edicao:
            self.preencher_campos()

    def criar_label(self, texto, obrigatorio=False):
        texto_final = f"{texto} *" if obrigatorio else texto

        label = ctk.CTkLabel(
            self,
            text=texto_final,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            anchor="w"
        )
        label.pack(fill="x", padx=25, pady=(14, 4))

    def criar_campos(self):
        self.criar_label("Descrição", obrigatorio=True)
        self.entrada_descricao = ctk.CTkEntry(
            self, height=36, fg_color=COR_COMPONENTE
        )
        self.entrada_descricao.pack(fill="x", padx=25)

        linha_valores = ctk.CTkFrame(self, fg_color="transparent")
        linha_valores.pack(fill="x", padx=25, pady=(14, 0))
        linha_valores.grid_columnconfigure((0, 1), weight=1)

        label_qtd = ctk.CTkLabel(
            linha_valores,
            text="Quantidade *",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            anchor="w"
        )
        label_qtd.grid(row=0, column=0, sticky="w")

        label_valor = ctk.CTkLabel(
            linha_valores,
            text="Valor unitário (R$) *",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            anchor="w"
        )
        label_valor.grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.entrada_quantidade = ctk.CTkEntry(
            linha_valores, height=36, fg_color=COR_COMPONENTE
        )
        self.entrada_quantidade.insert(0, "1")
        self.entrada_quantidade.grid(
            row=1, column=0, sticky="ew", pady=(4, 0)
        )

        self.entrada_valor_unitario = ctk.CTkEntry(
            linha_valores, height=36, fg_color=COR_COMPONENTE
        )
        self.entrada_valor_unitario.grid(
            row=1, column=1, sticky="ew", padx=(10, 0), pady=(4, 0)
        )

        self.label_erro = ctk.CTkLabel(
            self,
            text="",
            text_color=COR_ERRO,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=12)
        )
        self.label_erro.pack(fill="x", padx=25, pady=(12, 0))

        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=25, pady=(16, 20), side="bottom")

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
        self.entrada_descricao.insert(0, self.peca["descricao"])

        self.entrada_quantidade.delete(0, "end")
        self.entrada_quantidade.insert(0, str(self.peca["quantidade"]))

        self.entrada_valor_unitario.insert(
            0, str(self.peca["valor_unitario"])
        )

    def salvar(self):
        descricao = self.entrada_descricao.get().strip()

        if not descricao:
            self.label_erro.configure(text="Informe a descrição da peça.")
            return

        try:
            quantidade = int(self.entrada_quantidade.get().strip())
            if quantidade <= 0:
                raise ValueError
        except ValueError:
            self.label_erro.configure(
                text="Quantidade deve ser um número inteiro maior que zero."
            )
            return

        texto_valor = (
            self.entrada_valor_unitario.get().strip().replace(",", ".")
        )

        try:
            valor_unitario = Decimal(texto_valor)
            if valor_unitario <= 0:
                raise InvalidOperation
        except InvalidOperation:
            self.label_erro.configure(
                text="Valor unitário deve ser um número maior que zero."
            )
            return

        peca = Peca(
            id_os=self.id_os,
            descricao=descricao,
            valor_unitario=valor_unitario,
            quantidade=quantidade
        )

        if self.modo_edicao:
            peca.id_peca = self.peca["id_peca"]
            sucesso = PecaService.atualizar(peca)
        else:
            sucesso = PecaService.cadastrar(peca)

        if not sucesso:
            self.label_erro.configure(
                text="Não foi possível salvar. Tente novamente."
            )
            return

        self.ao_salvar()
        self.destroy()