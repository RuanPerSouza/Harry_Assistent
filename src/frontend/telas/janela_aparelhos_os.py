import customtkinter as ctk
from tkinter import messagebox

from backend.services.aparelho_service import AparelhoService
from backend.utils.formatadores import formatar_codigo_os
from frontend.telas.formulario_aparelho import FormularioAparelho
from frontend.tema import (
    COR_BORDA,
    COR_COMPONENTE,
    COR_COMPONENTE_HOVER,
    COR_ERRO,
    COR_FUNDO,
    COR_PRIMARIA,
    COR_PRIMARIA_HOVER,
    COR_TEXTO_SECUNDARIO,
    FONTE_PADRAO,
    RAIO_COMPONENTE,
)


class JanelaAparelhosOS(ctk.CTkToplevel):
    """
    Janela modal com os aparelhos vinculados a uma Ordem de Serviço.
    """

    def __init__(self, master, id_os, nome_cliente=""):
        super().__init__(master)

        self.id_os = id_os

        self.title(f"Aparelhos — {formatar_codigo_os(id_os)}")
        self.geometry("520x560")
        self.configure(fg_color=COR_FUNDO)

        self.transient(master)

        # Garante que a janela apareça na frente no Windows,
        # mesmo quando o CTkToplevel nasce atrás da janela principal.
        self.after(10, self.lift)
        self.after(10, self.focus_force)
        self.after(10, self.grab_set)

        self.criar_cabecalho(nome_cliente)
        self.criar_lista()

        self.carregar_aparelhos()

    def criar_cabecalho(self, nome_cliente):
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=25, pady=(20, 10))

        subtitulo = (
            f"Cliente: {nome_cliente}" if nome_cliente else ""
        )

        label_titulo = ctk.CTkLabel(
            topo,
            text=f"Aparelhos da {formatar_codigo_os(self.id_os)}",
            font=ctk.CTkFont(
                family=FONTE_PADRAO, size=20, weight="bold"
            ),
            anchor="w"
        )
        label_titulo.pack(anchor="w")

        if subtitulo:
            label_subtitulo = ctk.CTkLabel(
                topo,
                text=subtitulo,
                font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
                text_color=COR_TEXTO_SECUNDARIO,
                anchor="w"
            )
            label_subtitulo.pack(anchor="w", pady=(2, 0))

        botao_novo = ctk.CTkButton(
            topo,
            text="+ Novo Aparelho",
            height=36,
            fg_color=COR_PRIMARIA,
            hover_color=COR_PRIMARIA_HOVER,
            command=self.abrir_novo
        )
        botao_novo.pack(anchor="w", pady=(12, 0))

    def criar_lista(self):
        self.lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.lista.pack(fill="both", expand=True, padx=25, pady=(10, 20))

    def carregar_aparelhos(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        aparelhos = AparelhoService.listar_por_ordem_servico(self.id_os)

        if not aparelhos:
            label_vazio = ctk.CTkLabel(
                self.lista,
                text="Nenhum aparelho cadastrado nesta OS.",
                text_color=COR_TEXTO_SECUNDARIO,
                font=ctk.CTkFont(family=FONTE_PADRAO, size=14)
            )
            label_vazio.pack(pady=30)
            return

        for aparelho in aparelhos:
            self.criar_linha_aparelho(aparelho)

    def criar_linha_aparelho(self, aparelho):
        linha = ctk.CTkFrame(
            self.lista,
            fg_color=COR_COMPONENTE,
            corner_radius=RAIO_COMPONENTE,
            border_width=1,
            border_color=COR_BORDA
        )
        linha.pack(fill="x", pady=6)

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(fill="x", padx=18, pady=12)

        titulo = f"{aparelho['tipo']} — {aparelho['marca']} {aparelho['modelo']}"
        if aparelho["cor"]:
            titulo += f" ({aparelho['cor']})"

        label_titulo = ctk.CTkLabel(
            info,
            text=titulo,
            font=ctk.CTkFont(
                family=FONTE_PADRAO, size=14, weight="bold"
            ),
            anchor="w"
        )
        label_titulo.pack(anchor="w")

        label_defeito = ctk.CTkLabel(
            info,
            text=f"Defeito: {aparelho['defeito_informado']}",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=12),
            text_color=COR_TEXTO_SECUNDARIO,
            anchor="w",
            wraplength=360,
            justify="left"
        )
        label_defeito.pack(anchor="w", pady=(4, 0))

        if aparelho["imei"]:
            label_imei = ctk.CTkLabel(
                info,
                text=f"IMEI: {aparelho['imei']}",
                font=ctk.CTkFont(family=FONTE_PADRAO, size=12),
                text_color=COR_TEXTO_SECUNDARIO,
                anchor="w"
            )
            label_imei.pack(anchor="w", pady=(2, 0))

        frame_botoes = ctk.CTkFrame(linha, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=18, pady=(0, 12))

        botao_editar = ctk.CTkButton(
            frame_botoes,
            text="Editar",
            width=80,
            height=30,
            fg_color=COR_COMPONENTE_HOVER,
            hover_color=COR_PRIMARIA_HOVER,
            command=lambda: self.abrir_edicao(aparelho)
        )
        botao_editar.pack(side="left", padx=(0, 8))

        botao_excluir = ctk.CTkButton(
            frame_botoes,
            text="Excluir",
            width=80,
            height=30,
            fg_color=COR_COMPONENTE_HOVER,
            hover_color=COR_ERRO,
            command=lambda: self.excluir(aparelho)
        )
        botao_excluir.pack(side="left")

    def abrir_novo(self):
        FormularioAparelho(
            self, id_os=self.id_os, ao_salvar=self.carregar_aparelhos
        )

    def abrir_edicao(self, aparelho):
        FormularioAparelho(
            self,
            id_os=self.id_os,
            ao_salvar=self.carregar_aparelhos,
            aparelho=aparelho
        )

    def excluir(self, aparelho):
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir este aparelho "
            f"({aparelho['marca']} {aparelho['modelo']})?"
        )

        if not confirmar:
            return

        sucesso = AparelhoService.excluir(aparelho["id_aparelho"])

        if not sucesso:
            messagebox.showerror(
                "Erro", "Não foi possível excluir o aparelho."
            )
            return

        self.carregar_aparelhos()