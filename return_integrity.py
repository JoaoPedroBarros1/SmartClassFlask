from functools import wraps
from typing import Literal
from models import *
from flask import jsonify, request, g


def check_integrity(requirements: set):
    def integrity_decorator(func):
        @wraps(func)
        def integrity_wrap(*args, **kwargs):
            g.data_request = request.json
            req_difference = requirements.difference(set(g.data_request.keys()))
            if req_difference:
                return jsonify(mensagem="Valores necessários não foram enviados"), 400

            return func(*args, **kwargs)
        return integrity_wrap
    return integrity_decorator


def check_cargo_post(prof_req: set):
    def cargo_decorator(func):
        @wraps(func)
        def cargo_wrap(*args, **kwargs):
            g.data_request = request.json
            match g.data_request['cargo'].upper():
                case CargoChoices.Coordenador.value:
                    pass

                case CargoChoices.Professor.value:
                    req_difference = prof_req.difference(set(g.data_request.keys()))
                    if req_difference:
                        return jsonify(mensagem="Valores do cargo não foram enviados"), 400

                    if g.data_request['start_turno'] >= g.data_request['end_turno']:
                        return jsonify(mensagem="Horário que curso termina é menor que quando começa"), 400

                    if not 1 <= int(g.data_request['dias_da_semana']) <= 127:
                        return jsonify(mensagem="Dias de trabalho inválidos, você inseriu um número maior que 127?"), 400

                case CargoChoices.Aluno.value:
                    pass

                case _:
                    return jsonify(mensagem="Cargo inválido"), 400

            return func(*args, **kwargs)
        return cargo_wrap
    return cargo_decorator


def check_cargo_put(func):
    @wraps(func)
    def cargo_wrap(*args, **kwargs):
        g.data_request = request.json
        match g.usuario['cargo'].upper():
            case CargoChoices.Coordenador.value:
                pass

            case CargoChoices.Professor.value:
                start_turno = g.usuario.start_turno
                end_turno = g.usuario.end_turno
                dias_da_semana = g.usuario.dias_da_semana.num
                if 'start_turno' in g.data_request:
                    start_turno = g.data_request['start_turno']
                if 'end_turno' in g.data_request:
                    end_turno = g.data_request['end_turno']
                if 'dias_da_semana' in g.data_request:
                    dias_da_semana = g.data_request['dias_da_semana']

                if start_turno >= end_turno:
                    return jsonify(mensagem="Horário que curso termina é menor que quando começa"), 400

                if not 1 <= int(dias_da_semana) <= 127:
                    return jsonify(mensagem="Dias de trabalho inválidos, você inseriu um número maior que 127?"), 400

            case CargoChoices.Aluno.value:
                pass

            case _:
                return jsonify(mensagem="Cargo inválido"), 400

        return func(*args, **kwargs)
    return cargo_wrap


def _check_login(login_request: dict) -> dict:
    # FEITO
    for valor in login_request.values():
        if len(valor) == 0:
            return {'allowed': False, 'mensagem': 'Algum dos valores é nulo'}

    _POST_ = {"email", "senha"}
    _SET_ = set(login_request.keys())

    post_difference = _POST_.difference(_SET_)
    if post_difference:
        return {'allowed': False, 'mensagem': 'Valores não coincidem'}

    return {'allowed': True}


def _check_sala(sala_request: dict, method: Literal["POST", "PUT"]) -> dict:
    for valor in sala_request.values():
        if len(valor) == 0:
            return {'allowed': False, 'mensagem': 'Algum dos valores é nulo'}

    _POST_ = {"", ""}
    _PUT_ = {"", ""}
    _SET_ = set(sala_request.keys())

    match method:
        case "POST":
            post_difference = _POST_.difference(_SET_)
            if post_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

        case "PUT":
            put_difference = _PUT_.difference(_SET_)
            if put_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

    return {'allowed': True}


