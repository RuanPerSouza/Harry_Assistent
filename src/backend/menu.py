from backend.repositories.cliente_repository import buscar_cliente_por_id


from backend.models.cliente import Cliente
from backend.repositories.cliente_repository import (
    cadastrar_cliente,
    listar_clientes,
    buscar_cliente_por_id,
    atualizar_cliente,
    excluir_cliente
)


def ler_id_cliente():
    try:
        return int(input("Digite o ID do cliente: "))
    except ValueError:
        print("\nID inválido. Digite apenas números.")
        return None


def cadastrar():
    print("\n=== CADASTRAR CLIENTE ===")

    nome = input("Nome: ").strip()
    telefone = input("Telefone: ").strip()
    complemento = input("Complemento: ").strip() or None
    email = input("E-mail: ").strip() or None
    cpf = input("CPF: ").strip() or None

    if not nome or not telefone:
        print("\nNome e telefone são obrigatórios.")
        return

    cliente = Cliente(
        nome=nome,
        telefone=telefone,
        complemento=complemento,
        email=email,
        cpf=cpf
    )

    sucesso = cadastrar_cliente(cliente)

    if sucesso:
        print("\nCliente cadastrado com sucesso!")
    else:
        print("\nNão foi possível cadastrar o cliente.")


def listar():
    print("\n=== LISTA DE CLIENTES ===")

    clientes = listar_clientes()

    if not clientes:
        print("Nenhum cliente cadastrado.")
        return

    for cliente in clientes:
        print("-" * 40)
        print(f"ID: {cliente['id_cliente']}")
        print(f"Nome: {cliente['nome']}")
        print(f"Telefone: {cliente['telefone']}")
        print(f"E-mail: {cliente['email'] or 'Não informado'}")

    print("-" * 40)


def buscar():
    print("\n=== BUSCAR CLIENTE ===")

    id_cliente = ler_id_cliente()

    if id_cliente is None:
        return

    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        print("\nCliente não encontrado.")
        return

    print("-" * 40)
    print(f"ID: {cliente['id_cliente']}")
    print(f"Nome: {cliente['nome']}")
    print(f"Telefone: {cliente['telefone']}")
    print(f"Complemento: {cliente['complemento'] or 'Não informado'}")
    print(f"E-mail: {cliente['email'] or 'Não informado'}")
    print(f"CPF: {cliente['cpf'] or 'Não informado'}")
    print("-" * 40)


def atualizar():
    print("\n=== ATUALIZAR CLIENTE ===")

    id_cliente = ler_id_cliente()

    if id_cliente is None:
        return

    cliente_atual = buscar_cliente_por_id(id_cliente)

    if not cliente_atual:
        print("\nCliente não encontrado.")
        return

    print("\nPressione Enter para manter o valor atual.")

    nome = input(f"Nome [{cliente_atual['nome']}]: ").strip()
    telefone = input(f"Telefone [{cliente_atual['telefone']}]: ").strip()

    complemento_atual = cliente_atual["complemento"] or ""
    email_atual = cliente_atual["email"] or ""
    cpf_atual = cliente_atual["cpf"] or ""

    complemento = input(
        f"Complemento [{complemento_atual or 'Não informado'}]: "
    ).strip()

    email = input(
        f"E-mail [{email_atual or 'Não informado'}]: "
    ).strip()

    cpf = input(
        f"CPF [{cpf_atual or 'Não informado'}]: "
    ).strip()

    cliente = Cliente(
        nome=nome or cliente_atual["nome"],
        telefone=telefone or cliente_atual["telefone"],
        complemento=complemento or complemento_atual or None,
        email=email or email_atual or None,
        cpf=cpf or cpf_atual or None
    )

    sucesso = atualizar_cliente(id_cliente, cliente)

    if sucesso:
        print("\nCliente atualizado com sucesso!")
    else:
        print("\nNenhuma alteração foi realizada.")


def excluir():
    print("\n=== EXCLUIR CLIENTE ===")

    id_cliente = ler_id_cliente()

    if id_cliente is None:
        return

    cliente = buscar_cliente_por_id(id_cliente)

    if not cliente:
        print("\nCliente não encontrado.")
        return

    print(f"\nCliente selecionado: {cliente['nome']}")
    confirmacao = input("Confirma a exclusão? [s/N]: ").strip().lower()

    if confirmacao != "s":
        print("\nExclusão cancelada.")
        return

    sucesso = excluir_cliente(id_cliente)

    if sucesso:
        print("\nCliente excluído com sucesso!")
    else:
        print(
            "\nNão foi possível excluir o cliente. "
            "Verifique se ele possui ordens de serviço."
        )


def exibir_menu():
    print(
        """
================================
        HARRY_ASSISTENT
================================
1 - Cadastrar cliente
2 - Listar clientes
3 - Buscar cliente por ID
4 - Atualizar cliente
5 - Excluir cliente
0 - Sair
================================
"""
    )


def main():
    acoes = {
        "1": cadastrar,
        "2": listar,
        "3": buscar,
        "4": atualizar,
        "5": excluir
    }

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("\nEncerrando o Harry_Assistent...")
            break

        acao = acoes.get(opcao)

        if acao:
            acao()
        else:
            print("\nOpção inválida.")

        input("\nPressione Enter para voltar ao menu...")


if __name__ == "__main__":
    main()