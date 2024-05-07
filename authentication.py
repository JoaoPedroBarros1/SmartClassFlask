import jwt
from config import SECRET_KEY
from flask import request


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
        if id_usuario:
            return {'mensagem': 'Token resgatado com sucesso', 'id': id_usuario}
        else:
            return {'mensagem': 'Usuário não está logado'}

    except jwt.ExpiredSignatureError:
        return {'mensagem': 'Token expirado'}

    except jwt.InvalidTokenError:
        return {'mensagem': 'Token inválido'}


def is_allowed(cargo="Coordenador"):
    response = get_user_login()
    for keys in response.keys():
        if 'id' == keys:
            break
    else:
        return {'allowed': False, 'mensagem': response['mensagem']}

    return {'allowed': True, 'mensagem': response['mensagem'], 'id': response['id']}
