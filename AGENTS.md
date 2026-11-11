# Orientações para assistentes de desenvolvimento

Este repositório é um laboratório **Python 3 + SQLite** e não um sistema de produção. Leia `README.md`, `docs/REQUISITOS.md` e `docs/ARQUITETURA.md` antes de modificar o código.

- Preserve a separação CLI → serviço → repositório.
- Use nomes claros em português, SQL parametrizado e transações.
- Nunca versionar bancos locais, senhas, tokens ou dados pessoais.
- Não introduza dependências externas sem necessidade.
- Execute `python -m unittest discover -s tests -v` antes de afirmar que a alteração funciona.
- Não confunda funcionalidades propostas em UML com código implementado.
