<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banco</title>
</head>
<body>
    <h1>Banco - Pessoas cadastradas</h1>
    <p>Usuário autenticado: {{current_user.username}}</p>

    <table border="1" cellpadding="6">
        <tr><th>ID</th><th>Nome</th><th>Idade</th></tr>
        % for pessoa in pessoas:
        <tr>
            <td>{{pessoa.id}}</td>
            <td>{{pessoa.nome}}</td>
            <td>{{pessoa.idade}}</td>
        </tr>
        % end
    </table>
</body>
</html>
