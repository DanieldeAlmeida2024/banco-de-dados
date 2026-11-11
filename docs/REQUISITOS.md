# Requisitos funcionais e não funcionais

## Escopo do laboratório
RF-01 Cadastrar pessoa com nome e email.
RF-02 Listar e consultar pessoas por identificador.
RF-03 Atualizar e excluir uma pessoa.
RF-04 Rejeitar nome inválido e e-mail duplicado.
RF-05 Persistir dados em arquivo SQLite configurável.

## Qualidade
RNF-01 Queries parametrizadas (evitar injeção SQL).
RNF-02 Validações separadas da infraestrutura.
RNF-03 Testes repetíveis e banco isolado por teste.
RNF-04 Não registrar dados de produção nem credenciais.

## Fora do escopo
API HTTP, acesso simultâneo distribuído, autenticação e deploy público.
