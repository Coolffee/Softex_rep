from datetime import datetime
from decimal import Decimal

# Definição da classe ContaBancaria, que representa uma conta bancária
class ContaBancaria:
    def __init__(self, numero_conta, nome, data_abertura, tipo_conta, senha, saldo=Decimal('0')):
        # Inicializa os atributos da conta bancária
        self.numero_conta = numero_conta  # Número da conta bancária
        self.nome = nome  # Nome do titular da conta
        self.data_abertura = data_abertura  # Data de abertura da conta
        self.tipo_conta = tipo_conta  # Tipo da conta (poupança ou corrente)
        self.senha = senha  # Senha da conta
        self.saldo = Decimal(saldo)  # Saldo inicial da conta, definido como 0 por padrão

    # Método que converte os atributos da conta para um dicionário
    def to_dict(self):
        return {
            'numero_conta': self.numero_conta,  # Retorna o número da conta
            'nome': self.nome,  # Retorna o nome do titular da conta
            'data_abertura': self.data_abertura,  # Retorna a data de abertura da conta
            'tipo_conta': self.tipo_conta,  # Retorna o tipo da conta
            'senha': self.senha,  # Retorna a senha da conta
            'saldo': self.saldo  # Retorna o saldo atual da conta
        }

    # Método de classe que cria uma instância de ContaBancaria a partir de um dicionário
    @classmethod
    def from_dict(cls, data):
        # Retorna uma nova instância da classe ContaBancaria usando os dados do dicionário
        return cls(
            data['numero_conta'],  # Número da conta
            data['nome'],  # Nome do titular da conta
            data['data_abertura'],  # Data de abertura da conta
            data['tipo_conta'],  # Tipo da conta
            data['senha'],  # Senha da conta
            data['saldo']  # Saldo da conta
        )
