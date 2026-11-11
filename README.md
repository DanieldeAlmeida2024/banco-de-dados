# Banco de dados — laboratório de CRUD com SQLite

Projeto didático de persistência relacional em **Python 3.10+**, com operações de cadastro de pessoas e banco SQLite local. A implementação não requer serviços externos.

## Funcionalidades

- Criar tabela `pessoas` automaticamente.
- Cadastrar, consultar, listar, atualizar e excluir pessoas.
- Validar nome/e-mail; e-mail único; parâmetros SQL em todas as consultas.
- Banco em `dados/estudos.sqlite3` (não versionado).

## Executar

```powershell
python principal.py cadastrar --nome "Ana Silva" --email "ana@exemplo.com"
python principal.py listar
python principal.py consultar 1
python principal.py atualizar 1 --nome "Ana Souza" --email "ana@exemplo.com"
python principal.py excluir 1
```

Use `--banco caminho/arquivo.sqlite3` **antes** do subcomando para selecionar outro arquivo.

## Testar

```powershell
python -m unittest discover -s tests -v
```

## Estrutura

- `principal.py`: CLI.
- `aplicacao/servico.py`: validação e regras.
- `aplicacao/repositorio.py`: acesso SQLite com SQL parametrizado.
- `tests/test_pessoas.py`: testes funcionais.
- `docs/REQUISITOS.md`, `docs/ARQUITETURA.md`, `docs/UML.puml`, `docs/PLANO_TESTES.md`: especificações.
- `AGENTS.md`: regras para assistentes de código.

**Estado:** laboratório de uso local. Não oferece autenticação, criptografia do arquivo, API HTTP nem controle de acesso multiusuário.
