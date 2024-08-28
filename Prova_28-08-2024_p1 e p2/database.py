import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class DatabaseManager:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                print('Conectado ao MySQL com sucesso!')
                return connection
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    @staticmethod
    def criar_tabelas(connection):
        criar_tabela_contas = """
        CREATE TABLE IF NOT EXISTS contas (
            numero_conta INT PRIMARY KEY,
            nome VARCHAR(100),
            data_abertura DATE,
            tipo_conta VARCHAR(20),
            senha VARCHAR(255),
            saldo DECIMAL(10, 2)
        )
        """

        criar_tabela_movimentacoes = """
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero_conta INT,
            tipo VARCHAR(20),
            valor DECIMAL(10, 2),
            data DATETIME,
            FOREIGN KEY (numero_conta) REFERENCES contas(numero_conta)
        )
        """

        cursor = connection.cursor()
        try:
            cursor.execute(criar_tabela_contas)
            cursor.execute(criar_tabela_movimentacoes)
            connection.commit()
            print("Tabelas criadas com sucesso!")
        except Error as e:
            print(f"Erro ao criar tabelas: {e}")
        finally:
            cursor.close()
