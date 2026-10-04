from backend.repositories.cliente_repository import ClienteRepository


class ClienteService:

    repository = ClienteRepository()

    @classmethod
    def cadastrar(cls, cliente):
        return cls.repository.cadastrar(cliente)

    @classmethod
    def listar(cls):
        return cls.repository.listar()

    @classmethod
    def buscar_por_id(cls, id_cliente):
        return cls.repository.buscar_por_id(id_cliente)

    @classmethod
    def atualizar(cls, id_cliente, cliente):
        return cls.repository.atualizar(id_cliente, cliente)

    @classmethod
    def excluir(cls, id_cliente):
        return cls.repository.excluir(id_cliente)