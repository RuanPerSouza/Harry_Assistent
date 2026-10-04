import customtkinter as ctk
from tkinter import messagebox

from backend.builders.gerador_orcamento import GeradorOrcamento
from backend.services.peca_service import PecaService
from backend.utils.formatadores import formatar_codigo_os, formatar_moeda
from frontend.telas.formulario_peca import FormularioPeca
from frontend.tema import (
    COR_BORDA,
    COR_COMPONENTE,
    COR_COMPONENTE_HOVER,
    COR_ERRO,
    COR_FUNDO,
    COR_PRIMARIA,
    COR_PRIMARIA_HOVER,
    COR_SUCESSO,
    COR_TEXTO_SECUNDARIO,
    FONTE_PADRAO,
    RAIO_COMPONENTE,
)


class JanelaPecasOS(ctk.CTkToplevel):
    """
    Janela modal com as peças vinculadas a uma Ordem de Serviço,
    totais calculados e geração do texto de orçamento.
    """

    def __init__(self, master, id_os, nome_cliente=""):
        super().__init__(master)

        self.id_os = id_os
        self.nome_cliente = nome_cliente

        self.title(f"Peças — {formatar_codigo_os(id_os)}")
        self.geometry("560x680")
        self.resizable(True, True)
        self.minsize(480, 520)
        self.configure(fg_color=COR_FUNDO)

        self.transient(master)

        self.after(10, self.lift)
        self.after(10, self.focus_force)
        self.after(10, self.grab_set)

        self.criar_cabecalho()
        self.criar_lista()
        self.criar_rodape_totais()

        self.carregar_pecas()

    def criar_cabecalho(self):
        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=25, pady=(20, 10))

        label_titulo = ctk.CTkLabel(
            topo,
            text=f"Peças da {formatar_codigo_os(self.id_os)}",
            font=ctk.CTkFont(
                family=FONTE_PADRAO, size=20, weight="bold"
            ),
            anchor="w"
        )
        label_titulo.pack(anchor="w")

        if self.nome_cliente:
            label_subtitulo = ctk.CTkLabel(
                topo,
                text=f"Cliente: {self.nome_cliente}",
                font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
                text_color=COR_TEXTO_SECUNDARIO,
                anchor="w"
            )
            label_subtitulo.pack(anchor="w", pady=(2, 0))

        botao_nova = ctk.CTkButton(
            topo,
            text="+ Nova Peça",
            height=36,
            fg_color=COR_PRIMARIA,
            hover_color=COR_PRIMARIA_HOVER,
            command=self.abrir_nova
        )
        botao_nova.pack(anchor="w", pady=(12, 0))

    def criar_lista(self):
        self.lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.lista.pack(fill="both", expand=True, padx=25, pady=(10, 10))

    def criar_rodape_totais(self):
        self.rodape = ctk.CTkFrame(
            self,
            fg_color=COR_COMPONENTE,
            corner_radius=RAIO_COMPONENTE,
            border_width=1,
            border_color=COR_BORDA
        )
        self.rodape.pack(fill="x", padx=25, pady=(0, 20))

        self.label_total_pecas = ctk.CTkLabel(
            self.rodape,
            text="Total das peças: R$ 0,00",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            text_color=COR_TEXTO_SECUNDARIO,
            anchor="w"
        )
        self.label_total_pecas.pack(anchor="w", padx=18, pady=(14, 0))

        self.label_mao_obra = ctk.CTkLabel(
            self.rodape,
            text="Mão de obra: R$ 0,00",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            text_color=COR_TEXTO_SECUNDARIO,
            anchor="w"
        )
        self.label_mao_obra.pack(anchor="w", padx=18, pady=(2, 0))

        self.label_desconto = ctk.CTkLabel(
            self.rodape,
            text="Desconto: R$ 0,00",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            text_color=COR_TEXTO_SECUNDARIO,
            anchor="w"
        )
        self.label_desconto.pack(anchor="w", padx=18, pady=(2, 0))

        self.label_total_final = ctk.CTkLabel(
            self.rodape,
            text="TOTAL: R$ 0,00",
            font=ctk.CTkFont(
                family=FONTE_PADRAO, size=17, weight="bold"
            ),
            text_color=COR_SUCESSO,
            anchor="w"
        )
        self.label_total_final.pack(anchor="w", padx=18, pady=(6, 14))

        botao_orcamento = ctk.CTkButton(
            self.rodape,
            text="Gerar Orçamento (WhatsApp)",
            height=36,
            fg_color=COR_PRIMARIA,
            hover_color=COR_PRIMARIA_HOVER,
            command=self.gerar_orcamento
        )
        botao_orcamento.pack(fill="x", padx=18, pady=(0, 16))

    def carregar_pecas(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        pecas = PecaService.listar_por_ordem_servico(self.id_os)

        if not pecas:
            label_vazio = ctk.CTkLabel(
                self.lista,
                text="Nenhuma peça cadastrada nesta OS.",
                text_color=COR_TEXTO_SECUNDARIO,
                font=ctk.CTkFont(family=FONTE_PADRAO, size=14)
            )
            label_vazio.pack(pady=30)
        else:
            for peca in pecas:
                self.criar_linha_peca(peca)

        self.atualizar_totais()

    def criar_linha_peca(self, peca):
        linha = ctk.CTkFrame(
            self.lista,
            fg_color=COR_COMPONENTE,
            corner_radius=RAIO_COMPONENTE,
            border_width=1,
            border_color=COR_BORDA
        )
        linha.pack(fill="x", pady=6)

        frame_botoes = ctk.CTkFrame(linha, fg_color="transparent")
        frame_botoes.pack(side="right", padx=14, pady=10)

        botao_excluir = ctk.CTkButton(
            frame_botoes,
            text="Excluir",
            width=75,
            height=30,
            fg_color=COR_COMPONENTE_HOVER,
            hover_color=COR_ERRO,
            command=lambda: self.excluir(peca)
        )
        botao_excluir.pack(side="left")

        botao_editar = ctk.CTkButton(
            frame_botoes,
            text="Editar",
            width=75,
            height=30,
            fg_color=COR_COMPONENTE_HOVER,
            hover_color=COR_PRIMARIA_HOVER,
            command=lambda: self.abrir_edicao(peca)
        )
        botao_editar.pack(side="left", padx=(0, 8))

        info = ctk.CTkFrame(linha, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=14, pady=10)

        label_descricao = ctk.CTkLabel(
            info,
            text=peca["descricao"],
            font=ctk.CTkFont(
                family=FONTE_PADRAO, size=14, weight="bold"
            ),
            anchor="w"
        )
        label_descricao.pack(anchor="w")

        detalhes = (
            f"{peca['quantidade']} × "
            f"{formatar_moeda(peca['valor_unitario'])}  =  "
            f"{formatar_moeda(peca['subtotal'])}"
        )

        label_detalhes = ctk.CTkLabel(
            info,
            text=detalhes,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=12),
            text_color=COR_TEXTO_SECUNDARIO,
            anchor="w"
        )
        label_detalhes.pack(anchor="w", pady=(2, 0))

    def atualizar_totais(self):
        totais = PecaService.calcular_total_ordem_servico(self.id_os)

        if totais is None:
            return

        self.label_total_pecas.configure(
            text=f"Total das peças: {formatar_moeda(totais['total_pecas'])}"
        )
        self.label_mao_obra.configure(
            text=f"Mão de obra: {formatar_moeda(totais['mao_obra'])}"
        )
        self.label_desconto.configure(
            text=f"Desconto: {formatar_moeda(totais['desconto'])}"
        )
        self.label_total_final.configure(
            text=f"TOTAL: {formatar_moeda(totais['total'])}"
        )

    def abrir_nova(self):
        FormularioPeca(self, id_os=self.id_os, ao_salvar=self.carregar_pecas)

    def abrir_edicao(self, peca):
        FormularioPeca(
            self, id_os=self.id_os, ao_salvar=self.carregar_pecas, peca=peca
        )

    def excluir(self, peca):
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir a peça '{peca['descricao']}'?"
        )

        if not confirmar:
            return

        sucesso = PecaService.excluir(peca["id_peca"])

        if not sucesso:
            messagebox.showerror("Erro", "Não foi possível excluir a peça.")
            return

        self.carregar_pecas()

    def gerar_orcamento(self):
        texto = GeradorOrcamento.gerar(self.id_os)

        if texto is None:
            messagebox.showerror(
                "Erro", "Não foi possível gerar o orçamento."
            )
            return

        JanelaOrcamentoGerado(self, texto)


