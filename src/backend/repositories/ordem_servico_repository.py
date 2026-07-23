from backend.conexao import conectar


def cadastrar_ordem_servico(ordem_servico):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            INSERT INTO ordem_servico (
                id_cliente,
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
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            ordem_servico.id_cliente,
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
        )

        cursor.execute(sql, valores)
        conexao.commit()

        ordem_servico.id_os = cursor.lastrowid

        print(
            f"Ordem de Serviço cadastrada com sucesso. "
            f"ID: {ordem_servico.id_os}"
        )

        return ordem_servico.id_os

    except Exception as erro:
        if conexao:
            conexao.rollback()

        print(f"Erro ao cadastrar Ordem de Serviço: {erro}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()

def listar_ordens_servico():
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

        sql = """
            SELECT
                os.id_os,
                os.id_cliente,
                c.nome AS nome_cliente,
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
            FROM ordem_servico os
            INNER JOIN cliente c
                ON c.id_cliente = os.id_cliente
            ORDER BY os.id_os DESC
        """

        cursor.execute(sql)
        ordens = cursor.fetchall()

        return ordens

    except Exception as erro:
        print(f"Erro ao listar Ordens de Serviço: {erro}")
        return []

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()

def buscar_ordem_servico_por_id(id_os):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)

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
            FROM ordem_servico os
            INNER JOIN cliente c
                ON c.id_cliente = os.id_cliente
            WHERE os.id_os = %s
        """

        cursor.execute(sql, (id_os,))
        ordem = cursor.fetchone()

        return ordem

    except Exception as erro:
        print(f"Erro ao buscar Ordem de Serviço: {erro}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()

def atualizar_ordem_servico(ordem_servico):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            UPDATE ordem_servico
            SET
                id_cliente = %s,
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
        conexao.commit()

        if cursor.rowcount == 0:
            print("Nenhuma Ordem de Serviço foi atualizada.")
            return False

        print("Ordem de Serviço atualizada com sucesso.")
        return True

    except Exception as erro:
        if conexao:
            conexao.rollback()

        print(f"Erro ao atualizar Ordem de Serviço: {erro}")
        return False

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()

def excluir_ordem_servico(id_os):
    conexao = None
    cursor = None

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        sql = """
            DELETE FROM ordem_servico
            WHERE id_os = %s
        """

        cursor.execute(sql, (id_os,))
        conexao.commit()

        if cursor.rowcount == 0:
            print("Ordem de Serviço não encontrada.")
            return False

        print("Ordem de Serviço excluída com sucesso.")
        return True

    except Exception as erro:
        if conexao:
            conexao.rollback()

        print(f"Erro ao excluir Ordem de Serviço: {erro}")
        return False

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()