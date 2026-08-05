import customtkinter as ctk

from frontend.telas.dashboard import DashboardFrame
from frontend.telas.tela_em_construcao import TelaEmConstrucao
from frontend.tema import (
    COR_FUNDO,
    COR_MENU_LATERAL,
    COR_PRIMARIA,
    COR_PRIMARIA_HOVER,
    LARGURA_MENU,
)


class HarryAssistentApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Harry Assistent")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        self.configure(fg_color=COR_FUNDO)

        self.tela_atual = None
        self.botoes_menu = {}

        self.criar_layout()
        self.mostrar_dashboard()

    def criar_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=LARGURA_MENU,
            corner_radius=0,
            fg_color=COR_MENU_LATERAL
        )
        self.menu_lateral.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.menu_lateral.grid_propagate(False)

        self.area_conteudo = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=COR_FUNDO
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
                family="Segoe UI",
                size=22,
                weight="bold"
            )
        )
        titulo.pack(
            pady=(30, 40)
        )

        botoes = (
            (
                "Dashboard",
                self.mostrar_dashboard
            ),
            (
                "Clientes",
                lambda: self.mostrar_tela_generica(
                    "Clientes"
                )
            ),
            (
                "Ordens de Serviço",
                lambda: self.mostrar_tela_generica(
                    "Ordens de Serviço"
                )
            ),
            (
                "Aparelhos",
                lambda: self.mostrar_tela_generica(
                    "Aparelhos"
                )
            ),
            (
                "Peças",
                lambda: self.mostrar_tela_generica(
                    "Peças"
                )
            ),
            (
                "Financeiro",
                lambda: self.mostrar_tela_generica(
                    "Financeiro"
                )
            ),
            (
                "Configurações",
                lambda: self.mostrar_tela_generica(
                    "Configurações"
                )
            ),
        )

        for texto, comando in botoes:
            botao = ctk.CTkButton(
                self.menu_lateral,
                text=texto,
                command=lambda t=texto, c=comando: (
                    self.selecionar_botao(t),
                    c()
                ),
                anchor="w",
                height=42,
                fg_color="transparent",
                hover_color=COR_PRIMARIA_HOVER,
                border_spacing=10
            )

            botao.pack(
                fill="x",
                padx=20,
                pady=6
            )

            self.botoes_menu[texto] = botao

    def selecionar_botao(self, nome_botao):
        for nome, botao in self.botoes_menu.items():
            if nome == nome_botao:
                botao.configure(
                    fg_color=COR_PRIMARIA
                )
            else:
                botao.configure(
                    fg_color="transparent"
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
        self.selecionar_botao("Dashboard")

        self.trocar_tela(
            DashboardFrame(
                self.area_conteudo
            )
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