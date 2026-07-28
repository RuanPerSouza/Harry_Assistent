from backend.repositories.ordem_servico_repository import (
    cadastrar_ordem_servico,
    listar_ordens_servico,
    buscar_ordem_servico_por_id,
    atualizar_ordem_servico,
    excluir_ordem_servico
)


class OrdemServicoService:

    @staticmethod
    def cadastrar(ordem_servico):
        return cadastrar_ordem_servico(ordem_servico)

    @staticmethod
    def listar():
        return listar_ordens_servico()

    @staticmethod
    def buscar_por_id(id_os):
        return buscar_ordem_servico_por_id(id_os)

    @staticmethod
    def atualizar(ordem_servico):
        return atualizar_ordem_servico(ordem_servico)

    @staticmethod
    def excluir(id_os):
        return excluir_ordem_servico(id_os)