from backend.repositories.aparelho_repository import AparelhoRepository


class AparelhoService:

    repository = AparelhoRepository()

    @classmethod
    def cadastrar(cls, aparelho):
        return cls.repository.cadastrar(aparelho)

    @classmethod
    def listar(cls):
        return cls.repository.listar()

    @classmethod
    def buscar_por_id(cls, id_aparelho):
        return cls.repository.buscar_por_id(id_aparelho)

    @classmethod
    def listar_por_ordem_servico(cls, id_os):
        return cls.repository.listar_por_ordem_servico(id_os)

    @classmethod
    def atualizar(cls, aparelho):
        return cls.repository.atualizar(aparelho)

    @classmethod
    def excluir(cls, id_aparelho):
        return cls.repository.excluir(id_aparelho)