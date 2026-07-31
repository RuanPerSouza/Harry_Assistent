class Aparelho:

    def __init__(
        self,
        id_os,
        tipo,
        marca,
        modelo,
        defeito_informado,
        cor=None,
        imei=None,
        numero_serie=None,
        senha=None,
        estado_aparelho=None,
        id_aparelho=None
    ):
        self.id_aparelho = id_aparelho
        self.id_os = id_os
        self.tipo = tipo
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.imei = imei
        self.numero_serie = numero_serie
        self.senha = senha
        self.defeito_informado = defeito_informado
        self.estado_aparelho = estado_aparelho