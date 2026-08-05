import customtkinter as ctk


class PainelStatus(ctk.CTkFrame):
    """
    Painel reutilizável para exibir avisos e mensagens do sistema.
    """

    def __init__(
        self,
        master,
        mensagem="Tudo certo por aqui.",
        tipo="informacao"
    ):
        cores = {
            "informacao": "#2563EB",
            "sucesso": "#22C55E",
            "atencao": "#F59E0B",
            "erro": "#EF4444"
        }

        cor_destaque = cores.get(
            tipo,
            cores["informacao"]
        )

        super().__init__(
            master,
            corner_radius=12,
            border_width=1,
            border_color=cor_destaque
        )

        self.grid_columnconfigure(1, weight=1)

        self.label_icone = ctk.CTkLabel(
            self,
            text="🔧",
            font=ctk.CTkFont(
                family="Segoe UI Emoji",
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
                family="Segoe UI",
                size=17,
                weight="bold"
            ),
            text_color=cor_destaque
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
                family="Segoe UI",
                size=14
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
        cores = {
            "informacao": "#2563EB",
            "sucesso": "#22C55E",
            "atencao": "#F59E0B",
            "erro": "#EF4444"
        }

        cor_destaque = cores.get(
            tipo,
            cores["informacao"]
        )

        self.configure(
            border_color=cor_destaque
        )
        self.label_titulo.configure(
            text_color=cor_destaque
        )
        self.label_mensagem.configure(
            text=mensagem
        )