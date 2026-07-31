from backend.models.aparelho import Aparelho
from backend.services.aparelho_service import AparelhoService


def testar_aparelho():
    print("\n=== 1. CADASTRO ===")

    aparelho = Aparelho(
        id_os=3,
        tipo="Celular",
        marca="Samsung",
        modelo="Galaxy S22",
        cor="Preto",
        imei="123456789012345",
        numero_serie="SN123456",
        senha="1234",
        defeito_informado="Aparelho não está carregando.",
        estado_aparelho="Tela riscada e marcas de uso na carcaça."
    )

    cadastrado = AparelhoService.cadastrar(aparelho)

    if not cadastrado:
        print("O teste foi interrompido porque o cadastro falhou.")
        return

    print(f"ID gerado: {aparelho.id_aparelho}")

    print("\n=== 2. BUSCA POR ID ===")

    aparelho_encontrado = AparelhoService.buscar_por_id(
        aparelho.id_aparelho
    )

    print(aparelho_encontrado)

    print("\n=== 3. LISTAGEM GERAL ===")

    aparelhos = AparelhoService.listar()

    for item in aparelhos:
        print(item)

    print("\n=== 4. LISTAGEM POR ORDEM DE SERVIÇO ===")

    aparelhos_da_os = AparelhoService.listar_por_ordem_servico(
        aparelho.id_os
    )

    for item in aparelhos_da_os:
        print(item)

    print("\n=== 5. ATUALIZAÇÃO ===")

    aparelho.modelo = "Galaxy S22 5G"
    aparelho.cor = "Preto fosco"
    aparelho.defeito_informado = "Conector de carga com mau contato."
    aparelho.estado_aparelho = (
        "Tela riscada, carcaça marcada e tampa traseira trincada."
    )

    atualizado = AparelhoService.atualizar(aparelho)

    if atualizado:
        aparelho_atualizado = AparelhoService.buscar_por_id(
            aparelho.id_aparelho
        )

        print(aparelho_atualizado)

    print("\n=== 6. EXCLUSÃO ===")

    excluido = AparelhoService.excluir(aparelho.id_aparelho)

    if excluido:
        resultado = AparelhoService.buscar_por_id(
            aparelho.id_aparelho
        )

        if resultado is None:
            print("Teste concluído: aparelho removido do banco.")
        else:
            print("Erro: o aparelho ainda existe no banco.")


if __name__ == "__main__":
    testar_aparelho()