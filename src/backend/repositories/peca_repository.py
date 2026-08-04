from backend.repositories.base_repository import BaseRepository


class PecaRepository(BaseRepository):

    def cadastrar(self, peca):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                INSERT INTO peca (
                    id_os,
                    descricao,
                    quantidade,
                    valor_unitario
                )
                VALUES (%s, %s, %s, %s)
            """

            valores = (
                peca.id_os,
                peca.descricao,
                peca.quantidade,
                peca.valor_unitario
            )

            cursor.execute(sql, valores)
            self.confirmar_transacao(banco)

            peca.id_peca = cursor.lastrowid

            print(f"Peça {peca.id_peca} cadastrada com sucesso!")
            return True

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao cadastrar peça: {erro}")
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
                SELECT *
                FROM peca
                ORDER BY id_peca
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as erro:
            print(f"Erro ao listar peças: {erro}")
            return []

        finally:
            self.fechar_recursos(cursor, banco)

    def buscar_por_id(self, id_peca):
        banco = self.obter_conexao()

        if banco is None:
            return None

        cursor = None

        try:
            cursor = banco.cursor(dictionary=True)

            sql = """
                SELECT *
                FROM peca
                WHERE id_peca = %s
            """

            cursor.execute(sql, (id_peca,))

            return cursor.fetchone()

        except Exception as erro:
            print(f"Erro ao buscar peça: {erro}")
            return None

        finally:
            self.fechar_recursos(cursor, banco)

    def listar_por_ordem_servico(self, id_os):
        banco = self.obter_conexao()

        if banco is None:
            return []

        cursor = None

        try:
            cursor = banco.cursor(dictionary=True)

            sql = """
                SELECT
                    id_peca,
                    id_os,
                    descricao,
                    quantidade,
                    valor_unitario,
                    quantidade * valor_unitario AS subtotal
                FROM peca
                WHERE id_os = %s
                ORDER BY id_peca
            """

            cursor.execute(sql, (id_os,))

            return cursor.fetchall()

        except Exception as erro:
            print(f"Erro ao listar peças da Ordem de Serviço: {erro}")
            return []

        finally:
            self.fechar_recursos(cursor, banco)

    def atualizar(self, peca):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                UPDATE peca
                SET
                    id_os = %s,
                    descricao = %s,
                    quantidade = %s,
                    valor_unitario = %s
                WHERE id_peca = %s
            """

            valores = (
                peca.id_os,
                peca.descricao,
                peca.quantidade,
                peca.valor_unitario,
                peca.id_peca
            )

            cursor.execute(sql, valores)
            self.confirmar_transacao(banco)

            if cursor.rowcount > 0:
                print(f"Peça {peca.id_peca} atualizada com sucesso!")
                return True

            print("Peça não encontrada ou nenhum dado foi alterado.")
            return False

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao atualizar peça: {erro}")
            return False

        finally:
            self.fechar_recursos(cursor, banco)

    def excluir(self, id_peca):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                DELETE FROM peca
                WHERE id_peca = %s
            """

            cursor.execute(sql, (id_peca,))
            self.confirmar_transacao(banco)

            if cursor.rowcount > 0:
                print(f"Peça {id_peca} excluída com sucesso!")
                return True

            print("Peça não encontrada.")
            return False

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao excluir peça: {erro}")
            return False

        finally:
            self.fechar_recursos(cursor, banco)

    def calcular_total_por_ordem_servico(self, id_os):
        banco = self.obter_conexao()

        if banco is None:
            return 0

        cursor = None

        try:
            cursor = banco.cursor(dictionary=True)

            sql = """
                SELECT
                    COALESCE(
                        SUM(quantidade * valor_unitario),
                        0
                    ) AS total_pecas
                FROM peca
                WHERE id_os = %s
            """

            cursor.execute(sql, (id_os,))
            resultado = cursor.fetchone()

            return resultado["total_pecas"]

        except Exception as erro:
            print(f"Erro ao calcular total das peças: {erro}")
            return 0

        finally:
            self.fechar_recursos(cursor, banco)