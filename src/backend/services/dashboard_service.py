from datetime import datetime
from decimal import Decimal

from backend.services.cliente_service import ClienteService
from backend.services.ordem_servico_service import OrdemServicoService
from backend.services.peca_service import PecaService

STATUS_FINALIZADOS = ("Entregue", "Cancelado")


class DashboardService:
    """
    Agrega indicadores de várias áreas do sistema (clientes, OS,
    peças) pra exibição no Dashboard. Não acessa o banco diretamente,
    só reaproveita os Services que já existem.
    """

    @classmethod
    def obter_indicadores(cls):
        ordens = OrdemServicoService.listar()
        clientes = ClienteService.listar()

        return {
            "os_em_andamento": cls._contar_os_em_andamento(ordens),
            "clientes_cadastrados": len(clientes),
            "receita_mes": cls._calcular_receita_mes(ordens),
        }

    @staticmethod
    def _contar_os_em_andamento(ordens):
        return sum(
            1 for ordem in ordens
            if ordem["status"] not in STATUS_FINALIZADOS
        )

    @staticmethod
    def _calcular_receita_mes(ordens):
        agora = datetime.now()
        total = Decimal("0")

        for ordem in ordens:
            data_conclusao = ordem["data_conclusao"]

            if ordem["status"] != "Entregue" or data_conclusao is None:
                continue

            if (
                data_conclusao.month != agora.month
                or data_conclusao.year != agora.year
            ):
                continue

            total_pecas = Decimal(
                str(
                    PecaService.calcular_total_por_ordem_servico(
                        ordem["id_os"]
                    )
                )
            )

            mao_obra = Decimal(str(ordem["mao_obra"]))
            desconto = Decimal(str(ordem["desconto"]))

            total += total_pecas + mao_obra - desconto

        return total