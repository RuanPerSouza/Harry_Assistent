from backend.repositories.ordem_servico_repository import (
    buscar_ordem_servico_por_id,
    excluir_ordem_servico,
)


def main():
    id_os = 1

    ordem = buscar_ordem_servico_por_id(id_os)

    if ordem is None:
        print("Ordem de Serviço não encontrada.")
        return

    print(f"OS encontrada: {ordem['id_os']:06d}")
    print(f"Cliente: {ordem['nome_cliente']}")

    confirmar = input("Deseja realmente excluir esta OS? [s/n]: ").strip().lower()

    if confirmar == "s":
        excluir_ordem_servico(id_os)
    else:
        print("Exclusão cancelada.")


if __name__ == "__main__":
    main()