-- Criação do banco de dados
CREATE DATABASE IF NOT EXISTS banco;
USE banco;

-- Criação da tabela de contas
CREATE TABLE IF NOT EXISTS contas (
    numero_conta INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_abertura DATE NOT NULL,
    tipo_conta VARCHAR(20) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);

-- Criação da tabela de movimentações
CREATE TABLE IF NOT EXISTS movimentacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_conta INT,
    tipo VARCHAR(20) NOT NULL,
    valor DECIMAL(10, 2) NOT NULL,
    data DATETIME NOT NULL,
    FOREIGN KEY (numero_conta) REFERENCES contas(numero_conta)
);

-- Inserir alguns dados de exemplo (opcional)
INSERT INTO contas (numero_conta, nome, data_abertura, tipo_conta, senha, saldo)
VALUES 
(1, 'João Silva', '2023-01-01', 'corrente', '123456', 1000.00),
(2, 'Maria Santos', '2023-02-15', 'poupanca', '654321', 500.00);

INSERT INTO movimentacoes (numero_conta, tipo, valor, data)
VALUES
(1, 'deposito', 500.00, '2023-03-01 10:00:00'),
(2, 'saque', 100.00, '2023-03-02 14:30:00');
