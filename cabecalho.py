import customtkinter as ctk


class Cabecalho(ctk.CTkFrame):
    """
    Componente reutilizável para o cabeçalho das telas.

    Exemplo de uso:

        Cabecalho(
            self,
            titulo="Dashboard",
            subtitulo="Visão geral da assistência técnica"
        )
    """

    def __init__(
        self,
        master,
        titulo,
        subtitulo=""
    ):
        super().__init__(
            master,
            fg_color="transparent"
        )

        # O componente ocupa toda a largura disponível
        self.pack(
            fill="x",
            padx=30,
            pady=(25, 20)
        )

        # ----------------------------
        # Título
        # ----------------------------

        self.label_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=ctk.CTkFont(
                family="Segoe UI",
                size=28,
                weight="bold"
            )
        )

        self.label_titulo.pack(
            anchor="w"
        )

        # ----------------------------
        # Subtítulo (opcional)
        # ----------------------------

        if subtitulo:

            self.label_subtitulo = ctk.CTkLabel(
                self,
                text=subtitulo,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=15
                ),
                text_color="gray70"
            )

            self.label_subtitulo.pack(
                anchor="w",
                pady=(4, 0)
            )