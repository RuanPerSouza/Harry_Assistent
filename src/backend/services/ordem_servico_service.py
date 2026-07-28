from backend.repositories.ordem_servico_repository import (
    OrdemServicoRepository
)


class OrdemServicoService:

    repository = OrdemServicoRepository()

    @classmethod
    def cadastrar(cls, ordem_servico):
        return cls.repository.cadastrar(ordem_servico)

    @classmethod
    def listar(cls):
        return cls.repository.listar()

    @classmethod
    def buscar_por_id(cls, id_os):
        return cls.repository.buscar_por_id(id_os)

    @classmethod
    def atualizar(cls, ordem_servico):
        return cls.repository.atualizar(ordem_servico)

    @classmethod
    def excluir(cls, id_os):
        return cls.repository.excluir(id_os)