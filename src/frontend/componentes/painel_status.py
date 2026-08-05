import customtkinter as ctk

from frontend.tema import (
    COR_ATENCAO,
    COR_COMPONENTE,
    COR_ERRO,
    COR_INFORMACAO,
    COR_SUCESSO,
    FONTE_EMOJI,
    FONTE_PADRAO,
    RAIO_COMPONENTE,
    TAMANHO_TEXTO,
)


class PainelStatus(ctk.CTkFrame):
    """Painel para mensagens e avisos apresentados pelo Harry."""

    CORES = {
        "informacao": COR_INFORMACAO,
        "sucesso": COR_SUCESSO,
        "atencao": COR_ATENCAO,
        "erro": COR_ERRO
    }

    def __init__(
        self,
        master,
        mensagem="Tudo certo por aqui.",
        tipo="informacao"
    ):
        self.cor_destaque = self.CORES.get(
            tipo,
            COR_INFORMACAO
        )

        super().__init__(
            master,
            fg_color=COR_COMPONENTE,
            corner_radius=RAIO_COMPONENTE,
            border_width=1,
            border_color=self.cor_destaque
        )

        self.grid_columnconfigure(1, weight=1)

        self.label_icone = ctk.CTkLabel(
            self,
            text="🔧",
            font=ctk.CTkFont(
                family=FONTE_EMOJI,
                size=30
            )
        )
        self.label_icone.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=(20, 14),
            pady=18
        )

        self.label_titulo = ctk.CTkLabel(
            self,
            text="Harry diz:",
            font=ctk.CTkFont(
                family=FONTE_PADRAO,
                size=17,
                weight="bold"
            ),
            text_color=self.cor_destaque
        )
        self.label_titulo.grid(
            row=0,
            column=1,
            sticky="sw",
            padx=(0, 20),
            pady=(16, 0)
        )

        self.label_mensagem = ctk.CTkLabel(
            self,
            text=mensagem,
            font=ctk.CTkFont(
                family=FONTE_PADRAO,
                size=TAMANHO_TEXTO
            ),
            justify="left",
            anchor="w",
            wraplength=650
        )
        self.label_mensagem.grid(
            row=1,
            column=1,
            sticky="nw",
            padx=(0, 20),
            pady=(4, 16)
        )

    def atualizar_mensagem(
        self,
        mensagem,
        tipo="informacao"
    ):
        cor = self.CORES.get(
            tipo,
            COR_INFORMACAO
        )

        self.configure(border_color=cor)
        self.label_titulo.configure(text_color=cor)
        self.label_mensagem.configure(text=mensagem)