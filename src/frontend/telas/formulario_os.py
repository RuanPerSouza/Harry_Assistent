from datetime import datetime
from decimal import Decimal, InvalidOperation

import customtkinter as ctk

from backend.models.ordem_servico import OrdemServico
from backend.services.cliente_service import ClienteService
from backend.services.ordem_servico_service import OrdemServicoService
from frontend.tema import (
    COR_COMPONENTE,
    COR_ERRO,
    COR_FUNDO,
    COR_PRIMARIA,
    COR_PRIMARIA_HOVER,
    FONTE_PADRAO,
)


class FormularioOS(ctk.CTkToplevel):
    """
    Janela modal para cadastro ou edição de uma Ordem de Serviço.

    Se `ordem` for informado (dict vindo de OrdemServicoService.listar/
    buscar_por_id), o formulário abre em modo edição.
    `ao_salvar` é chamado após salvar com sucesso, para a tela de
    listagem se atualizar.
    """

    def __init__(self, master, ao_salvar, ordem=None):
        super().__init__(master)

        self.ao_salvar = ao_salvar
        self.ordem = ordem
        self.modo_edicao = ordem is not None

        self.title(
            "Editar Ordem de Serviço"
            if self.modo_edicao
            else "Nova Ordem de Serviço"
        )
        self.geometry("460x700")
        self.resizable(True, True)
        self.minsize(440, 560)
        self.configure(fg_color=COR_FUNDO)

        self.transient(master)
        self.grab_set()

        self.clientes = ClienteService.listar()
        self.mapa_clientes = {
            f"{c['nome']} — {c['telefone']}": c["id_cliente"]
            for c in self.clientes
        }

        self.criar_campos()

        if self.modo_edicao:
            self.preencher_campos()

    def criar_label(self, texto, obrigatorio=False):
        texto_final = f"{texto} *" if obrigatorio else texto

        label = ctk.CTkLabel(
            self,
            text=texto_final,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            anchor="w"
        )
        label.pack(fill="x", padx=30, pady=(12, 4))

    def criar_campos(self):
        self.criar_label("Cliente", obrigatorio=True)
        self.combo_cliente = ctk.CTkComboBox(
            self,
            values=list(self.mapa_clientes.keys()) or ["Nenhum cliente cadastrado"],
            fg_color=COR_COMPONENTE,
            button_color=COR_PRIMARIA,
            button_hover_color=COR_PRIMARIA_HOVER,
            state="readonly"
        )
        self.combo_cliente.pack(fill="x", padx=30)

        self.criar_label("Status")
        self.combo_status = ctk.CTkComboBox(
            self,
            values=list(OrdemServico.STATUS_VALIDOS),
            fg_color=COR_COMPONENTE,
            button_color=COR_PRIMARIA,
            button_hover_color=COR_PRIMARIA_HOVER,
            state="readonly"
        )
        self.combo_status.set("Recebido")
        self.combo_status.pack(fill="x", padx=30)

        self.criar_label("Prioridade")
        self.combo_prioridade = ctk.CTkComboBox(
            self,
            values=list(OrdemServico.PRIORIDADES_VALIDAS),
            fg_color=COR_COMPONENTE,
            button_color=COR_PRIMARIA,
            button_hover_color=COR_PRIMARIA_HOVER,
            state="readonly"
        )
        self.combo_prioridade.set("Média")
        self.combo_prioridade.pack(fill="x", padx=30)

        linha_valores = ctk.CTkFrame(self, fg_color="transparent")
        linha_valores.pack(fill="x", padx=30, pady=(12, 0))
        linha_valores.grid_columnconfigure((0, 1), weight=1)

        label_mao_obra = ctk.CTkLabel(
            linha_valores,
            text="Mão de obra (R$)",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            anchor="w"
        )
        label_mao_obra.grid(row=0, column=0, sticky="w")

        label_desconto = ctk.CTkLabel(
            linha_valores,
            text="Desconto (R$)",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
            anchor="w"
        )
        label_desconto.grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.entrada_mao_obra = ctk.CTkEntry(
            linha_valores, height=36, fg_color=COR_COMPONENTE
        )
        self.entrada_mao_obra.insert(0, "0")
        self.entrada_mao_obra.grid(
            row=1, column=0, sticky="ew", pady=(4, 0)
        )

        self.entrada_desconto = ctk.CTkEntry(
            linha_valores, height=36, fg_color=COR_COMPONENTE
        )
        self.entrada_desconto.insert(0, "0")
        self.entrada_desconto.grid(
            row=1, column=1, sticky="ew", padx=(10, 0), pady=(4, 0)
        )

        self.criar_label("Equipamentos recebidos (carregador, capa...)")
        self.entrada_equipamentos = ctk.CTkEntry(
            self, height=36, fg_color=COR_COMPONENTE
        )
        self.entrada_equipamentos.pack(fill="x", padx=30)

        self.criar_label("Observações")
        self.texto_observacoes = ctk.CTkTextbox(
            self, height=90, fg_color=COR_COMPONENTE
        )
        self.texto_observacoes.pack(fill="x", padx=30)

        self.label_erro = ctk.CTkLabel(
            self,
            text="",
            text_color=COR_ERRO,
            font=ctk.CTkFont(family=FONTE_PADRAO, size=12)
        )
        self.label_erro.pack(fill="x", padx=30, pady=(10, 0))

        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(fill="x", padx=30, pady=(16, 20), side="bottom")

        botao_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            command=self.destroy
        )
        botao_cancelar.pack(side="left", expand=True, fill="x", padx=(0, 8))

        botao_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            fg_color=COR_PRIMARIA,
            hover_color=COR_PRIMARIA_HOVER,
            command=self.salvar
        )
        botao_salvar.pack(side="left", expand=True, fill="x", padx=(8, 0))

    def preencher_campos(self):
        chave_cliente = (
            f"{self.ordem['nome_cliente']} — "
            f"{self.ordem['telefone_cliente']}"
        )

        if chave_cliente not in self.mapa_clientes:
            self.mapa_clientes[chave_cliente] = self.ordem["id_cliente"]
            self.combo_cliente.configure(
                values=list(self.mapa_clientes.keys())
            )

        self.combo_cliente.set(chave_cliente)
        self.combo_status.set(self.ordem["status"])
        self.combo_prioridade.set(self.ordem["prioridade"])

        self.entrada_mao_obra.delete(0, "end")
        self.entrada_mao_obra.insert(0, str(self.ordem["mao_obra"]))

        self.entrada_desconto.delete(0, "end")
        self.entrada_desconto.insert(0, str(self.ordem["desconto"]))

        self.entrada_equipamentos.insert(
            0, self.ordem["equipamentos_recebidos"] or ""
        )

        if self.ordem["observacoes"]:
            self.texto_observacoes.insert("1.0", self.ordem["observacoes"])

    def ler_valor_decimal(self, texto):
        texto = texto.strip().replace(",", ".")

        if not texto:
            return Decimal("0")

        try:
            return Decimal(texto)
        except InvalidOperation:
            return None

    def salvar(self):
        chave_cliente = self.combo_cliente.get()
        id_cliente = self.mapa_clientes.get(chave_cliente)

        if not id_cliente:
            self.label_erro.configure(text="Selecione um cliente válido.")
            return

        mao_obra = self.ler_valor_decimal(self.entrada_mao_obra.get())
        desconto = self.ler_valor_decimal(self.entrada_desconto.get())

        if mao_obra is None or desconto is None:
            self.label_erro.configure(
                text="Mão de obra e desconto devem ser valores numéricos."
            )
            return

        equipamentos = self.entrada_equipamentos.get().strip() or None
        observacoes = (
            self.texto_observacoes.get("1.0", "end").strip() or None
        )

        status_selecionado = self.combo_status.get()

        if self.modo_edicao:
            # Preserva campos não editados nesta tela (pagamento, datas).
            # Marca a conclusão automaticamente ao entregar a OS, pra
            # alimentar o cálculo de receita do Dashboard.
            data_conclusao = self.ordem["data_conclusao"]

            if status_selecionado == "Entregue" and data_conclusao is None:
                data_conclusao = datetime.now()
            elif status_selecionado != "Entregue":
                data_conclusao = None

            ordem = OrdemServico(
                id_os=self.ordem["id_os"],
                id_cliente=id_cliente,
                data_entrada=self.ordem["data_entrada"],
                data_conclusao=data_conclusao,
                status=status_selecionado,
                prioridade=self.combo_prioridade.get(),
                mao_obra=mao_obra,
                desconto=desconto,
                status_pagamento=self.ordem["status_pagamento"],
                forma_pagamento=self.ordem["forma_pagamento"],
                numero_parcelas=self.ordem["numero_parcelas"],
                valor_pago=self.ordem["valor_pago"],
                equipamentos_recebidos=equipamentos,
                observacoes=observacoes,
            )
            sucesso = OrdemServicoService.atualizar(ordem)
        else:
            ordem = OrdemServico(
                id_cliente=id_cliente,
                status=self.combo_status.get(),
                prioridade=self.combo_prioridade.get(),
                mao_obra=mao_obra,
                desconto=desconto,
                equipamentos_recebidos=equipamentos,
                observacoes=observacoes,
            )
            sucesso = OrdemServicoService.cadastrar(ordem)

        if not sucesso:
            self.label_erro.configure(
                text="Não foi possível salvar. Tente novamente."
            )
            return

        self.ao_salvar()
        self.destroy()