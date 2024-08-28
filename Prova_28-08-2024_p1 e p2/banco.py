from mysql.connector import Error
from datetime import datetime
from database import DatabaseManager
from conta import ContaBancaria
from decimal import Decimal

class Banco:
    def __init__(self):
        self.connection = DatabaseManager.get_connection()
        if self.connection:
            DatabaseManager.criar_tabelas(self.connection)

    def cadastrar_conta(self):
        while True:
            try:
                numero_conta = int(input("Número da conta: "))
                if self.conta_existe(numero_conta):
                    print("Erro: Número de conta já existe. Por favor, escolha outro número.")
                    continue
                break
            except ValueError:
                print("Erro: Por favor, insira um número inteiro válido para o número da conta.")

        nome = input("Seu nome: ")
        while len(nome.strip()) == 0:
            print("Erro: O nome não pode estar vazio.")
            nome = input("Seu nome: ")

        while True:
            data_abertura = input("Data de abertura (dd/mm/aaaa): ")
            try:
                data = datetime.strptime(data_abertura, "%d/%m/%Y").date()
                if data > datetime.now().date():
                    print("Erro: A data de abertura não pode ser no futuro.")
                    continue
                break
            except ValueError:
                print("Erro: Formato de data inválido. Use dd/mm/aaaa.")

        while True:
            tipo_conta = input("Tipo de conta (Poupança: p, Corrente: c): ").lower()
            if tipo_conta in ['p', 'c']:
                tipo_conta = "poupanca" if tipo_conta == "p" else "corrente"
                break
            else:
                print("Erro: Por favor, insira 'p' para Poupança ou 'c' para Corrente.")

        while True:
            senha = input("Cadastre uma senha (apenas números): ")
            if senha.isdigit():
                break
            else:
                print("Erro: A senha deve conter apenas números.")

        query = """
        INSERT INTO contas (numero_conta, nome, data_abertura, tipo_conta, senha, saldo)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (numero_conta, nome, data, tipo_conta, senha, Decimal('0'))

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, values)
            self.connection.commit()
            print("Conta cadastrada com sucesso!")
        except Error as e:
            print(f"Erro ao cadastrar conta: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def entrar_conta(self):
        numero_conta = int(input("Digite o número da conta: "))
        senha = input("Digite a senha da conta: ")

        query = "SELECT * FROM contas WHERE numero_conta = %s AND senha = %s"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (numero_conta, senha))
            conta_data = cursor.fetchone()
            if conta_data:
                conta = ContaBancaria.from_dict(conta_data)
                self.menu_conta(conta)
            else:
                print("Número da conta ou senha inválidos!")
        except Error as e:
            print(f"Erro ao buscar conta: {e}")
        finally:
            cursor.close()

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
                self.saque(conta)
            elif opcao == 2:
                self.deposito(conta)
            elif opcao == 3:
                self.editar_conta(conta)
            elif opcao == 4:
                if self.excluir_conta(conta):
                    break
            elif opcao == 5:
                self.extrato(conta)
            elif opcao == 6:
                break
            else:
                print("Opção inválida!")

    def saque(self, conta):
        valor = Decimal(input("Valor do saque: "))
        if 0 < valor <= conta.saldo:
            query_update = "UPDATE contas SET saldo = saldo - %s WHERE numero_conta = %s"
            query_insert = "INSERT INTO movimentacoes (numero_conta, tipo, valor, data) VALUES (%s, %s, %s, %s)"
            
            cursor = self.connection.cursor()
            try:
                cursor.execute(query_update, (valor, conta.numero_conta))
                cursor.execute(query_insert, (conta.numero_conta, "saque", valor, datetime.now()))
                self.connection.commit()
                conta.saldo -= valor
                print(f"Saque de R${valor:.2f} realizado com sucesso!")
                print(f"Novo saldo: R${conta.saldo:.2f}")
            except Error as e:
                print(f"Erro ao realizar saque: {e}")
                self.connection.rollback()
            finally:
                cursor.close()
        else:
            print("Saldo insuficiente ou valor inválido.")

    def deposito(self, conta):
        valor = Decimal(input("Valor do depósito: "))
        if valor > 0:
            query_update = "UPDATE contas SET saldo = saldo + %s WHERE numero_conta = %s"
            query_insert = "INSERT INTO movimentacoes (numero_conta, tipo, valor, data) VALUES (%s, %s, %s, %s)"
            
            cursor = self.connection.cursor()
            try:
                cursor.execute(query_update, (valor, conta.numero_conta))
                cursor.execute(query_insert, (conta.numero_conta, "deposito", valor, datetime.now()))
                self.connection.commit()
                conta.saldo += valor
                print(f"Depósito de R${valor:.2f} realizado com sucesso!")
                print(f"Novo saldo: R${conta.saldo:.2f}")
            except Error as e:
                print(f"Erro ao realizar depósito: {e}")
                self.connection.rollback()
            finally:
                cursor.close()
        else:
            print("Valor inválido para depósito.")

    def editar_conta(self, conta):
        nome = input("Novo nome da conta (ou deixe em branco para manter): ")
        senha = input("Nova senha da conta (ou deixe em branco para manter): ")
        tipo_conta = input("Novo tipo de conta (Poupança: p, Corrente: c, ou deixe em branco para manter): ")

        query = "UPDATE contas SET "
        updates = []
        values = []

        if nome:
            updates.append("nome = %s")
            values.append(nome)
        if senha:
            updates.append("senha = %s")
            values.append(senha)
        if tipo_conta:
            tipo_conta = "poupanca" if tipo_conta.lower() == "p" else "corrente"
            updates.append("tipo_conta = %s")
            values.append(tipo_conta)

        if not updates:
            print("Nenhuma alteração realizada.")
            return

        query += ", ".join(updates) + " WHERE numero_conta = %s"
        values.append(conta.numero_conta)

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, tuple(values))
            self.connection.commit()
            print("Conta editada com sucesso!")
        except Error as e:
            print(f"Erro ao editar conta: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def excluir_conta(self, conta):
        confirmacao = input("Tem certeza que deseja excluir? S/N ").upper()
        if confirmacao == "S":
            query_delete_movimentacoes = "DELETE FROM movimentacoes WHERE numero_conta = %s"
            query_delete_conta = "DELETE FROM contas WHERE numero_conta = %s"
            
            cursor = self.connection.cursor()
            try:
                cursor.execute(query_delete_movimentacoes, (conta.numero_conta,))
                cursor.execute(query_delete_conta, (conta.numero_conta,))
                self.connection.commit()
                print("Conta excluída com sucesso!")
                return True
            except Error as e:
                print(f"Erro ao excluir conta: {e}")
                self.connection.rollback()
            finally:
                cursor.close()
        return False

    def extrato(self, conta):
        query = """
        SELECT tipo, valor, data
        FROM movimentacoes
        WHERE numero_conta = %s
        ORDER BY data DESC
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (conta.numero_conta,))
            movimentacoes = cursor.fetchall()
            
            print(f"\nExtrato da conta {conta.numero_conta}:")
            for mov in movimentacoes:
                print(f"{mov['data']}: {mov['tipo'].capitalize()} de R${mov['valor']:.2f}")
            print(f"Saldo atual: R${conta.saldo:.2f}")
        except Error as e:
            print(f"Erro ao gerar extrato: {e}")
        finally:
            cursor.close()

    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            print("Conexão com o banco de dados encerrada.")

    def conta_existe(self, numero_conta):
        query = "SELECT COUNT(*) FROM contas WHERE numero_conta = %s"
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, (numero_conta,))
            (count,) = cursor.fetchone()
            return count > 0
        except Error as e:
            print(f"Erro ao verificar existência da conta: {e}")
            return False
        finally:
            cursor.close()
