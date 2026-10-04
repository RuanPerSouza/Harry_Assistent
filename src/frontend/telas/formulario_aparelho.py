import customtkinter as ctk

from backend.models.aparelho import Aparelho
from backend.services.aparelho_service import AparelhoService
from frontend.tema import (
    COR_COMPONENTE,
    COR_ERRO,
    COR_FUNDO,
    COR_PRIMARIA,
    COR_PRIMARIA_HOVER,
    FONTE_PADRAO,
)

TIPOS_APARELHO = ("Celular", "Notebook")


class FormularioAparelho(ctk.CTkToplevel):
    """
    Janela modal para cadastro ou edição de um aparelho vinculado
    a uma Ordem de Serviço específica (id_os).

    Se `aparelho` for informado (dict vindo de AparelhoService), o
    formulário abre em modo edição.
    """

    def __init__(self, master, id_os, ao_salvar, aparelho=None):
        super().__init__(master)

        self.id_os = id_os
        self.ao_salvar = ao_salvar
        self.aparelho = aparelho
        self.modo_edicao = aparelho is not None

        self.title(
            "Editar Aparelho" if self.modo_edicao else "Novo Aparelho"
        )
        self.geometry("440x780")
        self.resizable(True, True)
        self.minsize(420, 560)
        self.configure(fg_color=COR_FUNDO)

        self.transient(master)

        self.after(10, self.lift)
        self.after(10, self.focus_force)
        self.after(10, self.grab_set)

        self.criar_campos()

        if self.modo_edicao:
            self.preencher_campos()

    def criar_campo_label(self, texto, obrigatorio=False):
        texto_final = f"{texto} *" if obrigatorio else texto

        label = ctk.CTkLabel(
            self,
            text=texto_final,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            anchor="w"
        )
        label.pack(fill="x", padx=30, pady=(12, 4))

    def criar_campo_entry(self):
        entrada = ctk.CTkEntry(self, height=36, fg_color=COR_COMPONENTE)
        entrada.pack(fill="x", padx=30)
        return entrada

    def criar_campos(self):
        self.criar_campo_label("Tipo", obrigatorio=True)
        self.combo_tipo = ctk.CTkComboBox(
            self,
            values=list(TIPOS_APARELHO),
            fg_color=COR_COMPONENTE,
            button_color=COR_PRIMARIA,
            button_hover_color=COR_PRIMARIA_HOVER,
            state="readonly"
        )
        self.combo_tipo.set("Celular")
        self.combo_tipo.pack(fill="x", padx=30)

        self.criar_campo_label("Marca", obrigatorio=True)
        self.entrada_marca = self.criar_campo_entry()

        self.criar_campo_label("Modelo", obrigatorio=True)
        self.entrada_modelo = self.criar_campo_entry()

        self.criar_campo_label("Cor")
        self.entrada_cor = self.criar_campo_entry()

        linha_identificadores = ctk.CTkFrame(self, fg_color="transparent")
        linha_identificadores.pack(fill="x", padx=30, pady=(12, 0))
        linha_identificadores.grid_columnconfigure((0, 1), weight=1)

        label_imei = ctk.CTkLabel(
            linha_identificadores,
            text="IMEI",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            anchor="w"
        )
        label_imei.grid(row=0, column=0, sticky="w")

        label_serie = ctk.CTkLabel(
            linha_identificadores,
            text="Nº de série",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            anchor="w"
        )
        label_serie.grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.entrada_imei = ctk.CTkEntry(
            linha_identificadores, height=36, fg_color=COR_COMPONENTE
        )
        self.entrada_imei.grid(row=1, column=0, sticky="ew", pady=(4, 0))

        self.entrada_numero_serie = ctk.CTkEntry(
            linha_identificadores, height=36, fg_color=COR_COMPONENTE
        )
        self.entrada_numero_serie.grid(
            row=1, column=1, sticky="ew", padx=(10, 0), pady=(4, 0)
        )

        self.criar_campo_label("Senha / padrão de desbloqueio")
        self.entrada_senha = self.criar_campo_entry()

        self.criar_campo_label("Defeito informado", obrigatorio=True)
        self.texto_defeito = ctk.CTkTextbox(
            self, height=70, fg_color=COR_COMPONENTE
        )
        self.texto_defeito.pack(fill="x", padx=30)

        self.criar_campo_label("Estado do aparelho")
        self.texto_estado = ctk.CTkTextbox(
            self, height=60, fg_color=COR_COMPONENTE
        )
        self.texto_estado.pack(fill="x", padx=30)

        self.label_erro = ctk.CTkLabel(
            self,
            text="",
            text_color=COR_ERRO,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=12)
        )
        self.label_erro.pack(fill="x", padx=30, pady=(10, 0))

        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=30, pady=(16, 20), side="bottom")

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
        self.combo_tipo.set(self.aparelho["tipo"])
        self.entrada_marca.insert(0, self.aparelho["marca"])
        self.entrada_modelo.insert(0, self.aparelho["modelo"])
        self.entrada_cor.insert(0, self.aparelho["cor"] or "")
        self.entrada_imei.insert(0, self.aparelho["imei"] or "")
        self.entrada_numero_serie.insert(
            0, self.aparelho["numero_serie"] or ""
        )
        self.entrada_senha.insert(0, self.aparelho["senha"] or "")

        if self.aparelho["defeito_informado"]:
            self.texto_defeito.insert(
                "1.0", self.aparelho["defeito_informado"]
            )

        if self.aparelho["estado_aparelho"]:
            self.texto_estado.insert(
                "1.0", self.aparelho["estado_aparelho"]
            )

    def salvar(self):
        marca = self.entrada_marca.get().strip()
        modelo = self.entrada_modelo.get().strip()
        defeito = self.texto_defeito.get("1.0", "end").strip()

        if not marca or not modelo or not defeito:
            self.label_erro.configure(
                text="Marca, modelo e defeito informado são obrigatórios."
            )
            return

        aparelho = Aparelho(
            id_os=self.id_os,
            tipo=self.combo_tipo.get(),
            marca=marca,
            modelo=modelo,
            cor=self.entrada_cor.get().strip() or None,
            imei=self.entrada_imei.get().strip() or None,
            numero_serie=self.entrada_numero_serie.get().strip() or None,
            senha=self.entrada_senha.get().strip() or None,
            defeito_informado=defeito,
            estado_aparelho=(
                self.texto_estado.get("1.0", "end").strip() or None
            ),
        )

        if self.modo_edicao:
            aparelho.id_aparelho = self.aparelho["id_aparelho"]
            sucesso = AparelhoService.atualizar(aparelho)
        else:
            sucesso = AparelhoService.cadastrar(aparelho)

        if not sucesso:
            self.label_erro.configure(
                text="Não foi possível salvar. Tente novamente."
            )
            return

        self.ao_salvar()
        self.destroy()