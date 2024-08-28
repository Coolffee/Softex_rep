from banco import Banco

def main():
    banco = Banco()
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
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
