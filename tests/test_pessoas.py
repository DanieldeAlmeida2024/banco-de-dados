import tempfile
import unittest
from pathlib import Path
from aplicacao.repositorio import RepositorioPessoas
from aplicacao.servico import ErroValidacao, ServicoPessoas

class TestesPessoas(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.servico = ServicoPessoas(RepositorioPessoas(str(Path(self.tmp.name) / 'dados.sqlite3')))

    def tearDown(self): self.tmp.cleanup()

    def test_fluxo_crud(self):
        codigo = self.servico.cadastrar('Ana Silva', 'ANA@EXEMPLO.COM')
        self.assertEqual('ana@exemplo.com', self.servico.consultar(codigo)['email'])
        self.assertEqual(1, len(self.servico.listar()))
        self.assertTrue(self.servico.atualizar(codigo, 'Ana Souza', 'ana@exemplo.com'))
        self.assertEqual('Ana Souza', self.servico.consultar(codigo)['nome'])
        self.assertTrue(self.servico.excluir(codigo))
        self.assertIsNone(self.servico.consultar(codigo))

    def test_duplicidade(self):
        self.servico.cadastrar('Pessoa Um', 'pessoa@exemplo.com')
        with self.assertRaises(ErroValidacao): self.servico.cadastrar('Pessoa Dois', 'pessoa@exemplo.com')

    def test_parametrizacao_sql(self):
        codigo = self.servico.cadastrar("Teste'); DROP TABLE pessoas;--", 'teste@exemplo.com')
        self.assertIsNotNone(self.servico.consultar(codigo))
        self.assertEqual(1, len(self.servico.listar()))

    def test_nome_invalido(self):
        with self.assertRaises(ErroValidacao): self.servico.cadastrar(' ', 'email@exemplo.com')
