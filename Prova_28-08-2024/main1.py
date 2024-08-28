from banco import Banco

# Função principal que serve como ponto de entrada do programa
def main():
    banco = Banco()  # Cria uma instância da classe Banco
    while True:  # Loop infinito para o menu principal
        # Exibe as opções do menu para o usuário
        print("\n1 - Entrar na conta")
        print("2 - Cadastrar conta")
        print("3 - Sair")
        # Captura a opção escolhida pelo usuário
        opcao = int(input("Opção: "))
        
        if opcao == 1:  # Se a opção for "Entrar na conta"
            banco.entrar_conta()  # Chama o método para login na conta bancária
        elif opcao == 2:  # Se a opção for "Cadastrar conta"
            banco.cadastrar_conta()  # Chama o método para cadastrar uma nova conta bancária
        elif opcao == 3:  # Se a opção for "Sair"
            break  # Sai do loop e encerra o programa
        else:  # Se o usuário digitar uma opção inválida
            print("Opção inválida!")  # Informa o usuário sobre a opção inválida

# Verifica se este arquivo está sendo executado diretamente
if __name__ == "__main__":
    main()  # Chama a função principal
