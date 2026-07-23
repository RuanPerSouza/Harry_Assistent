from decimal import Decimal


class OrdemServico:

    STATUS_VALIDOS = (
        "Recebido",
        "Na bancada",
        "Aguardando peça",
        "Em reparo",
        "Reparo concluído",
        "Entregue",
        "Cancelado",
    )

    PRIORIDADES_VALIDAS = (
        "Baixa",
        "Média",
        "Alta",
        "Urgente",
    )

    STATUS_PAGAMENTO_VALIDOS = (
        "Aguardando pagamento",
        "Parcial",
        "Pago",
        "Isento",
    )

    FORMAS_PAGAMENTO_VALIDAS = (
        "Dinheiro",
        "PIX",
        "Cartão de débito",
        "Cartão de crédito",
        "Outro",
    )

    def __init__(
        self,
        id_cliente,
        status="Recebido",
        prioridade="Média",
        mao_obra=0,
        desconto=0,
        status_pagamento="Aguardando pagamento",
        forma_pagamento=None,
        numero_parcelas=1,
        valor_pago=0,
        equipamentos_recebidos=None,
        observacoes=None,
        id_os=None,
        data_entrada=None,
        data_conclusao=None,
    ):
        self.id_os = id_os
        self.id_cliente = id_cliente
        self.data_entrada = data_entrada
        self.data_conclusao = data_conclusao
        self.status = status
        self.prioridade = prioridade
        self.mao_obra = Decimal(str(mao_obra))
        self.desconto = Decimal(str(desconto))
        self.status_pagamento = status_pagamento
        self.forma_pagamento = forma_pagamento
        self.numero_parcelas = numero_parcelas
        self.valor_pago = Decimal(str(valor_pago))
        self.equipamentos_recebidos = equipamentos_recebidos
        self.observacoes = observacoes