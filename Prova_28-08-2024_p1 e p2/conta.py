from datetime import datetime
from decimal import Decimal

class ContaBancaria:
    def __init__(self, numero_conta, nome, data_abertura, tipo_conta, senha, saldo=Decimal('0')):
        self.numero_conta = numero_conta
        self.nome = nome
        self.data_abertura = data_abertura
        self.tipo_conta = tipo_conta
        self.senha = senha
        self.saldo = Decimal(saldo)

    def to_dict(self):
        return {
            'numero_conta': self.numero_conta,
            'nome': self.nome,
            'data_abertura': self.data_abertura,
            'tipo_conta': self.tipo_conta,
            'senha': self.senha,
            'saldo': self.saldo
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['numero_conta'],
            data['nome'],
            data['data_abertura'],
            data['tipo_conta'],
            data['senha'],
            data['saldo']
        )