import jwt
from flask import jsonify, request
from config import SECRET_KEY


def remove_bearer(token):
    if token.startswith('Bearer '):
        return token[len('Bearer '):]
    else:
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
