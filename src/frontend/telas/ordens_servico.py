import customtkinter as ctk
from tkinter import messagebox

from backend.services.ordem_servico_service import OrdemServicoService
from backend.utils.formatadores import formatar_codigo_os, formatar_moeda
from frontend.componentes.cabecalho import Cabecalho
from frontend.telas.formulario_os import FormularioOS
from frontend.tema import (
    COR_ATENCAO,
    COR_BORDA,
    COR_COMPONENTE,
    COR_COMPONENTE_HOVER,
    COR_ERRO,
    COR_INFORMACAO,
    COR_PRIMARIA,
    COR_PRIMARIA_HOVER,
    COR_SUCESSO,
    COR_TEXTO_SECUNDARIO,
    FONTE_PADRAO,
    RAIO_COMPONENTE,
)

CORES_STATUS = {
    "Recebido": COR_INFORMACAO,
    "Na bancada": COR_INFORMACAO,
    "Aguardando peça": COR_ATENCAO,
    "Em reparo": COR_ATENCAO,
    "Reparo concluído": COR_SUCESSO,
    "Entregue": COR_SUCESSO,
    "Cancelado": COR_ERRO,
}

CORES_PRIORIDADE = {
    "Baixa": COR_TEXTO_SECUNDARIO,
    "Média": COR_INFORMACAO,
    "Alta": COR_ATENCAO,
    "Urgente": COR_ERRO,
}


class OrdensServicoFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, corner_radius=0)

        Cabecalho(
            self,
            titulo="Ordens de Serviço",
            subtitulo="Acompanhamento dos reparos em andamento"
        )

        self.criar_barra_acoes()
        self.criar_lista()

        self.carregar_ordens()

    def criar_barra_acoes(self):
        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(fill="x", padx=30, pady=(0, 15))
        barra.grid_columnconfigure(0, weight=1)

        self.entrada_busca = ctk.CTkEntry(
            barra,
            placeholder_text="Buscar por cliente ou nº da OS...",
            height=38,
            fg_color=COR_COMPONENTE
        )
        self.entrada_busca.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entrada_busca.bind(
            "<KeyRelease>", lambda e: self.carregar_ordens()
        )

        botao_nova = ctk.CTkButton(
            barra,
            text="+ Nova OS",
            height=38,
            fg_color=COR_PRIMARIA,
            hover_color=COR_PRIMARIA_HOVER,
            command=self.abrir_nova
        )
        botao_nova.grid(row=0, column=1)

    def criar_lista(self):
        self.lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.lista.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    def carregar_ordens(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        ordens = OrdemServicoService.listar()

        termo = self.entrada_busca.get().strip().lower()
        if termo:
            ordens = [
                o for o in ordens
                if termo in o["nome_cliente"].lower()
                or termo in str(o["id_os"])
            ]

        if not ordens:
            label_vazio = ctk.CTkLabel(
                self.lista,
                text="Nenhuma Ordem de Serviço encontrada.",
                text_color=COR_TEXTO_SECUNDARIO,
                font=ctk.CTkFont(family=FONTE_PADRAO, size=14)
            )
            label_vazio.pack(pady=30)
            return

        for ordem in ordens:
            self.criar_linha_os(ordem)

    def criar_badge(self, master, texto, cor):
        badge = ctk.CTkLabel(
            master,
            text=texto,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"),
            text_color=cor,
            fg_color="transparent"
        )
        return badge

    def criar_linha_os(self, ordem):
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
            command=lambda: self.excluir(ordem)
        )
        botao_excluir.pack(side="left")

        botao_editar = ctk.CTkButton(
            frame_botoes,
            text="Editar",
            width=80,
            height=32,
            fg_color=COR_COMPONENTE_HOVER,
            hover_color=COR_PRIMARIA_HOVER,
            command=lambda: self.abrir_edicao(ordem)
        )
        botao_editar.pack(side="left", padx=(0, 8))

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=20, pady=14)

        linha_topo = ctk.CTkFrame(info, fg_color="transparent")
        linha_topo.pack(anchor="w", fill="x")

        label_codigo = ctk.CTkLabel(
            linha_topo,
            text=formatar_codigo_os(ordem["id_os"]),
            font=ctk.CTkFont(
                family=FONTE_PADRAO, size=15, weight="bold"
            )
        )
        label_codigo.pack(side="left")

        label_cliente = ctk.CTkLabel(
            linha_topo,
            text=f"  •  {ordem['nome_cliente']}",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=15)
        )
        label_cliente.pack(side="left")

        linha_badges = ctk.CTkFrame(info, fg_color="transparent")
        linha_badges.pack(anchor="w", pady=(4, 0))

        self.criar_badge(
            linha_badges,
            f"● {ordem['status']}",
            CORES_STATUS.get(ordem["status"], COR_TEXTO_SECUNDARIO)
        ).pack(side="left", padx=(0, 14))

        self.criar_badge(
            linha_badges,
            ordem["prioridade"],
            CORES_PRIORIDADE.get(
                ordem["prioridade"], COR_TEXTO_SECUNDARIO
            )
        ).pack(side="left", padx=(0, 14))

        label_valor = ctk.CTkLabel(
            linha_badges,
            text=f"Mão de obra: {formatar_moeda(ordem['mao_obra'])}",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=12),
            text_color=COR_TEXTO_SECUNDARIO
        )
        label_valor.pack(side="left")

    def abrir_nova(self):
        FormularioOS(self, ao_salvar=self.carregar_ordens)

    def abrir_edicao(self, ordem):
        FormularioOS(
            self, ao_salvar=self.carregar_ordens, ordem=ordem
        )

    def excluir(self, ordem):
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir a "
            f"{formatar_codigo_os(ordem['id_os'])}?\n\n"
            f"Isso também excluirá os aparelhos e peças vinculados."
        )

        if not confirmar:
            return

        sucesso = OrdemServicoService.excluir(ordem["id_os"])

        if not sucesso:
            messagebox.showerror(
                "Erro", "Não foi possível excluir a Ordem de Serviço."
            )
            return

        self.carregar_ordens()