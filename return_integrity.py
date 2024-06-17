from functools import wraps
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
                        return jsonify(
                            mensagem="Dias de trabalho inválidos, você inseriu um número maior que 127?"
                        ), 400

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
