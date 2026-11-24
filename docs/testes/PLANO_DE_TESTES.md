# Laboratório SQLite — plano de testes

> **Documento DB-ESTUDO-TST** | v1.1.0 | 2026-11-24 | [Controle de versões](../controle/VERSIONAMENTO.md)
> Análise do código efetivo deste repositório; cenários “pendente” não representam testes executados.


## Suíte existente
`tests/test_pessoas.py` usa `unittest` e banco SQLite exclusivo por teste, criado dentro de `tempfile.TemporaryDirectory()`. Essa escolha evita dependência externa e não utiliza `dados/estudos.sqlite3` real.

| ID | Caso | Fonte automatizada | Aceitação |
|---|---|---|---|
| DB-T01 | Cadastrar, consultar, listar, atualizar e excluir | `test_fluxo_crud` | Registro percorre todo o ciclo e consulta final é `None` |
| DB-T02 | E-mail duplicado | `test_duplicidade` | `ErroValidacao` no segundo cadastro |
| DB-T03 | Tentativa de injeção em nome | `test_parametrizacao_sql` | Texto suspeito não é executado como SQL |
| DB-T04 | Nome só com espaços | `test_nome_invalido` | `ErroValidacao` |

## Cenários ainda não automatizados
| ID | Cenário | Resultado esperado |
|---|---|---|
| DB-T05 | Nome com exatamente 2 e 120 caracteres | Aceito |
| DB-T06 | Nome com 1 e 121 caracteres | Recusado |
| DB-T07 | E-mail normalizado em atualização | Retorno em minúsculas e sem espaços nas bordas |
| DB-T08 | Atualizar/excluir ID inexistente | `False`, sem criar registro |
| DB-T09 | Banco em caminho sem diretório | Diretório criado no `__init__` |
| DB-T10 | Persistência entre processos | Arquivo SQLite mantém dados após reiniciar o CLI |
| DB-T11 | Concorrência de gravações | Verificar lock/timeout; comportamento não prometido |

## Executar
```bash
python -m unittest discover -s tests -p "test_*.py" -v
python -m compileall -q principal.py aplicacao tests
```

## Critério de aceite
A suíte existente e os testes de regressão pertinentes devem passar. Não considerar validação simples de e-mail como verificação de propriedade do endereço. Evidência precisa registrar commit, comando e retorno da suíte.

## DB-T12–15 — regressões integradas (14/11/2026)

- DB-T12: impedir exclusão/edição do ID 1 com booleano `True` ou identificadores zero/negativos/não inteiros.
- DB-T13: nome/e-mail não textuais retornam `ErroValidacao`.
- DB-T14: conexão SQLite de arquivo é fechada após commit/rollback, inclusive exceção.
- DB-T15: SQLite em memória mantém dados entre operações da mesma instância até `fechar()`.

Executáveis em `tests/test_db_safety.py`. O escopo não inclui teste de concorrência multi-processo ou operação de produção.

## DB-T16–18 — limites do identificador SQLite

| ID | Caso | Aceitação |
|---|---|---|
| DB-T16 | Consultar, atualizar e excluir com ID 9223372036854775808 | O serviço retorna `ErroValidacao` nas três operações |
| DB-T17 | Consultar, atualizar e excluir um registro com ID 9223372036854775807 | As três operações funcionam e a consulta final retorna `None` |
| DB-T18 | Executar os três comandos do CLI com ID 9223372036854775808 | Código 2 e mensagem com o limite aceito, sem traceback |

Os casos estão em `tests/test_db_safety.py` e usam banco temporário ou em memória.
