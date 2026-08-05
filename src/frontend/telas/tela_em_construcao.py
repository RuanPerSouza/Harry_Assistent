import customtkinter as ctk


class TelaEmConstrucao(ctk.CTkFrame):

    def __init__(self, master, titulo):
        super().__init__(master, corner_radius=0)

        label_titulo = ctk.CTkLabel(
            self,
            text=titulo,
            font=ctk.CTkFont(size=28, weight="bold")
        )
        label_titulo.pack(
            anchor="w",
            padx=30,
            pady=(30, 8)
        )

        mensagem = ctk.CTkLabel(
            self,
            text="Tela em desenvolvimento.",
            font=ctk.CTkFont(size=18)
        )
        mensagem.pack(expand=True)