class JanelaOrcamentoGerado(ctk.CTkToplevel):
    """
    Mostra o texto do orçamento gerado, pronto pra copiar e
    colar no WhatsApp.
    """

    def __init__(self, master, texto_orcamento):
        super().__init__(master)

        self.texto_orcamento = texto_orcamento

        self.title("Orçamento Gerado")
        self.geometry("420x520")
        self.resizable(True, True)
        self.minsize(360, 400)
        self.configure(fg_color=COR_FUNDO)

        self.transient(master)

        self.after(10, self.lift)
        self.after(10, self.focus_force)
        self.after(10, self.grab_set)

        caixa_texto = ctk.CTkTextbox(
            self, fg_color=COR_COMPONENTE, font=("Consolas", 12)
        )
        caixa_texto.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        caixa_texto.insert("1.0", texto_orcamento)
        caixa_texto.configure(state="disabled")

        botao_copiar = ctk.CTkButton(
            self,
            text="Copiar texto",
            height=38,
            fg_color=COR_PRIMARIA,
            hover_color=COR_PRIMARIA_HOVER,
            command=self.copiar
        )
        botao_copiar.pack(fill="x", padx=20, pady=(0, 20))

    def copiar(self):
        self.clipboard_clear()
        self.clipboard_append(self.texto_orcamento)