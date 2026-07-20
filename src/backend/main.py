from backend.repositories.cliente_repository import buscar_cliente_por_id


cliente = buscar_cliente_por_id(2)

if cliente:
    print("--------------------")
    print(f"ID: {cliente['id_cliente']}")
    print(f"Nome: {cliente['nome']}")
    print(f"Telefone: {cliente['telefone']}")
    print(f"Complemento: {cliente['complemento']}")
    print(f"E-mail: {cliente['email']}")
    print(f"CPF: {cliente['cpf']}")
else:
    print("Cliente não encontrado.")