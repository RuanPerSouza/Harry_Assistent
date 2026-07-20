create database harry_assistent;
use harry_assistent;

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    complemento VARCHAR(100),
    email VARCHAR(100),
    cpf VARCHAR(14)
);

CREATE TABLE ordem_servico (
    id_os INT AUTO_INCREMENT PRIMARY KEY,

    id_cliente INT NOT NULL,

    data_entrada DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_conclusao DATETIME,

    status ENUM(
        'Recebido',
        'Na bancada',
        'Aguardando peça',
        'Em reparo',
        'Reparo concluído',
        'Entregue'
    ) DEFAULT 'Recebido',

    prioridade ENUM(
        'Baixa',
        'Média',
        'Alta',
        'Urgente'
    ) DEFAULT 'Média',

    mao_obra DECIMAL(10,2) DEFAULT 0.00,
    desconto DECIMAL(10,2) DEFAULT 0.00,

    equipamentos_recebidos TEXT,
    observacoes TEXT,

    FOREIGN KEY (id_cliente)
        REFERENCES cliente(id_cliente)
);

CREATE TABLE aparelho (
    id_aparelho INT AUTO_INCREMENT PRIMARY KEY,

    id_os INT NOT NULL,

    tipo ENUM('Celular','Notebook') NOT NULL,

    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(80) NOT NULL,
    cor VARCHAR(30),

    imei VARCHAR(20),
    numero_serie VARCHAR(50),

    senha VARCHAR(50),

    defeito_informado TEXT NOT NULL,
    estado_aparelho TEXT,

    FOREIGN KEY (id_os)
        REFERENCES ordem_servico(id_os)
);

CREATE TABLE peca (
    id_peca INT AUTO_INCREMENT PRIMARY KEY,

    id_os INT NOT NULL,

    descricao VARCHAR(100) NOT NULL,

    quantidade INT NOT NULL DEFAULT 1,

    valor_unitario DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (id_os)
        REFERENCES ordem_servico(id_os)
);

ALTER TABLE ordem_servico
DROP FOREIGN KEY ordem_servico_ibfk_1;

ALTER TABLE ordem_servico
ADD CONSTRAINT fk_ordem_cliente
FOREIGN KEY (id_cliente)
REFERENCES cliente(id_cliente)
ON DELETE RESTRICT
ON UPDATE CASCADE;

ALTER TABLE aparelho
DROP FOREIGN KEY aparelho_ibfk_1;

ALTER TABLE aparelho
ADD CONSTRAINT fk_aparelho_os
FOREIGN KEY (id_os)
REFERENCES ordem_servico(id_os)
ON DELETE CASCADE
ON UPDATE CASCADE;

ALTER TABLE peca
DROP FOREIGN KEY peca_ibfk_1;

ALTER TABLE peca
ADD CONSTRAINT fk_peca_os
FOREIGN KEY (id_os)
REFERENCES ordem_servico(id_os)
ON DELETE CASCADE
ON UPDATE CASCADE;