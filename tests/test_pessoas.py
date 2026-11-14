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

    def test_emails_malformados_sao_rejeitados(self):
        for email in ('a@@exemplo.com', 'usuario@', 'usuario exemplo@dominio.com',
                      'x@dominio', '.x@exemplo.com', 'x..y@exemplo.com',
                      'x@-exemplo.com', 'x@exemplo..com'):
            with self.subTest(email=email):
                with self.assertRaises(ErroValidacao):
                    self.servico.cadastrar('Pessoa Teste', email)

    def test_email_e_normalizado_e_indice_unico_o_bloqueia(self):
        codigo = self.servico.cadastrar('Pessoa Teste', '  TESTE@EXEMPLO.COM  ')
        self.assertEqual('teste@exemplo.com', self.servico.consultar(codigo)['email'])
        with self.assertRaises(ErroValidacao):
            self.servico.cadastrar('Outra Pessoa', 'teste@exemplo.com')
