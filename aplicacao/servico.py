"""Validação de entradas e casos de uso."""
import sqlite3
import re
from aplicacao.repositorio import RepositorioPessoas

class ErroValidacao(ValueError):
    pass

class ServicoPessoas:
    def __init__(self, repositorio: RepositorioPessoas):
        self.repositorio = repositorio
        self.repositorio.preparar()

    @staticmethod
    def _validar(nome, email):
        nome, email = nome.strip(), email.strip().lower()
        if not 2 <= len(nome) <= 120:
            raise ErroValidacao('O nome deve ter entre 2 e 120 caracteres.')
        local = email.split('@', 1)[0]
        if (not 6 <= len(email) <= 254 or '..' in email or local.startswith('.') or local.endswith('.')
                or not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+", email)):
            raise ErroValidacao('Informe um email valido.')
        return nome, email

    def cadastrar(self, nome, email):
        nome, email = self._validar(nome, email)
        try:
            return self.repositorio.cadastrar(nome, email)
        except sqlite3.IntegrityError as erro:
            raise ErroValidacao('Email ja cadastrado.') from erro

    def atualizar(self, identificador, nome, email):
        nome, email = self._validar(nome, email)
        try:
            return self.repositorio.atualizar(identificador, nome, email)
        except sqlite3.IntegrityError as erro:
            raise ErroValidacao('Email ja cadastrado.') from erro

    def listar(self): return self.repositorio.listar()
    def consultar(self, identificador): return self.repositorio.consultar(identificador)
    def excluir(self, identificador): return self.repositorio.excluir(identificador)
