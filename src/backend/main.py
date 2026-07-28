from datetime import datetime

from backend.models.ordem_servico import OrdemServico
from backend.services.ordem_servico_service import OrdemServicoService


def main():
    ordem = OrdemServico(
        id_cliente=1,
        data_entrada=datetime.now(),
        status="Recebido",
        prioridade="Média",
        mao_obra=100.00,
        desconto=0,
        status_pagamento="Aguardando pagamento",
        forma_pagamento=None,
        numero_parcelas=1,
        valor_pago=0,
        equipamentos_recebidos="Celular Samsung",
        observacoes="Aparelho não liga."
    )

    cadastrado = OrdemServicoService.cadastrar(ordem)

    if not cadastrado:
        print("Não foi possível cadastrar a Ordem de Serviço.")
        return

    print(f"ID gerado: {ordem.id_os}")

    ordem_encontrada = OrdemServicoService.buscar_por_id(ordem.id_os)

    if ordem_encontrada is None:
        print("A Ordem de Serviço foi cadastrada, mas não foi encontrada.")
        return

    print("\nOrdem de Serviço encontrada:")
    print(f"OS: {ordem_encontrada['id_os']:06d}")
    print(f"Cliente: {ordem_encontrada['nome_cliente']}")
    print(f"Status: {ordem_encontrada['status']}")
    print(f"Prioridade: {ordem_encontrada['prioridade']}")
    print(f"Mão de obra: R$ {ordem_encontrada['mao_obra']:.2f}")


if __name__ == "__main__":
    main()