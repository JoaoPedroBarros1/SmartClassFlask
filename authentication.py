import jwt
from config import SECRET_KEY
from flask import jsonify, request


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
        return jsonify({'mensagem': 'Token de autenticação necessário'}), 401

    token = remove_bearer(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        id_usuario = payload['id_usuario']
        if id_usuario:
            return jsonify({'mensagem': 'Token resgatado com sucesso', 'id_usuario': id_usuario}), 200
        else:
            return jsonify({'mensagem': 'Usuário não está logado'}), 401

    except jwt.ExpiredSignatureError:
        return jsonify({'mensagem': 'Token expirado'}), 401

    except jwt.InvalidTokenError:
        return jsonify({'mensagem': 'Token inválido'}), 401


def check_if_allowed(cargo="Coordenador"):
    response = get_user_login()
    print(response[0].__dir__())
    if response[1] != 200:
        return response[0]

    return response
    # user = Usuario.query.filter_by(id=response.id_usuario)
