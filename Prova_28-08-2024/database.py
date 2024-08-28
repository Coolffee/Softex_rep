import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

# Definição da classe DatabaseManager para gerenciar a conexão e manipulação de tabelas no banco de dados
class DatabaseManager:
    
    # Método estático para obter a conexão com o banco de dados MySQL
    @staticmethod
    def get_connection():
        try:
            # Estabelece a conexão usando as configurações definidas em DB_CONFIG
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                # Se a conexão for bem-sucedida, imprime uma mensagem de sucesso e retorna a conexão
                print('Conectado ao MySQL com sucesso!')
                return connection
        except Error as e:
            # Em caso de erro na conexão, imprime o erro e retorna None
            print(f"Erro ao conectar ao MySQL: {e}")
            return None

    # Método estático para criar as tabelas necessárias no banco de dados
    @staticmethod
    def criar_tabelas(connection):
        # Definição da query para criar a tabela 'contas' se ela não existir
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

        # Definição da query para criar a tabela 'movimentacoes' se ela não existir
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

        cursor = connection.cursor()  # Cria um cursor para executar as queries
        try:
            # Executa as queries para criar as tabelas
            cursor.execute(criar_tabela_contas)
            cursor.execute(criar_tabela_movimentacoes)
            connection.commit()  # Confirma as mudanças no banco de dados
            print("Tabelas criadas com sucesso!")
        except Error as e:
            # Em caso de erro na criação das tabelas, imprime o erro
            print(f"Erro ao criar tabelas: {e}")
        finally:
            # Fecha o cursor após a execução das queries, independentemente de sucesso ou falha
            cursor.close()
