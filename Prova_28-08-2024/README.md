# Sistema Bancário

## Configuração do Banco de Dados

Para configurar o banco de dados para este projeto, siga estas etapas:

1. Instale o MySQL em sua máquina, se ainda não o tiver feito.

2. Abra um cliente MySQL (como MySQL Workbench ou o cliente de linha de comando).

3. Execute o script SQL fornecido no arquivo `init_database.sql` (na pasta instruções). Você pode fazer isso de duas maneiras:
   
   a. No MySQL Workbench, abra o arquivo `init_database.sql` e execute-o.
   
   b. Na linha de comando, use:
      ```
      mysql -u seu_usuario -p < init_database.sql
      ```

4. Verifique se o banco de dados 'banco' foi criado e se as tabelas 'contas' e 'movimentacoes' estão presentes.

5. Atualize o arquivo `config.py` com suas credenciais de banco de dados:

   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'database': 'banco',
       'user': 'seu_usuario',
       'password': 'sua_senha'
   }
   ```

Agora você deve estar pronto para executar o sistema bancário com o banco de dados configurado corretamente.


## Estrutura do Projeto
O projeto está dividido em vários arquivos Python, cada um com uma responsabilidade específica:

1. `main1.py`: Ponto de entrada do programa, gerencia o menu principal.
2. `banco.py`: Implementa a classe `Banco`, que contém a lógica principal do sistema.
3. `conta.py`: Define a classe `ContaBancaria` para representar contas individuais.
4. `database.py`: Contém a classe `DatabaseManager` para gerenciar conexões e operações do banco de dados.
5. `config.py`: Armazena as configurações de conexão com o banco de dados MySQL.

## Principais Funcionalidades

### Classe Banco (`banco.py`)
- Cadastro de novas contas
- Login em contas existentes
- Operações bancárias: saque, depósito, edição de conta, exclusão de conta, extrato
- Gerenciamento de conexão com o banco de dados

### Classe ContaBancaria (`conta.py`)
- Representa uma conta bancária individual
- Armazena informações como número da conta, nome do titular, data de abertura, tipo de conta, senha e saldo
- Métodos para converter entre objetos e dicionários

### DatabaseManager (`database.py`)
- Gerencia a conexão com o banco de dados MySQL
- Cria as tabelas necessárias (contas e movimentações)

### Menu Principal (`main1.py`)
- Interface de usuário baseada em console
- Opções para entrar na conta, cadastrar nova conta ou sair do programa

## Banco de Dados
- Utiliza MySQL
- Duas tabelas principais: `contas` e `movimentacoes`
- Configurações de conexão armazenadas em `config.py`

## Características do Sistema
- Validação de entradas do usuário
- Tratamento de erros para operações de banco de dados
- Uso de transações para garantir a integridade dos dados
- Senhas armazenadas como texto simples (não é uma prática segura em ambiente de produção)
- Suporte para diferentes tipos de conta (poupança e corrente)
