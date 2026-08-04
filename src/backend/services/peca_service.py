from backend.repositories.peca_repository import PecaRepository


class PecaService:

    repository = PecaRepository()

    @classmethod
    def cadastrar(cls, peca):
        return cls.repository.cadastrar(peca)

    @classmethod
    def listar(cls):
        return cls.repository.listar()

    @classmethod
    def buscar_por_id(cls, id_peca):
        return cls.repository.buscar_por_id(id_peca)

    @classmethod
    def listar_por_ordem_servico(cls, id_os):
        return cls.repository.listar_por_ordem_servico(id_os)

    @classmethod
    def atualizar(cls, peca):
        return cls.repository.atualizar(peca)

    @classmethod
    def excluir(cls, id_peca):
        return cls.repository.excluir(id_peca)

    @classmethod
    def calcular_total_por_ordem_servico(cls, id_os):
        return cls.repository.calcular_total_por_ordem_servico(id_os)

from decimal import Decimal

from backend.repositories.ordem_servico_repository import (
    OrdemServicoRepository
)
from backend.repositories.peca_repository import PecaRepository


class PecaService:

    repository = PecaRepository()
    ordem_repository = OrdemServicoRepository()

    @classmethod
    def cadastrar(cls, peca):
        return cls.repository.cadastrar(peca)

    @classmethod
    def listar(cls):
        return cls.repository.listar()

    @classmethod
    def buscar_por_id(cls, id_peca):
        return cls.repository.buscar_por_id(id_peca)

    @classmethod
    def listar_por_ordem_servico(cls, id_os):
        return cls.repository.listar_por_ordem_servico(id_os)

    @classmethod
    def atualizar(cls, peca):
        return cls.repository.atualizar(peca)

    @classmethod
    def excluir(cls, id_peca):
        return cls.repository.excluir(id_peca)

    @classmethod
    def calcular_total_por_ordem_servico(cls, id_os):
        return cls.repository.calcular_total_por_ordem_servico(id_os)

    @classmethod
    def calcular_total_ordem_servico(cls, id_os):
        ordem = cls.ordem_repository.buscar_por_id(id_os)

        if ordem is None:
            return None

        total_pecas = Decimal(
            str(cls.repository.calcular_total_por_ordem_servico(id_os))
        )

        mao_obra = Decimal(str(ordem["mao_obra"]))
        desconto = Decimal(str(ordem["desconto"]))

        total = total_pecas + mao_obra - desconto

        return {
            "total_pecas": total_pecas,
            "mao_obra": mao_obra,
            "desconto": desconto,
            "total": total
        }