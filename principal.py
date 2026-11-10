"""CLI para estudos de persistencia: python principal.py --help."""
import argparse
import json
import os
from aplicacao.repositorio import RepositorioPessoas
from aplicacao.servico import ServicoPessoas, ErroValidacao

def executar(argumentos=None):
    parser = argparse.ArgumentParser(description='Laboratorio de CRUD com SQLite')
    parser.add_argument('--banco', default=os.environ.get('BANCO_ESTUDOS', 'dados/estudos.sqlite3'))
    comandos = parser.add_subparsers(dest='comando', required=True)
    criar = comandos.add_parser('cadastrar'); criar.add_argument('--nome', required=True); criar.add_argument('--email', required=True)
    comandos.add_parser('listar')
    consultar = comandos.add_parser('consultar'); consultar.add_argument('id', type=int)
    atualizar = comandos.add_parser('atualizar'); atualizar.add_argument('id', type=int); atualizar.add_argument('--nome', required=True); atualizar.add_argument('--email', required=True)
    excluir = comandos.add_parser('excluir'); excluir.add_argument('id', type=int)
    args = parser.parse_args(argumentos)
    servico = ServicoPessoas(RepositorioPessoas(args.banco))
    try:
        if args.comando == 'cadastrar': resposta = {'id': servico.cadastrar(args.nome, args.email)}
        elif args.comando == 'listar': resposta = servico.listar()
        elif args.comando == 'consultar': resposta = servico.consultar(args.id)
        elif args.comando == 'atualizar': resposta = {'atualizado': servico.atualizar(args.id, args.nome, args.email)}
        else: resposta = {'excluido': servico.excluir(args.id)}
    except ErroValidacao as erro:
        parser.error(str(erro))
    print(json.dumps(resposta, ensure_ascii=False, indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(executar())
