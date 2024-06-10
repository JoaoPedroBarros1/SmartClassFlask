import jwt
from functools import wraps
from config import SECRET_KEY
from flask import request, jsonify, g
from models import Usuario, CargoChoices
from return_dicts import return_aluno, return_professor, return_coordenador


def _remove_bearer(token):
    if token.startswith('Bearer '):
        return token[len('Bearer '):]
    else:
        return token


def _get_user_login() -> dict:
    token = request.headers.get('Authorization')
    if not token:
        return {'sucesso': False, 'mensagem': 'Token de autenticação necessário'}

    token = _remove_bearer(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        id_usuario = payload['id_usuario']

        if not id_usuario:
            return {'sucesso': False, 'mensagem': 'ID não enviado'}

        user = Usuario.query.filter_by(id=id_usuario).first()
        if not user:
            return {'sucesso': False, 'mensagem': 'Usuário não existe'}

        return {'sucesso': True, 'mensagem': 'Usuário encontrado', 'user': user}

    except jwt.ExpiredSignatureError:
        return {'sucesso': False, 'mensagem': 'Token expirado'}

    except jwt.InvalidTokenError:
        return {'sucesso': False, 'mensagem': 'Token inválido'}


def login_required(func):
    @wraps(func)
    def login_wrap(*args, **kwargs):
        response = _get_user_login()
        if not response['sucesso']:
            return jsonify(mensagem=response['mensagem']), 401

        user = response['user']
        user_cargo_value = user.cargo.value

        usuario_dict = {}
        access = False

        match user_cargo_value:
            case CargoChoices.Professor.value:
                usuario_dict.update(return_professor(user.professor, False, True))

            case CargoChoices.Coordenador.value:
                usuario_dict.update(return_coordenador(user.coordenador, True))
                access = True

            case CargoChoices.Aluno.value:
                usuario_dict.update(return_aluno(user.aluno, False, True))

        g.mensagem = response['mensagem']
        g.usuario = usuario_dict
        g.is_admin = access
        return func(*args, **kwargs)
    return login_wrap


def admin_required(func):
    @wraps(func)
    def admin_wrap(*args, **kwargs):
        if not g.is_admin:
            return jsonify(mensagem="Necessário ter cargo de coordenador"), 403
        return func(*args, **kwargs)
    return admin_wrap
