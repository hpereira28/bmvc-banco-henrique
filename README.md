# Sistema BMVC: portal e banco (Pessoa)

Sistema desenvolvido a partir do framework BMVC (Bottle + MVC), mantendo a mesma arquitetura: as rotas ficam em `route.py`, o controlador `Application` (`app/controllers/application.py`) administra as páginas pelo dicionário `pages` e compõe um objeto `DataRecord` (`app/controllers/datarecord.py`), que persiste os modelos em arquivos JSON na pasta `app/controllers/db`; os modelos `UserAccount` e `Pessoa` ficam em `app/models` e as páginas `.tpl` em `app/views/html`. O recurso **portal** faz o login dos usuários (modelo `UserAccount`): ao autenticar, o `DataRecord` gera um `session_id` com `uuid` e o controlador o grava em um cookie, que passa a identificar o usuário. O recurso **banco** só responde a usuários autenticados e apresenta a lista de objetos cadastrados, com o tema `Pessoa` (atributos nome e idade); o READ é feito no próprio sistema, na página `/banco`, enquanto o CREATE (`POST /banco`) e o DELETE (`DELETE /banco/<id>`) são feitos via cURL no terminal Linux, enviando o cookie da sessão obtido no login do portal.

## Como executar

```bash
pip install bottle
python3 route.py
```

Abra http://localhost:8080/portal e entre com `admin` / `admin`. Depois do login, `/banco` mostra as pessoas cadastradas.

## CREATE e DELETE via cURL

```bash
# login no portal (guarda o cookie de sessão)
curl -c cookies.txt -d "username=admin&password=admin" http://localhost:8080/portal

# CREATE
curl -b cookies.txt -X POST -d "nome=Ana&idade=30" http://localhost:8080/banco

# DELETE
curl -b cookies.txt -X DELETE http://localhost:8080/banco/1
```
