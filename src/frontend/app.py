import customtkinter as ctk

from frontend.telas.dashboard import DashboardFrame
from frontend.telas.tela_em_construcao import TelaEmConstrucao


class HarryAssistentApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Harry_Assistent")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        self.tela_atual = None

        self.criar_layout()
        self.mostrar_dashboard()

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

        self.area_conteudo = ctk.CTkFrame(
            self,
            corner_radius=0
        )
        self.area_conteudo.grid(
            row=0,
            column=1,
            sticky="nsew"
        )
        self.area_conteudo.grid_columnconfigure(0, weight=1)
        self.area_conteudo.grid_rowconfigure(0, weight=1)

        self.criar_menu()

    def criar_menu(self):
        titulo = ctk.CTkLabel(
            self.menu_lateral,
            text="Harry Assistent",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )
        titulo.pack(pady=(30, 40))

        botoes = (
            ("Dashboard", self.mostrar_dashboard),
            ("Clientes", lambda: self.mostrar_tela_generica("Clientes")),
            (
                "Ordens de Serviço",
                lambda: self.mostrar_tela_generica("Ordens de Serviço")
            ),
            ("Aparelhos", lambda: self.mostrar_tela_generica("Aparelhos")),
            ("Peças", lambda: self.mostrar_tela_generica("Peças")),
            ("Financeiro", lambda: self.mostrar_tela_generica("Financeiro")),
            (
                "Configurações",
                lambda: self.mostrar_tela_generica("Configurações")
            ),
        )

        for texto, comando in botoes:
            botao = ctk.CTkButton(
                self.menu_lateral,
                text=texto,
                command=comando,
                anchor="w",
                height=42
            )
            botao.pack(
                fill="x",
                padx=20,
                pady=6
            )

    def trocar_tela(self, nova_tela):
        if self.tela_atual is not None:
            self.tela_atual.destroy()

        self.tela_atual = nova_tela
        self.tela_atual.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    def mostrar_dashboard(self):
        self.trocar_tela(
            DashboardFrame(self.area_conteudo)
        )

    def mostrar_tela_generica(self, titulo):
        self.trocar_tela(
            TelaEmConstrucao(
                self.area_conteudo,
                titulo
            )
        )


if __name__ == "__main__":
    app = HarryAssistentApp()
    app.mainloop()