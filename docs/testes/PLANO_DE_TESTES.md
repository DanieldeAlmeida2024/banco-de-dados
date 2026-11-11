# Laboratório SQLite — plano de testes

> **Documento DB-ESTUDO-TST** | v1.0.0 | 2026-11-11 | Código `main` @ `388ff5f952d55b4511a186667b9f4f745076e013`
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
Os quatro testes existentes devem passar; para evolução funcional, acrescentar testes dos limites e da persistência entre execuções. Não considerar validação simples de e-mail como verificação de propriedade do endereço. Evidência precisa registrar commit, comando e retorno da suíte.
