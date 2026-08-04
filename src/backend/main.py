from backend.builders.gerador_orcamento import GeradorOrcamento
from backend.models.peca import Peca
from backend.services.peca_service import PecaService


def main():
    id_os = 3

    print("\n=== CADASTRO DAS PEÇAS ===")

    tela = Peca(
        id_os=id_os,
        descricao="Tela OLED Samsung Galaxy S22",
        quantidade=1,
        valor_unitario=850
    )

    conectores = Peca(
        id_os=id_os,
        descricao="Conector USB-C",
        quantidade=2,
        valor_unitario=25
    )

    cadastrou_tela = PecaService.cadastrar(tela)
    cadastrou_conectores = PecaService.cadastrar(conectores)

    if not cadastrou_tela or not cadastrou_conectores:
        print("Não foi possível cadastrar todas as peças.")
        return

    print(f"Peça 1 criada com ID: {tela.id_peca}")
    print(f"Peça 2 criada com ID: {conectores.id_peca}")

    print("\n=== ORÇAMENTO GERADO ===")

    orcamento = GeradorOrcamento.gerar(id_os)

    if orcamento is None:
        print("Não foi possível gerar o orçamento.")
        return

    print(orcamento)

    print("\n=== CONFERÊNCIA DOS VALORES ===")

    totais = PecaService.calcular_total_ordem_servico(id_os)

    if totais is None:
        print("Não foi possível calcular os totais.")
        return

    print(f"Total das peças: {totais['total_pecas']}")
    print(f"Mão de obra: {totais['mao_obra']}")
    print(f"Desconto: {totais['desconto']}")
    print(f"Total final: {totais['total']}")

    print("\n=== LIMPEZA DOS DADOS DE TESTE ===")

    PecaService.excluir(tela.id_peca)
    PecaService.excluir(conectores.id_peca)


if __name__ == "__main__":
    main()