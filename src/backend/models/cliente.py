class Cliente:
    def __init__(
        self,
        nome,
        telefone,
        complemento=None,
        email=None,
        cpf=None
    ):
        self.nome = nome
        self.telefone = telefone
        self.complemento = complemento
        self.email = email
        self.cpf = cpf