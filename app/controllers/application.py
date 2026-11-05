from app.controllers.datarecord import DataRecord
from bottle import template, redirect, request, response


class Application():

    def __init__(self):

        self.pages = {
            'portal': self.portal,
            'banco': self.banco
        }

        self.__model = DataRecord()


    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)


    def get_session_id(self):
        return request.get_cookie('session_id')


    # O navegador envia "Accept: text/html"; o cURL não.
    def is_browser(self):
        return 'text/html' in request.headers.get('Accept', '')


    def helper(self):
        return template('app/views/html/helper')


    # ---------------- recurso PORTAL ----------------

    def portal(self):
        return template('app/views/html/portal')


    def is_authenticated(self):
        session_id = self.get_session_id()
        return self.__model.getCurrentUser(session_id) is not None


    def authenticate_user(self, username, password):
        session_id = self.__model.checkUser(username, password)
        if session_id:
            self.logout_user()
            return session_id
        return None


    def logout_user(self):
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)


    def not_authenticated(self):
        if self.is_browser():
            redirect('/portal')
        response.status = 401
        return 'Não autenticado: faça login em /portal\n'


    # ---------------- recurso BANCO ----------------

    def banco(self):
        user = self.__model.getCurrentUser(self.get_session_id())
        pessoas = self.__model.getPessoas()
        return template('app/views/html/banco', current_user=user, pessoas=pessoas)


    def create_pessoa(self, nome, idade):
        if not nome or not idade:
            response.status = 400
            return 'Use: curl -b cookies.txt -X POST -d "nome=...&idade=..." http://localhost:8080/banco\n'
        pessoa = self.__model.addPessoa(nome, idade)
        return f'Pessoa criada com id {pessoa.id}\n'


    def delete_pessoa(self, id):
        if self.__model.deletePessoa(id):
            return f'Pessoa {id} removida\n'
        response.status = 404
        return f'Pessoa {id} não encontrada\n'
