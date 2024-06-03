from typing import Literal
from models import *


def check_login(login_request: dict) -> dict:
    return {'allowed': True}


def check_sala(sala_request: dict, method: Literal["POST", "PUT"]) -> dict:
    return {'allowed': True}


def check_usuario(usuario_request: dict, method: Literal["POST", "PUT"]) -> dict:
    return {'allowed': True}


def check_aluno(aluno_request: dict, method: Literal["POST", "PUT"]) -> dict:
    return {'allowed': True}


def check_professor(professor_request: dict, method: Literal["POST", "PUT"]) -> dict:
    # Checar se o valor do dias_da_semana é 1 <= x <= 127
    # Checar se o start_turno é menor que o end_turno

    return {'allowed': True}


def check_coordenador(coordenador_request: dict, method: Literal["POST", "PUT"]) -> dict:
    return {'allowed': True}


def check_curso(curso_request: dict, method: Literal["POST", "PUT"]) -> dict:
    # Verificar se a aula já não está sendo utilizada por outro curso
    # Verificar se o professor já não está ocupado por outro curso no mesmo horário
    # Verificar se o horário de aula do aluno está dentro do horário de aula do prof

    return {'allowed': True}


def check_emenda(emenda_request: dict, method: Literal["POST", "PUT"]) -> dict:
    return {'allowed': True}


def check_feriado(feriado_request: dict, method: Literal["POST", "PUT"]) -> dict:
    return {'allowed': True}


def check_reposicao(reposicao_request: dict, method: Literal["POST", "PUT"]) -> dict:
    # Não pode ser colocada em um dia que já tem um curso ocupado
    # Não pode ser colocada em um dia de feriado

    return {'allowed': True}


def check_matricula(matricula_request: dict, method: Literal["POST", "PUT"]) -> dict:
    # Checar se o aluno já está cadastrado naquele curso

    return {'allowed': True}
