from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

# Recurso PORTAL: login de usuários (modelo UserAccount)

@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')


@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id = ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, max_age=3600)
        if ctl.is_browser():
            redirect('/banco')
        return 'Login realizado\n'
    if ctl.is_browser():
        redirect('/portal')
    response.status = 401
    return 'Usuário ou senha inválidos\n'


# Recurso BANCO: lista de objetos cadastrados (modelo Pessoa)
#   GET    /banco       READ   (no próprio sistema)
#   POST   /banco       CREATE (via cURL)
#   DELETE /banco/<id>  DELETE (via cURL)

@app.route('/banco', method='GET')
def action_banco():
    if not ctl.is_authenticated():
        return ctl.not_authenticated()
    return ctl.render('banco')


@app.route('/banco', method='POST')
def action_banco_create():
    if not ctl.is_authenticated():
        return ctl.not_authenticated()
    nome = request.forms.get('nome')
    idade = request.forms.get('idade')
    return ctl.create_pessoa(nome, idade)


@app.route('/banco/<id:int>', method='DELETE')
def action_banco_delete(id):
    if not ctl.is_authenticated():
        return ctl.not_authenticated()
    return ctl.delete_pessoa(id)


#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