def _check_usuario(usuario_request: dict, method: Literal["POST", "PUT"]) -> dict:
    for valor in usuario_request.values():
        if len(valor) == 0:
            return {'allowed': False, 'mensagem': 'Algum dos valores é nulo'}

    _POST_ = {"email", "senha", "nome"}
    _PUT_ = {"", ""}
    _SET_ = set(usuario_request.keys())

    match method:
        case "POST":
            post_difference = _POST_.difference(_SET_)
            if post_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

        case "PUT":
            put_difference = _PUT_.difference(_SET_)
            if put_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

    return {'allowed': True}


def _check_curso(curso_request: dict, method: Literal["POST", "PUT"]) -> dict:
    # Verificar se a aula já não está sendo utilizada por outro curso
    # Verificar se o professor já não está ocupado por outro curso no mesmo horário
    # Verificar se o horário de aula do aluno está dentro do horário de aula do prof

    for valor in curso_request.values():
        if len(valor) == 0:
            return {'allowed': False, 'mensagem': 'Algum dos valores é nulo'}

    _POST_ = {"", ""}
    _PUT_ = {"", ""}
    _SET_ = set(curso_request.keys())

    match method:
        case "POST":
            post_difference = _POST_.difference(_SET_)
            if post_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

        case "PUT":
            put_difference = _PUT_.difference(_SET_)
            if put_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

    return {'allowed': True}


def _check_emenda(emenda_request: dict, method: Literal["POST", "PUT"]) -> dict:
    for valor in emenda_request.values():
        if len(valor) == 0:
            return {'allowed': False, 'mensagem': 'Algum dos valores é nulo'}

    _POST_ = {"", ""}
    _PUT_ = {"", ""}
    _SET_ = set(emenda_request.keys())

    match method:
        case "POST":
            post_difference = _POST_.difference(_SET_)
            if post_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

        case "PUT":
            put_difference = _PUT_.difference(_SET_)
            if put_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

    return {'allowed': True}


def _check_feriado(feriado_request: dict, method: Literal["POST", "PUT"]) -> dict:
    for valor in feriado_request.values():
        if len(valor) == 0:
            return {'allowed': False, 'mensagem': 'Algum dos valores é nulo'}

    _POST_ = {"", ""}
    _PUT_ = {"", ""}
    _SET_ = set(feriado_request.keys())

    match method:
        case "POST":
            post_difference = _POST_.difference(_SET_)
            if post_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

        case "PUT":
            put_difference = _PUT_.difference(_SET_)
            if put_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

    return {'allowed': True}


def _check_reposicao(reposicao_request: dict, method: Literal["POST", "PUT"]) -> dict:
    # Não pode ser colocada em um dia que já tem um curso ocupado
    # Não pode ser colocada em um dia de feriado

    for valor in reposicao_request.values():
        if len(valor) == 0:
            return {'allowed': False, 'mensagem': 'Algum dos valores é nulo'}

    _POST_ = {"", ""}
    _PUT_ = {"", ""}
    _SET_ = set(reposicao_request.keys())

    match method:
        case "POST":
            post_difference = _POST_.difference(_SET_)
            if post_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

        case "PUT":
            put_difference = _PUT_.difference(_SET_)
            if put_difference:
                return {'allowed': False, 'mensagem': 'Valores não coincidem'}

    return {'allowed': True}


def _check_matricula(matricula_request: dict) -> dict:
    # FEITO
    for valor in matricula_request.values():
        if len(valor) == 0:
            return {'allowed': False, 'mensagem': 'Algum dos valores é nulo'}

    _POST_ = {"id_usuario", "id_curso"}
    _SET_ = set(matricula_request.keys())

    post_difference = _POST_.difference(_SET_)
    if post_difference:
        return {'allowed': False, 'mensagem': 'Valores não coincidem'}

    local_aluno: Aluno = Aluno.query.filter_by(id=matricula_request['id_usuario']).first()
    if not local_aluno:
        return {'allowed': False, 'mensagem': 'Aluno não encontrado'}

    local_curso: Curso = Curso.query.filter_by(id=matricula_request['id_curso']).first()
    if not local_curso:
        return {'allowed': False, 'mensagem': 'Curso não encontrado'}

    if local_curso in local_aluno.cursos:
        return {'allowed': False, 'mensagem': 'Aluno já cadastrado no curso'}

    return {'allowed': True, 'curso': local_curso, 'aluno': local_aluno}
