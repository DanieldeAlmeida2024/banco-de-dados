import sqlite3
import tempfile
import unittest
from pathlib import Path
from aplicacao.repositorio import RepositorioPessoas
from aplicacao.servico import ErroValidacao, ServicoPessoas

class PersistenciaSegura(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = RepositorioPessoas(str(Path(self.tmp.name) / 'teste.db'))
        self.servico = ServicoPessoas(self.repo)
    def tearDown(self):
        self.tmp.cleanup()

    def test_booleano_nao_e_identificador_um(self):
        pk = self.servico.cadastrar('Pessoa Teste', 'pessoa@example.com')
        self.assertEqual(1, pk)
        for value in (True, False, 0, -1, '1', 1.0, None):
            with self.subTest(value=value):
                for func in (lambda: self.servico.consultar(value),
                             lambda: self.servico.excluir(value),
                             lambda: self.servico.atualizar(value, 'Novo nome', 'novo@example.com')):
                    with self.assertRaises(ErroValidacao):
                        func()
        self.assertIsNotNone(self.servico.consultar(pk))

    def test_tipos_invalidos_produzem_erro_de_dominio(self):
        for nome, email in ((None, 'pessoa@example.com'),
                            ('Pessoa Teste', None),
                            (23, 'pessoa@example.com')):
            with self.assertRaises(ErroValidacao):
                self.servico.cadastrar(nome, email)

    def test_memoria_e_reutilizada_durante_vida_da_instancia(self):
        repo = RepositorioPessoas(':memory:')
        try:
            s = ServicoPessoas(repo)
            pk = s.cadastrar('Pessoa Memoria', 'memoria@example.com')
            self.assertEqual('Pessoa Memoria', s.consultar(pk)['nome'])
            self.assertEqual(1, len(s.listar()))
        finally:
            repo.fechar()

    def test_conexao_arquivo_fecha_apos_sucesso_e_erro(self):
        with self.repo._sessao() as conn:
            self.assertEqual(1, conn.execute('SELECT 1').fetchone()[0])
        with self.assertRaises(sqlite3.ProgrammingError):
            conn.execute('SELECT 1')
        with self.assertRaises(RuntimeError):
            with self.repo._sessao() as failed:
                failed.execute('INSERT INTO pessoas(nome,email) VALUES (?,?)',
                               ('Rollback', 'rollback@example.com'))
                raise RuntimeError('excecao sintética')
        with self.assertRaises(sqlite3.ProgrammingError):
            failed.execute('SELECT 1')
        self.assertEqual([], self.servico.listar())
