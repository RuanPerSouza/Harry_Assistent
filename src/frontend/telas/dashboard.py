import customtkinter as ctk


class DashboardFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, corner_radius=0)

        titulo = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        titulo.pack(
            anchor="w",
            padx=30,
            pady=(30, 8)
        )

        subtitulo = ctk.CTkLabel(
            self,
            text="Visão geral da assistência técnica",
            font=ctk.CTkFont(size=15)
        )
        subtitulo.pack(
            anchor="w",
            padx=30
        )

        mensagem = ctk.CTkLabel(
            self,
            text="Bem-vindo ao Harry_Assistent!",
            font=ctk.CTkFont(size=20)
        )
        mensagem.pack(
            expand=True
        )
        