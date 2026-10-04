from datetime import datetime

import customtkinter as ctk

from backend.services.dashboard_service import DashboardService
from backend.utils.formatadores import formatar_moeda
from frontend.componentes.cabecalho import Cabecalho
from frontend.componentes.card import CardInformacao
from frontend.componentes.painel_status import PainelStatus


class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            corner_radius=0
        )

        # Permite que o conteúdo ocupe toda a largura
        self.grid_columnconfigure(0, weight=1)

        Cabecalho(
            self,
            titulo="Dashboard",
            subtitulo="Visão geral da assistência técnica"
        )

        self.criar_saudacao()
        self.criar_cards()
        self.criar_painel_status()

        self.atualizar_indicadores()

    def criar_saudacao(self):
        hora = datetime.now().hour

        if hora < 12:
            saudacao = "Bom dia"
            icone = "☀️"

        elif hora < 18:
            saudacao = "Boa tarde"
            icone = "🌤️"

        else:
            saudacao = "Boa noite"
            icone = "🌙"

        self.label_saudacao = ctk.CTkLabel(
            self,
            text=f"{saudacao}, Ruan! {icone}",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=20,
                weight="bold"
            )
        )

        self.label_saudacao.pack(
            anchor="w",
            padx=30,
            pady=(0, 18)
        )

    def criar_cards(self):
        self.frame_cards = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.frame_cards.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        for coluna in range(3):
            self.frame_cards.grid_columnconfigure(
                coluna,
                weight=1,
                uniform="cards"
            )

        self.card_ordens = CardInformacao(
            self.frame_cards,
            titulo="OS em andamento",
            valor="0",
            icone="📋",
            cor_destaque="#2563EB"
        )

        self.card_ordens.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        self.card_clientes = CardInformacao(
            self.frame_cards,
            titulo="Clientes cadastrados",
            valor="0",
            icone="👤",
            cor_destaque="#22C55E"
        )

        self.card_clientes.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=8
        )

        self.card_receita = CardInformacao(
            self.frame_cards,
            titulo="Receita do mês",
            valor="R$ 0,00",
            icone="💰",
            cor_destaque="#F59E0B"
        )

        self.card_receita.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(8, 0)
        )

    def criar_painel_status(self):
        self.painel_status = PainelStatus(
            self,
            mensagem=(
                "O sistema está funcionando normalmente. "
                "Nenhuma Ordem de Serviço precisa de atenção."
            ),
            tipo="sucesso"
        )

        self.painel_status.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

    def atualizar_indicadores(self):
        indicadores = DashboardService.obter_indicadores()

        self.card_ordens.atualizar_valor(
            str(indicadores["os_em_andamento"])
        )
        self.card_clientes.atualizar_valor(
            str(indicadores["clientes_cadastrados"])
        )
        self.card_receita.atualizar_valor(
            formatar_moeda(indicadores["receita_mes"])
        )

        if indicadores["os_em_andamento"] > 0:
            self.painel_status.atualizar_mensagem(
                mensagem=(
                    f"Você tem {indicadores['os_em_andamento']} "
                    f"Ordem(ns) de Serviço em andamento."
                ),
                tipo="atencao"
            )