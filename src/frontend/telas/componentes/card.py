import customtkinter as ctk


class CardInformacao(ctk.CTkFrame):
    """
    Card reutilizável para exibir indicadores no Dashboard.

    Exemplo:
        CardInformacao(
            master,
            titulo="OS em andamento",
            valor="12",
            icone="📋"
        )
    """

    def __init__(
        self,
        master,
        titulo,
        valor,
        icone="",
        cor_destaque="#2563EB"
    ):
        super().__init__(
            master,
            corner_radius=12,
            border_width=1,
            border_color="#3A3A3A"
        )

        self.grid_columnconfigure(0, weight=1)

        self.label_icone = ctk.CTkLabel(
            self,
            text=icone,
            font=ctk.CTkFont(
                family="Segoe UI Emoji",
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
                family="Segoe UI",
                size=14
            ),
            text_color="gray70"
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
                family="Segoe UI",
                size=27,
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
        """Atualiza o valor exibido no card."""

        self.label_valor.configure(text=str(novo_valor))