# Laboratório SQLite — especificação funcional

> **Documento DB-ESTUDO-PROJ** | v1.0.0 | 2026-11-11 | Código `main` @ `388ff5f952d55b4511a186667b9f4f745076e013`
> Análise do código efetivo deste repositório; cenários “pendente” não representam testes executados.


## Finalidade
Aplicação de linha de comando para cadastrar, listar, consultar, atualizar e excluir pessoas. O processo grava os dados em um arquivo SQLite e oferece uma separação simples entre comando de entrada, validação e persistência.

## Fluxo implementado
1. `principal.py` interpreta `--banco` (padrão `dados/estudos.sqlite3`) e o subcomando.
2. `ServicoPessoas` chama `RepositorioPessoas.preparar()`; a tabela `pessoas` é criada se ainda não existir.
3. `ServicoPessoas._validar()` remove espaços das bordas do nome e e-mail e normaliza o e-mail para minúsculas.
4. O repositório usa `sqlite3` com parâmetros `?` em `INSERT`, `SELECT`, `UPDATE` e `DELETE`, retornando registros em dicionários.
5. A CLI apresenta JSON em UTF-8; erros de validação são repassados ao `argparse`.

## Contrato de dados
A tabela `pessoas` possui `id INTEGER PRIMARY KEY AUTOINCREMENT`, `nome TEXT NOT NULL CHECK(length(nome)>0)` e `email TEXT NOT NULL UNIQUE`. O serviço exige nome com 2–120 caracteres e e-mail com 3–254 caracteres contendo `@`. A verificação é propositalmente simples e **não comprova validade real de e-mails**.

| Comando | Entrada | Saída | Comportamento |
|---|---|---|---|
| `cadastrar` | `--nome`, `--email` | `{"id": ...}` | Restrições da tabela e validação do serviço |
| `listar` | nenhuma | vetor JSON | Ordenação crescente por ID |
| `consultar` | `id` | objeto ou `null` | Não encontrado não é exceção |
| `atualizar` | `id`, `--nome`, `--email` | `{"atualizado": bool}` | Retorna falso quando ID não existe |
| `excluir` | `id` | `{"excluido": bool}` | Retorna falso quando ID não existe |

## Exemplo reproduzível
```bash
python principal.py --banco dados/exemplo.sqlite3 cadastrar --nome "Ana Ribeiro" --email "ANA@EXEMPLO.COM"
python principal.py --banco dados/exemplo.sqlite3 listar
python -m unittest discover -s tests -v
```

## Restrições e decisões
- SQLite é adequado ao laboratório local, mas este exemplo **não** demonstra controle de acesso multiusuário, API REST ou migrações SQL versionadas.
- A unicidade de e-mail é confirmada pelo banco. Uma segunda inclusão é convertida para `ErroValidacao` pelo serviço.
- `PRAGMA foreign_keys=ON` está preparado para relacionamentos futuros, mas a tabela atual não possui chaves estrangeiras.
- Transações usam contexto `with`, com commits/rollbacks gerenciados pelo SQLite.
- A verificação de nome e e-mail deve evoluir quando houver novos requisitos, com testes antes da mudança.
