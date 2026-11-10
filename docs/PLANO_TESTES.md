# Plano de testes

| Caso | Verificação | Método |
|---|---|---|
| CT-01 | CRUD persistente | `TestesPessoas.test_fluxo_crud` |
| CT-02 | E-mail único | `test_duplicidade` |
| CT-03 | SQL parametrizado | `test_parametrizacao_sql` |
| CT-04 | Nome inválido | `test_nome_invalido` |

Executar: `python -m unittest discover -s tests -v`.

Limitação: estes testes não avaliam concorrência, latência, ataques de múltiplos usuários nem criptografia do arquivo.
