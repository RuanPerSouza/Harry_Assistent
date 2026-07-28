from backend.models.ordem_servico import OrdemServico


class OrdemServicoMapper:

    @staticmethod
    def de_dict(dados):
        if dados is None:
            return None

        return OrdemServico(
            id_os=dados.get("id_os"),
            id_cliente=dados.get("id_cliente"),
            data=dados.get("data_entrada"),
            status=dados.get("status"),
            prioridade=dados.get("prioridade"),
            mao_obra=dados.get("mao_obra"),
            desconto=dados.get("desconto"),
            status_pagamento=dados.get("status_pagamento"),
            forma_pagamento=dados.get("forma_pagamento"),
            numero_parcelas=dados.get("numero_parcelas"),
            valor_pago=dados.get("valor_pago"),
            equipamentos_recebidos=dados.get("equipamentos_recebidos"),
            observacoes=dados.get("observacoes"),
        )

    @staticmethod
    def de_lista(lista_dados):
        return [
            OrdemServicoMapper.de_dict(dados)
            for dados in lista_dados
        ]