# Controle documental — banco-de-dados

Versão inicial: **1.0.0**, em 11/11/2026. Código auditado: `388ff5f952d55b4511a186667b9f4f745076e013`.

| ID | Arquivo | Versão | Motivo |
|---|---|---|---|
| DB-ESTUDO-PROJ | [Projeto](../projeto/ESPECIFICACAO.md) | 2.0.0 | Faixa de IDs aceita no serviço e erro de uso do CLI |
| DB-ESTUDO-UML | [Arquitetura/UML](../uml/README.md) | 1.0.0 | Componentes, dados, fluxos |
| DB-ESTUDO-TST | [Plano de testes](../testes/PLANO_DE_TESTES.md) | 1.1.0 | Casos DB-T16–18 para o limite de IDs |

### Revisão de 24/11/2026

O contrato de IDs passou a explicitar a faixa suportada pelo SQLite e a rejeição de valores fora dela, com código 2 no CLI. O plano recebeu três casos de regressão. Na revisão de código `b78ac934bdeda24e07106fabaf4a08608e85c6cb`, Python 3.11.9 executou `python -m unittest discover -s tests -v` com 13 testes aprovados e `python -m compileall -q principal.py aplicacao tests` sem erros.

### Regras
Versão **MAJOR** quando o contrato mudar; **MINOR** para casos/fluxos novos; **PATCH** para correções editoriais. Cada PR que alterar comportamento deve atualizar os documentos afetados e registrar o SHA testado e evidências, nunca substituir execução por proposta.
