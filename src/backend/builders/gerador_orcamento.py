from backend.services.peca_service import PecaService
from backend.services.ordem_servico_service import OrdemServicoService
from backend.utils.formatadores import (
    formatar_codigo_os,
    formatar_moeda,
    formatar_quantidade_valor,
)


class GeradorOrcamento:

    @staticmethod
    def gerar(id_os):
        ordem = OrdemServicoService.buscar_por_id(id_os)

        if ordem is None:
            return None

        pecas = PecaService.listar_por_ordem_servico(id_os)

        totais = PecaService.calcular_total_ordem_servico(id_os)

        if totais is None:
            return None

        linhas = [
            "=" * 40,
            "ORÇAMENTO",
            formatar_codigo_os(ordem["id_os"]),
            "=" * 40,
            "",
            f"Cliente: {ordem['nome_cliente']}",
            f"Status: {ordem['status']}",
            "",
        ]

        if pecas:
            linhas.append("PEÇAS")
            linhas.append("-" * 40)

            for peca in pecas:
                linhas.append(peca["descricao"])

                linhas.append(
                    formatar_quantidade_valor(
                        peca["quantidade"],
                        peca["valor_unitario"],
                    )
                )

                linhas.append(
                    f"Subtotal: {formatar_moeda(peca['subtotal'])}"
                )

                linhas.append("")

        else:
            linhas.append("Nenhuma peça cadastrada.")
            linhas.append("")

        linhas.append("-" * 40)
        linhas.append(
            f"Total das peças: "
            f"{formatar_moeda(totais['total_pecas'])}"
        )

        if totais["mao_obra"] > 0:
            linhas.append(
                f"Mão de obra: "
                f"{formatar_moeda(totais['mao_obra'])}"
            )

        if totais["desconto"] > 0:
            linhas.append(
                f"Desconto: "
                f"{formatar_moeda(totais['desconto'])}"
            )

        linhas.append("=" * 40)
        linhas.append(
            f"TOTAL: {formatar_moeda(totais['total'])}"
        )
        linhas.append("=" * 40)

        return "\n".join(linhas)