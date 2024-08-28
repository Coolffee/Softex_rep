import mysql.connector
import datetime

class BancoDeDados:
    def __init__(self, host, user, password, database):
        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="alou"
        )
        self.cursor = self.conexao.cursor()

    def criar_tabelas(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS contas (
            numero_conta INT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            data_abertura DATE,
            tipo_conta ENUM('poupanca', 'corrente'),
            senha INT NOT NULL,
            saldo DECIMAL(10, 2) DEFAULT 0.0
        );
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero_conta INT,
            descricao VARCHAR(255),
            FOREIGN KEY (numero_conta) REFERENCES contas(numero_conta)
        );
        """)
        self.conexao.commit()

    def inserir_conta(self, conta):
        sql = "INSERT INTO contas (numero_conta, nome, data_abertura, tipo_conta, senha, saldo) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (conta.numero_conta, conta.nome, conta.data_abertura, conta.tipo_conta, conta.senha, conta.saldo)
        self.cursor.execute(sql, valores)
        self.conexao.commit()

    def atualizar_saldo(self, numero_conta, saldo):
        sql = "UPDATE contas SET saldo = %s WHERE numero_conta = %s"
        self.cursor.execute(sql, (saldo, numero_conta))
        self.conexao.commit()

    def registrar_movimentacao(self, numero_conta, descricao):
        sql = "INSERT INTO movimentacoes (numero_conta, descricao) VALUES (%s, %s)"
        self.cursor.execute(sql, (numero_conta, descricao))
        self.conexao.commit()

    def buscar_conta(self, numero_conta):
        sql = "SELECT * FROM contas WHERE numero_conta = %s"
        self.cursor.execute(sql, (numero_conta,))
        conta = self.cursor.fetchone()
        return conta

    def buscar_movimentacoes(self, numero_conta):
        sql = "SELECT descricao FROM movimentacoes WHERE numero_conta = %s"
        self.cursor.execute(sql, (numero_conta,))
        movimentacoes = self.cursor.fetchall()
        return [mov[0] for mov in movimentacoes]

    def excluir_conta(self, numero_conta):
        sql = "DELETE FROM contas WHERE numero_conta = %s"
        self.cursor.execute(sql, (numero_conta,))
        self.conexao.commit()

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()

# Classe ContaBancaria adaptada para usar o BancoDeDados
class ContaBancaria:
    def __init__(self, banco_dados, numero_conta, nome, data_abertura, tipo_conta, senha, saldo=0):
        self.banco_dados = banco_dados
        self.numero_conta = numero_conta
        self.nome = nome
        self.data_abertura = data_abertura
        self.tipo_conta = tipo_conta
        self.senha = senha
        self.saldo = saldo
        self.movimentacoes = self.banco_dados.buscar_movimentacoes(numero_conta)

    def deposito(self, valor):
        if valor > 0:
            self.saldo += valor
            self.banco_dados.atualizar_saldo(self.numero_conta, self.saldo)
            self.banco_dados.registrar_movimentacao(self.numero_conta, f"Depósito: R${valor}")
            print("Depósito realizado com sucesso!")
        else:
            print("Valor inválido para depósito.")

    def saque(self, valor):
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            self.banco_dados.atualizar_saldo(self.numero_conta, self.saldo)
            self.banco_dados.registrar_movimentacao(self.numero_conta, f"Saque: R${valor}")
            print("Saque realizado com sucesso!")
        else:
            print("Saldo insuficiente ou valor inválido.")

    def editar_conta(self, nome=None, senha=None, tipo_conta=None):
        if nome:
            self.nome = nome
        if senha:
            self.senha = senha
        if tipo_conta:
            self.tipo_conta = tipo_conta
        # Atualizar informações no banco de dados, se necessário
        print("Conta editada com sucesso!")

    def extrato(self):
        print(f"Extrato da conta {self.numero_conta}:")
        for movimentacao in self.movimentacoes:
            print(movimentacao)
        print(f"Saldo atual: R${self.saldo}")

class Banco:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados

    def cadastrar_conta(self):
        numero_conta = int(input("Número da conta: "))
        if self.banco_dados.buscar_conta(numero_conta):
            print("Número da conta já existe.")
            return
        nome = input("Seu nome: ")
        data_abertura = input("Data de abertura (dd/mm/aa): ")

        # Converter a data para o formato YYYY-MM-DD
        data_abertura_formatada = datetime.datetime.strptime(data_abertura, '%d/%m/%Y').strftime('%Y-%m-%d')

        tipo_conta = input("Tipo de conta (Poupança: p, Corrente: c): ")
        senha = int(input("Cadastre uma senha: "))
        tipo_conta = "poupanca" if tipo_conta == "p" else "corrente"

        nova_conta = ContaBancaria(self.banco_dados, numero_conta, nome, data_abertura_formatada, tipo_conta, senha)
        self.banco_dados.inserir_conta(nova_conta)
        print("Conta cadastrada com sucesso!")


    def menu_conta(self, conta):
        while True:
            print(f"\nNº da conta: {conta.numero_conta}")
            print(f"Nome do Correntista: {conta.nome}")
            print(f"Tipo: {conta.tipo_conta}")
            print(f"Saldo atual: R${conta.saldo}")
            print("1 - Saque")
            print("2 - Depósito")
            print("3 - Editar conta")
            print("4 - Excluir conta")
            print("5 - Extrato")
            print("6 - Sair")
            opcao = int(input("Opção: "))
            if opcao == 1:
                valor = float(input("Valor do saque: "))
                conta.saque(valor)
            elif opcao == 2:
                valor = float(input("Valor do depósito: "))
                conta.deposito(valor)
            elif opcao == 3:
                nome = input("Novo nome da conta (ou deixe em branco para manter): ")
                senha = input("Nova senha da conta (ou deixe em branco para manter): ")
                tipo_conta = input("Novo tipo de conta (Poupança: p, Corrente: c, ou deixe em branco para manter): ")
                tipo_conta = "poupanca" if tipo_conta == "p" else "corrente" if tipo_conta == "c" else None
                conta.editar_conta(nome if nome else None, int(senha) if senha else None, tipo_conta)
            elif opcao == 4:
                ctz = input("Tem certeza que deseja excluir? S/N ")
                if ctz.upper() == "S":
                    self.banco_dados.excluir_conta(conta.numero_conta)
                    print("Conta excluída com sucesso!")
                    break
            elif opcao == 5:
                conta.extrato()
            elif opcao == 6:
                break
            else:
                print("Opção inválida!")

if __name__ == "__main__":
    banco_dados = BancoDeDados(host="localhost", user="seu_usuario", password="sua_senha", database="nome_do_banco")
    banco_dados.criar_tabelas()
    banco = Banco(banco_dados)

    while True:
        print("\n1 - Entrar na conta")
        print("2 - Cadastrar conta")
        print("3 - Sair")
        opcao = int(input("Opção: "))
        if opcao == 1:
            banco.entrar_conta()
        elif opcao == 2:
            banco.cadastrar_conta()
        elif opcao == 3:
            banco_dados.fechar_conexao()
            break
        else:
            print("Opção inválida!")
