from backend.conexao import conectar


def cadastrar_cliente(cliente):

    banco = conectar()

    cursor = banco.cursor()


    sql = """
    INSERT INTO cliente
    (nome, telefone, complemento, email, cpf)

    VALUES
    (%s, %s, %s, %s, %s)
    """


    valores = (
        cliente.nome,
        cliente.telefone,
        cliente.complemento,
        cliente.email,
        cliente.cpf
    )


    cursor.execute(sql, valores)

    banco.commit()


    cursor.close()
    banco.close()


    print("Cliente cadastrado com sucesso!")

def listar_clientes():

    banco = conectar()

    if banco is None:
        return []

    cursor = banco.cursor(dictionary=True)

    sql = """
        SELECT *
        FROM cliente
        ORDER BY nome
    """

    cursor.execute(sql)

    clientes = cursor.fetchall()

    cursor.close()
    banco.close()

    return clientes

from backend.conexao import conectar


def cadastrar_cliente(cliente):
    banco = conectar()

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
        banco.commit()

        return True

    except Exception as erro:
        banco.rollback()
        print(f"Erro ao cadastrar cliente: {erro}")
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if banco.is_connected():
            banco.close()


def listar_clientes():
    banco = conectar()

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
        if cursor is not None:
            cursor.close()

        if banco.is_connected():
            banco.close()

def buscar_cliente_por_id(id_cliente):
    banco = conectar()

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
        if cursor is not None:
            cursor.close()

        if banco.is_connected():
            banco.close()

def buscar_cliente_por_id(id_cliente):
    banco = conectar()

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
        if cursor is not None:
            cursor.close()

        if banco.is_connected():
            banco.close()


def atualizar_cliente(cliente, id_cliente):
    banco = conectar()

    if banco is None:
        return False

    cursor = None

    try:
        cursor = banco.cursor()

        sql = """
            UPDATE cliente
            SET nome = %s,
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
        banco.commit()

        return cursor.rowcount > 0

    except Exception as erro:
        banco.rollback()
        print(f"Erro ao atualizar cliente: {erro}")
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if banco.is_connected():
            banco.close()


def excluir_cliente(id_cliente):
    banco = conectar()

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
        banco.commit()

        return cursor.rowcount > 0

    except Exception as erro:
        banco.rollback()
        print(f"Erro ao excluir cliente: {erro}")
        return False

    finally:
        if cursor is not None:
            cursor.close()

        if banco.is_connected():
            banco.close()