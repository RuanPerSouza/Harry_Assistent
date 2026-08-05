import customtkinter as ctk


class HarryAssistentApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Harry_Assistent")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        self.criar_layout()

    def criar_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )
        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.menu_lateral.grid_propagate(False)

        self.conteudo = ctk.CTkFrame(
            self,
            corner_radius=0
        )
        self.conteudo.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.criar_menu()
        self.criar_tela_inicial()

    def criar_menu(self):
        titulo = ctk.CTkLabel(
            self.menu_lateral,
            text="Harry_Assistent",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )
        titulo.pack(pady=(30, 40))

        botoes = (
            "Dashboard",
            "Clientes",
            "Ordens de Serviço",
            "Aparelhos",
            "Peças",
            "Financeiro",
            "Configurações",
        )

        for texto in botoes:
            botao = ctk.CTkButton(
                self.menu_lateral,
                text=texto,
                anchor="w",
                height=42
            )
            botao.pack(
                fill="x",
                padx=20,
                pady=6
            )

    def criar_tela_inicial(self):
        titulo = ctk.CTkLabel(
            self.conteudo,
            text="Dashboard",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )
        titulo.pack(
            anchor="w",
            padx=30,
            pady=(30, 10)
        )

        subtitulo = ctk.CTkLabel(
            self.conteudo,
            text="Visão geral da assistência técnica",
            font=ctk.CTkFont(size=15)
        )
        subtitulo.pack(
            anchor="w",
            padx=30
        )


if __name__ == "__main__":
    app = HarryAssistentApp()
    app.mainloop()