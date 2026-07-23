from backend.repositories.ordem_servico_repository import (
    buscar_ordem_servico_por_id,
    atualizar_ordem_servico
)

from backend.models.ordem_servico import OrdemServico


def main():

    dados = buscar_ordem_servico_por_id(1)

    ordem = OrdemServico(
        id_os=dados["id_os"],
        id_cliente=dados["id_cliente"],
        data_entrada=dados["data_entrada"],
        data_conclusao=dados["data_conclusao"],
        status="Em reparo",
        prioridade=dados["prioridade"],
        mao_obra=dados["mao_obra"],
        desconto=dados["desconto"],
        status_pagamento=dados["status_pagamento"],
        forma_pagamento=dados["forma_pagamento"],
        numero_parcelas=dados["numero_parcelas"],
        valor_pago=dados["valor_pago"],
        equipamentos_recebidos=dados["equipamentos_recebidos"],
        observacoes="Teste de atualização"
    )

    atualizar_ordem_servico(ordem)


if __name__ == "__main__":
    main()