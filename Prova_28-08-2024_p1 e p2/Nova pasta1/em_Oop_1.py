import json

class ContaBancaria:
    def __init__(self, numero_conta, nome, data_abertura, tipo_conta, senha, saldo=0, movimentacoes=None):
        self.numero_conta = numero_conta
        self.nome = nome
        self.data_abertura = data_abertura
        self.tipo_conta = tipo_conta
        self.senha = senha
        self.saldo = saldo
        self.movimentacoes = movimentacoes if movimentacoes is not None else []

    def deposito(self, valor):
        if valor > 0:
            self.saldo += valor
            self.movimentacoes.append(f"Depósito: R${valor}")
            print("Depósito realizado com sucesso!")
        else:
            print("Valor inválido para depósito.")

    def saque(self, valor):
        if 0 < valor <= self.saldo:
            self.saldo -= valor
            self.movimentacoes.append(f"Saque: R${valor}")
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
        print("Conta editada com sucesso!")

    def extrato(self):
        print(f"Extrato da conta {self.numero_conta}:")
        for movimentacao in self.movimentacoes:
            print(movimentacao)
        print(f"Saldo atual: R${self.saldo}")

class Banco:
    def __init__(self):
        self.contas = self.carregar_contas()

    def cadastrar_conta(self):
        numero_conta = int(input("Número da conta: "))
        if any(conta.numero_conta == numero_conta for conta in self.contas):
            print("Número da conta já existe.")
            return
        nome = input("Seu nome: ")
        data_abertura = input("Data de abertura (dd/mm/aa): ")
        tipo_conta = input("Tipo de conta (Poupança: p, Corrente: c): ")
        senha = int(input("Cadastre uma senha: "))
        tipo_conta = "poupanca" if tipo_conta == "p" else "corrente"

        nova_conta = ContaBancaria(numero_conta, nome, data_abertura, tipo_conta, senha)
        self.contas.append(nova_conta)
        print("Conta cadastrada com sucesso!")

    def entrar_conta(self):
        numero_conta = int(input("Digite o número da conta: "))
        conta = self.buscar_conta(numero_conta)

        if conta:
            senha = int(input("Digite a senha da conta: "))
            if senha == conta.senha:
                self.menu_conta(conta)
            else:
                print("Senha inválida!")
        else:
            print("Número da conta não existe!")

    def buscar_conta(self, numero_conta):
        for conta in self.contas:
            if conta.numero_conta == numero_conta:
                return conta
        return None

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
                    self.contas.remove(conta)
                    print("Conta excluída com sucesso!")
                    break
            elif opcao == 5:
                conta.extrato()
            elif opcao == 6:
                break
            else:
                print("Opção inválida!")

    def salvar_contas(self):
        dados = [{"numero_conta": conta.numero_conta, "nome": conta.nome, "data_abertura": conta.data_abertura, "tipo_conta": conta.tipo_conta, "senha": conta.senha, "saldo": conta.saldo, "movimentacoes": conta.movimentacoes} for conta in self.contas]
        with open("contas.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)

    def carregar_contas(self):
        try:
            with open("contas.json", "r") as arquivo:
                dados = json.load(arquivo)
            return [ContaBancaria(**conta) for conta in dados]
        except FileNotFoundError:
            return []

if __name__ == "__main__":
    banco = Banco()
    while True:
        banco.salvar_contas()
        print("\n1 - Entrar na conta")
        print("2 - Cadastrar conta")
        print("3 - Sair")
        opcao = int(input("Opção: "))
        if opcao == 1:
            banco.entrar_conta()
        elif opcao == 2:
            banco.cadastrar_conta()
        elif opcao == 3:
            break
        else:
            print("Opção inválida!")
