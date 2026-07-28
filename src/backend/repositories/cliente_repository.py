from backend.repositories.base_repository import BaseRepository


class ClienteRepository(BaseRepository):

    def cadastrar(self, cliente):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                INSERT INTO cliente
                (nome, telefone, complemento, email, cpf)
                VALUES (%s, %s, %s, %s, %s)
            """

            valores = (
                cliente.nome,
                cliente.telefone,
                cliente.complemento,
                cliente.email,
                cliente.cpf
            )

            cursor.execute(sql, valores)
            self.confirmar_transacao(banco)

            print("Cliente cadastrado com sucesso!")
            return True

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao cadastrar cliente: {erro}")
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
                FROM cliente
                ORDER BY nome
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as erro:
            print(f"Erro ao listar clientes: {erro}")
            return []

        finally:
            self.fechar_recursos(cursor, banco)

    def buscar_por_id(self, id_cliente):
        banco = self.obter_conexao()

        if banco is None:
            return None

        cursor = None

        try:
            cursor = banco.cursor(dictionary=True)

            sql = """
                SELECT *
                FROM cliente
                WHERE id_cliente = %s
            """

            cursor.execute(sql, (id_cliente,))

            return cursor.fetchone()

        except Exception as erro:
            print(f"Erro ao buscar cliente: {erro}")
            return None

        finally:
            self.fechar_recursos(cursor, banco)

    def atualizar(self, id_cliente, cliente):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                UPDATE cliente
                SET
                    nome = %s,
                    telefone = %s,
                    complemento = %s,
                    email = %s,
                    cpf = %s
                WHERE id_cliente = %s
            """

            valores = (
                cliente.nome,
                cliente.telefone,
                cliente.complemento,
                cliente.email,
                cliente.cpf,
                id_cliente
            )

            cursor.execute(sql, valores)
            self.confirmar_transacao(banco)

            if cursor.rowcount > 0:
                print("Cliente atualizado com sucesso!")
                return True

            print("Cliente não encontrado ou nenhum dado foi alterado.")
            return False

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao atualizar cliente: {erro}")
            return False

        finally:
            self.fechar_recursos(cursor, banco)

    def excluir(self, id_cliente):
        banco = self.obter_conexao()

        if banco is None:
            return False

        cursor = None

        try:
            cursor = banco.cursor()

            sql = """
                DELETE FROM cliente
                WHERE id_cliente = %s
            """

            cursor.execute(sql, (id_cliente,))
            self.confirmar_transacao(banco)

            if cursor.rowcount > 0:
                print("Cliente excluído com sucesso!")
                return True

            print("Cliente não encontrado.")
            return False

        except Exception as erro:
            self.desfazer_transacao(banco)
            print(f"Erro ao excluir cliente: {erro}")
            return False

        finally:
            self.fechar_recursos(cursor, banco)