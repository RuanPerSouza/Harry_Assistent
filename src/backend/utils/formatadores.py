from decimal import Decimal, InvalidOperation


def formatar_moeda(valor):
    """
    Converte um valor numérico para o formato monetário brasileiro.

    Exemplo:
        1250.50 -> R$ 1.250,50
    """
    try:
        valor_decimal = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        valor_decimal = Decimal("0.00")

    valor_formatado = f"{valor_decimal:,.2f}"

    valor_formatado = (
        valor_formatado
        .replace(",", "TEMP")
        .replace(".", ",")
        .replace("TEMP", ".")
    )

    return f"R$ {valor_formatado}"


def formatar_codigo_os(id_os):
    """
    Formata o ID numérico da Ordem de Serviço.

    Exemplo:
        3 -> OS 000003
    """
    try:
        return f"OS {int(id_os):06d}"
    except (TypeError, ValueError):
        return "OS 000000"


def formatar_quantidade_valor(quantidade, valor_unitario):
    """
    Formata quantidade e valor unitário para exibição.

    Exemplo:
        2 × R$ 25,00
    """
    return (
        f"{quantidade} × "
        f"{formatar_moeda(valor_unitario)}"
    )