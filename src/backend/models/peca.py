from decimal import Decimal


class Peca:

    def __init__(
        self,
        id_os,
        descricao,
        valor_unitario,
        quantidade=1,
        id_peca=None
    ):
        self.id_peca = id_peca
        self.id_os = id_os
        self.descricao = descricao
        self.quantidade = quantidade
        self.valor_unitario = Decimal(str(valor_unitario))

    def calcular_subtotal(self):
        return self.valor_unitario * self.quantidade