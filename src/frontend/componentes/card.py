import customtkinter as ctk

from frontend.tema import (
    COR_BORDA,
    COR_COMPONENTE,
    COR_PRIMARIA,
    COR_TEXTO_SECUNDARIO,
    FONTE_EMOJI,
    FONTE_PADRAO,
    RAIO_COMPONENTE,
    TAMANHO_DESTAQUE,
    TAMANHO_TEXTO,
)


class CardInformacao(ctk.CTkFrame):
    """Card reutilizável para indicadores do Dashboard."""

    def __init__(
        self,
        master,
        titulo,
        valor,
        icone="",
        cor_destaque=COR_PRIMARIA
    ):
        super().__init__(
            master,
            fg_color=COR_COMPONENTE,
            corner_radius=RAIO_COMPONENTE,
            border_width=1,
            border_color=COR_BORDA
        )

        self.grid_columnconfigure(0, weight=1)

        self.label_icone = ctk.CTkLabel(
            self,
            text=icone,
            font=ctk.CTkFont(
                family=FONTE_EMOJI,
                size=26
            )
        )
        self.label_icone.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(18, 5)
        )

        self.label_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=ctk.CTkFont(
                family=FONTE_PADRAO,
                size=TAMANHO_TEXTO
            ),
            text_color=COR_TEXTO_SECUNDARIO
        )
        self.label_titulo.grid(
            row=1,
            column=0,
            sticky="w",
            padx=20
        )

        self.label_valor = ctk.CTkLabel(
            self,
            text=valor,
            font=ctk.CTkFont(
                family=FONTE_PADRAO,
                size=TAMANHO_DESTAQUE,
                weight="bold"
            ),
            text_color=cor_destaque
        )
        self.label_valor.grid(
            row=2,
            column=0,
            sticky="w",
            padx=20,
            pady=(5, 18)
        )

    def atualizar_valor(self, novo_valor):
        self.label_valor.configure(text=str(novo_valor))