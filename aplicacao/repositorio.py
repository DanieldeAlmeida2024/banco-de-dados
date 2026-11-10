"""Persistência SQLite; consultas parametrizadas."""
import sqlite3
from pathlib import Path

class RepositorioPessoas:
    def __init__(self, caminho_banco: str):
        self.caminho_banco = str(caminho_banco)
        if self.caminho_banco != ':memory:':
            Path(self.caminho_banco).parent.mkdir(parents=True, exist_ok=True)

    def _conectar(self):
        conexao = sqlite3.connect(self.caminho_banco)
        conexao.row_factory = sqlite3.Row
        conexao.execute('PRAGMA foreign_keys = ON')
        return conexao

    def preparar(self):
        with self._conectar() as conexao:
            conexao.execute('''CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL CHECK(length(nome) > 0),
                email TEXT NOT NULL UNIQUE
            )''')

    def cadastrar(self, nome, email):
        with self._conectar() as conexao:
            return int(conexao.execute('INSERT INTO pessoas (nome, email) VALUES (?, ?)', (nome, email)).lastrowid)

    def listar(self):
        with self._conectar() as conexao:
            return [dict(x) for x in conexao.execute('SELECT id, nome, email FROM pessoas ORDER BY id').fetchall()]

    def consultar(self, identificador):
        with self._conectar() as conexao:
            linha = conexao.execute('SELECT id, nome, email FROM pessoas WHERE id = ?', (identificador,)).fetchone()
            return dict(linha) if linha else None

    def atualizar(self, identificador, nome, email):
        with self._conectar() as conexao:
            return conexao.execute('UPDATE pessoas SET nome = ?, email = ? WHERE id = ?', (nome, email, identificador)).rowcount == 1

    def excluir(self, identificador):
        with self._conectar() as conexao:
            return conexao.execute('DELETE FROM pessoas WHERE id = ?', (identificador,)).rowcount == 1
