import mysql.connector
from mysql.connector import Error


def conectar():

    try:

        conexao = mysql.connector.connect(

            host="localhost",

            user="root",

            password="root",

            database="harry_assistent"

        )


        if conexao.is_connected():

            print("Conectado ao banco Harry_Assistent")

            return conexao


    except Error as erro:

        print(f"Erro ao conectar: {erro}")

        return None