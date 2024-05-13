import jwt
from config import SECRET_KEY
from flask import request
from models import Usuario


def remove_bearer(token):
    if token.startswith('Bearer '):
        return token[len('Bearer '):]
    else:
        return token


def generate_token(user_id):
    payload = {'id_usuario': user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def get_user_login():
    token = request.headers.get('Authorization')
    if not token:
        return {'mensagem': 'Token de autenticação necessário'}

    token = remove_bearer(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        id_usuario = payload['id_usuario']

        if not id_usuario:
            return {'mensagem': 'ID não enviado'}

        user = Usuario.query.filter_by(id=id_usuario).first()
        if not user:
            return {'mensagem': 'Usuário não existe'}

        return {'mensagem': 'Usuário encontrado', 'user': user}

    except jwt.ExpiredSignatureError:
        return {'mensagem': 'Token expirado'}

    except jwt.InvalidTokenError:
        return {'mensagem': 'Token inválido'}


def is_allowed(allowed_list: list):
    response = get_user_login()
    for keys in response.keys():
        if 'user' == keys:
            break
    else:
        return {'allowed': False, 'mensagem': response['mensagem']}

    user = response['user']

    user_cargo_value = user.cargo.value

    if user_cargo_value not in allowed_list:
        return {'allowed': False, 'mensagem': 'Usuário não possui cargo necessário'}

    usuario = {
        'email': user.nome,
        'senha': user.senha,
        'nome': user.nome,
        'cargo': user.cargo.name
    }
    return {'allowed': True, 'mensagem': response['mensagem'], 'usuario': usuario}
