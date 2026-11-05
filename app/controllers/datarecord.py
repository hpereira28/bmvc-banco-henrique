from app.models.user_account import UserAccount
from app.models.pessoa import Pessoa
import json
import uuid


class DataRecord():
    """Banco de dados JSON para os recursos Usuários e Pessoas"""

    def __init__(self):

        self.__user_accounts = []
        self.__authenticated_users = {}
        self.__pessoas = []
        self.read()


    def read(self):
        try:
            with open("app/controllers/db/user_accounts.json", "r") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            self.__user_accounts.append(UserAccount('admin', 'admin'))

        try:
            with open("app/controllers/db/pessoas.json", "r") as arquivo_json:
                pessoa_data = json.load(arquivo_json)
                self.__pessoas = [Pessoa(**data) for data in pessoa_data]
        except FileNotFoundError:
            self.__pessoas = []


    # ---------------- Usuários ----------------

    def getCurrentUser(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None


    def getUserName(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id].username
        else:
            return None


    def checkUser(self, username, password):
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                self.__authenticated_users[session_id] = user
                return session_id  # Retorna o ID de sessão para o usuário
        return None


    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]  # Remove o usuário logado


    # ---------------- Pessoas ----------------

    def getPessoas(self):
        return self.__pessoas


    def addPessoa(self, nome, idade):
        novo_id = max([p.id for p in self.__pessoas], default=0) + 1
        pessoa = Pessoa(novo_id, nome, int(idade))
        self.__pessoas.append(pessoa)
        self.__savePessoas()
        return pessoa


    def deletePessoa(self, id):
        for pessoa in self.__pessoas:
            if pessoa.id == id:
                self.__pessoas.remove(pessoa)
                self.__savePessoas()
                return True
        return False


    def __savePessoas(self):
        with open("app/controllers/db/pessoas.json", "w") as arquivo_json:
            pessoa_data = [vars(pessoa) for pessoa in self.__pessoas]
            json.dump(pessoa_data, arquivo_json, indent=4, ensure_ascii=False)
