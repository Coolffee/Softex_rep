# Cadastro de contas bancarias e correntista
    # nome do correntista
    # número da conta(único)
    # data da abertura da conta
    # tipo da conta(poupança ou corrente)

# Operações financeiras
    # deposito
    # saque
    # Salvar cada saque e deposito em uma lista de movimentações
# Geraciamento de contas
    # editar contas
    # excluir contas

# extrato bancário
    # poder vizualiar o extrato do banco, podendo vizualizar as movimentações


# Informaçôes
import json

def cadastrar_contas(contas):
    conta = {}
    t = True
    while t == True:
        n2_conta = int(input("Numero da conta: "))
        for conta in contas:
            if n2_conta == conta["n_conta"]:
                print("Número da conta já existe")
                break
        else:
            t = False
    conta["n_conta"] = n2_conta
    conta["nome"] = input("Seu nome: ")
    conta["data"] = input("Data: dd/mm/aa: ")
    tipo = input("Poupança: p, Corrente: c ")
    conta["senha"] = int(input("Cadastre uma senha: "))
    conta["saldo"] = 0
    if tipo == "p":
        conta["tipo"] = "poupanca"
    elif tipo == "c":
        conta["tipo"] = "corrente"
    contas.append(conta)

def entrar_conta():
    n_conta = int(input("Digite o numero da conta: "))

    for conta in contas:
        if n_conta == conta["n_conta"]:
            senha = int(input("digite a senha da conta: "))
            if senha == conta["senha"]:
                menu_entrar(conta)
            else:
                print("Senha inválida!")
                break
    else:
        print("Numero da conta não existe!")

def registro_mov(mov):
    registro = {}
    registro["Saques"] = []
    registro["Depositos"] = []
    registro["Movimento_Total"] = 0



    

def menu_entrar(conta):
    while True:
        print(f"Nº da conta: {conta['n_conta']}")
        print(f"Nome do Correntista: {conta['nome']}")
        print(f"Tipo: {conta['tipo']}")
        print(f"saldo atual: R${conta['saldo']}")
        print("1 - Saque")
        print("2 - Deposito")
        print("3 - Editar conta")
        print("4 - Excluir conta")
        print("5 - Sair")
        opcao2 = int(input("Opção: "))
        match opcao2:
            case 1:
                print(f'Seu saldo atual é: R${conta["saldo"]}')
                saque = float(input("Valor do saque: "))
                if saque > conta["saldo"] or conta["saldo"] <= 0:
                    print("Você não possui saldo o suficiente")
                    continue
                elif saque < 0:
                    print("Saque inválido")
                    continue
                conta["saldo"] = conta["saldo"] - saque
                print("Realizado com sucesso!")
            case 2:
                print(f'Seu saldo atual é: R${conta["saldo"]}')
                deposito = float(input("Valor do deposito"))
                conta["saldo"] = conta["saldo"] + deposito
                print("Realizado com sucesso!")
            case 3:
                print("1 - Nome")
                print("2 - Senha")
                print("3 - Nº da conta")
                print("4 - Tipo da conta")
                print("5 - Sair")
                opcao3 = int(input("Opcão: "))
                match opcao3:
                    case 1:
                        conta["nome"] = input("Novo nome da conta: ")
                        print("feito com sucesso")
                    case 2:
                        conta["senha"] = int(input("Nova senha da conta: "))
                        print("Feito com sucesso")
                    case 3:
                        conta["n_conta"] = int(input("Novo numero da conta: "))
                        print("Feito com sucesso!")
                    case 4:
                        tipo = input("Poupança: p, Corrente: c ")
                        if tipo == "p":
                            conta["tipo"] = "poupanca"
                        elif tipo == "c":
                            conta["tipo"] = "corrente"
                        print("Feito com sucesso!")
                    case 5:
                        break  
            case 4:
                ctz = input("Tem certeza que deseja excluir? S/N ")
                if ctz == "S":
                    contas.remove(conta)
                    break
            case 5: 
                break
def salvar(contas):
    dados = []
    for conta in contas:
        dados.append({
            "n_conta": conta["n_conta"], 
            "nome": conta["nome"],
            "data": conta["data"],
            "senha": conta["senha"],
            "tipo": conta["tipo"],
            "saldo": conta["saldo"]
        })
    with open("contas.json", "w") as arquivo:
        json.dump(dados,arquivo,indent=4)

def carregar_contas():
    try:
        with open("contas.json", "r") as arquivo:
            dados = json.load(arquivo)
        return dados
    except FileNotFoundError:
        # Se o arquivo não existir, retornamos uma lista vazia
        return []


registros = []
contas = carregar_contas()
opcao = None
while True:
    salvar(contas)
    print("1 - Entrar na conta")
    print("2 - Cadastrar conta")
    print("3 - Sair")
    opcao = int(input("Opção: "))
    match opcao:
        case 1:
            entrar_conta()

        case 2:
            cadastrar_contas(contas)
        case 3:
            break
