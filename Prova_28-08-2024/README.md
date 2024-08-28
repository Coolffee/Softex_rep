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
