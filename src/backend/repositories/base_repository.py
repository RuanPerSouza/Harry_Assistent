from backend.conexao import conectar


class BaseRepository:

    def obter_conexao(self):
        return conectar()

    def confirmar_transacao(self, conexao):
        conexao.commit()

    def desfazer_transacao(self, conexao):
        if conexao and conexao.is_connected():
            conexao.rollback()

    def fechar_recursos(self, cursor=None, conexao=None):
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()