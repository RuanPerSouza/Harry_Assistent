from backend.repositories.base_repository import BaseRepository


class OrdemServicoRepository(BaseRepository):

    def cadastrar(self, ordem_servico):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                INSERT INTO ordem_servico (
                    id_cliente,
                    data_entrada,
                    data_conclusao,
                    status,
                    prioridade,
                    mao_obra,
                    desconto,
                    status_pagamento,
                    forma_pagamento,
                    numero_parcelas,
                    valor_pago,
                    equipamentos_recebidos,
                    observacoes
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s
                )
            """

            valores = (
                ordem_servico.id_cliente,
                ordem_servico.data_entrada,
                ordem_servico.data_conclusao,
                ordem_servico.status,
                ordem_servico.prioridade,
                ordem_servico.mao_obra,
                ordem_servico.desconto,
                ordem_servico.status_pagamento,
                ordem_servico.forma_pagamento,
                ordem_servico.numero_parcelas,
                ordem_servico.valor_pago,
                ordem_servico.equipamentos_recebidos,
                ordem_servico.observacoes
            )

            cursor.execute(sql, valores)
            self.confirmar_transacao(banco)

            ordem_servico.id_os = cursor.lastrowid

            print(
                f"Ordem de Serviço "
                f"{ordem_servico.id_os:06d} cadastrada com sucesso!"
            )

            return True

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao cadastrar Ordem de Serviço: {erro}")
            return False

        finally:
            self.fechar_recursos(cursor, banco)

    def listar(self):
        banco = self.obter_conexao()

        if banco is None:
            return []

        cursor = None

        try:
            cursor = banco.cursor(dictionary=True)

            sql = """
                SELECT
                    os.id_os,
                    os.id_cliente,
                    c.nome AS nome_cliente,
                    c.telefone AS telefone_cliente,
                    os.data_entrada,
                    os.data_conclusao,
                    os.status,
                    os.prioridade,
                    os.mao_obra,
                    os.desconto,
                    os.status_pagamento,
                    os.forma_pagamento,
                    os.numero_parcelas,
                    os.valor_pago,
                    os.equipamentos_recebidos,
                    os.observacoes
                FROM ordem_servico AS os
                INNER JOIN cliente AS c
                    ON c.id_cliente = os.id_cliente
                ORDER BY os.id_os DESC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as erro:
            print(f"Erro ao listar Ordens de Serviço: {erro}")
            return []

        finally:
            self.fechar_recursos(cursor, banco)

    def buscar_por_id(self, id_os):
        banco = self.obter_conexao()

        if banco is None:
            return None

        cursor = None

        try:
            cursor = banco.cursor(dictionary=True)

            sql = """
                SELECT
                    os.id_os,
                    os.id_cliente,
                    c.nome AS nome_cliente,
                    c.telefone AS telefone_cliente,
                    c.email AS email_cliente,
                    c.cpf AS cpf_cliente,
                    os.data_entrada,
                    os.data_conclusao,
                    os.status,
                    os.prioridade,
                    os.mao_obra,
                    os.desconto,
                    os.status_pagamento,
                    os.forma_pagamento,
                    os.numero_parcelas,
                    os.valor_pago,
                    os.equipamentos_recebidos,
                    os.observacoes
                FROM ordem_servico AS os
                INNER JOIN cliente AS c
                    ON c.id_cliente = os.id_cliente
                WHERE os.id_os = %s
            """

            cursor.execute(sql, (id_os,))

            return cursor.fetchone()

        except Exception as erro:
            print(f"Erro ao buscar Ordem de Serviço: {erro}")
            return None

        finally:
            self.fechar_recursos(cursor, banco)

    def atualizar(self, ordem_servico):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                UPDATE ordem_servico
                SET
                    id_cliente = %s,
                    data_entrada = %s,
                    data_conclusao = %s,
                    status = %s,
                    prioridade = %s,
                    mao_obra = %s,
                    desconto = %s,
                    status_pagamento = %s,
                    forma_pagamento = %s,
                    numero_parcelas = %s,
                    valor_pago = %s,
                    equipamentos_recebidos = %s,
                    observacoes = %s
                WHERE id_os = %s
            """

            valores = (
                ordem_servico.id_cliente,
                ordem_servico.data_entrada,
                ordem_servico.data_conclusao,
                ordem_servico.status,
                ordem_servico.prioridade,
                ordem_servico.mao_obra,
                ordem_servico.desconto,
                ordem_servico.status_pagamento,
                ordem_servico.forma_pagamento,
                ordem_servico.numero_parcelas,
                ordem_servico.valor_pago,
                ordem_servico.equipamentos_recebidos,
                ordem_servico.observacoes,
                ordem_servico.id_os
            )

            cursor.execute(sql, valores)
            self.confirmar_transacao(banco)

            if cursor.rowcount > 0:
                print(
                    f"Ordem de Serviço "
                    f"{ordem_servico.id_os:06d} atualizada com sucesso!"
                )
                return True

            print("Ordem de Serviço não encontrada ou nenhum dado foi alterado.")
            return False

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao atualizar Ordem de Serviço: {erro}")
            return False

        finally:
            self.fechar_recursos(cursor, banco)

    def excluir(self, id_os):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                DELETE FROM ordem_servico
                WHERE id_os = %s
            """

            cursor.execute(sql, (id_os,))
            self.confirmar_transacao(banco)

            if cursor.rowcount > 0:
                print(
                    f"Ordem de Serviço "
                    f"{id_os:06d} excluída com sucesso!"
                )
                return True

            print("Ordem de Serviço não encontrada.")
            return False

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao excluir Ordem de Serviço: {erro}")
            return False

        finally:
            self.fechar_recursos(cursor, banco)