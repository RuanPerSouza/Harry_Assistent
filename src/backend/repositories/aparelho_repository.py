from backend.repositories.base_repository import BaseRepository


class AparelhoRepository(BaseRepository):

    def cadastrar(self, aparelho):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                INSERT INTO aparelho (
                    id_os,
                    tipo,
                    marca,
                    modelo,
                    cor,
                    imei,
                    numero_serie,
                    senha,
                    defeito_informado,
                    estado_aparelho
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """

            valores = (
                aparelho.id_os,
                aparelho.tipo,
                aparelho.marca,
                aparelho.modelo,
                aparelho.cor,
                aparelho.imei,
                aparelho.numero_serie,
                aparelho.senha,
                aparelho.defeito_informado,
                aparelho.estado_aparelho
            )

            cursor.execute(sql, valores)

            self.confirmar_transacao(banco)

            aparelho.id_aparelho = cursor.lastrowid

            print(
                f"Aparelho {aparelho.id_aparelho} cadastrado com sucesso!"
            )

            return True

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao cadastrar aparelho: {erro}")
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
                FROM aparelho
                ORDER BY id_aparelho
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as erro:
            print(f"Erro ao listar aparelhos: {erro}")
            return []

        finally:
            self.fechar_recursos(cursor, banco)

    def buscar_por_id(self, id_aparelho):
        banco = self.obter_conexao()

        if banco is None:
            return None

        cursor = None

        try:
            cursor = banco.cursor(dictionary=True)

            sql = """
                SELECT *
                FROM aparelho
                WHERE id_aparelho = %s
            """

            cursor.execute(sql, (id_aparelho,))

            return cursor.fetchone()

        except Exception as erro:
            print(f"Erro ao buscar aparelho: {erro}")
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
                SELECT *
                FROM aparelho
                WHERE id_os = %s
                ORDER BY id_aparelho
            """

            cursor.execute(sql, (id_os,))

            return cursor.fetchall()

        except Exception as erro:
            print(f"Erro ao listar aparelhos da OS: {erro}")
            return []

        finally:
            self.fechar_recursos(cursor, banco)

    def atualizar(self, aparelho):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                UPDATE aparelho
                SET
                    id_os = %s,
                    tipo = %s,
                    marca = %s,
                    modelo = %s,
                    cor = %s,
                    imei = %s,
                    numero_serie = %s,
                    senha = %s,
                    defeito_informado = %s,
                    estado_aparelho = %s
                WHERE id_aparelho = %s
            """

            valores = (
                aparelho.id_os,
                aparelho.tipo,
                aparelho.marca,
                aparelho.modelo,
                aparelho.cor,
                aparelho.imei,
                aparelho.numero_serie,
                aparelho.senha,
                aparelho.defeito_informado,
                aparelho.estado_aparelho,
                aparelho.id_aparelho
            )

            cursor.execute(sql, valores)

            self.confirmar_transacao(banco)

            print(
                f"Aparelho {aparelho.id_aparelho} atualizado com sucesso!"
            )

            return True

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao atualizar aparelho: {erro}")
            return False

        finally:
            self.fechar_recursos(cursor, banco)

    def excluir(self, id_aparelho):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                DELETE FROM aparelho
                WHERE id_aparelho = %s
            """

            cursor.execute(sql, (id_aparelho,))

            self.confirmar_transacao(banco)

            print(f"Aparelho {id_aparelho} excluído com sucesso!")

            return True

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao excluir aparelho: {erro}")
            return False

        finally:
            self.fechar_recursos(cursor, banco)