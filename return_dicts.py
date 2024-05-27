from models import *


def return_sala(sala: Sala, public=True) -> dict:
    curso_list = []
    for curso in sala.cursos:
        curso_list.append(return_curso(curso, public))

    sala_dict = {
        'nome': sala.nome,
        'cursos': curso_list
    }

    if public:
        sala_dict.update({
            'id': sala.id
        })
    return sala_dict


def return_usuario(usuario: Usuario, public=True) -> dict:
    usuario_dict = {
        'nome': usuario.nome,
        'cargo': usuario.cargo.name
    }

    if public:
        usuario_dict.update({
            'id': usuario.id,
            'email': usuario.email,
            'senha': usuario.senha
        })
    return usuario_dict


def return_aluno(aluno: Aluno, public=True) -> dict:
    aluno_dict = {}

    if public:
        aluno_dict.update({
            'id': aluno.id
        })
    return aluno_dict


def return_professor(professor: Professor, public=True) -> dict:
    professor_dict = {}

    if public:
        professor_dict.update({
            'id': professor.id
        })
    return professor_dict


def return_coordenador(coordenador: Coordenador, public=True) -> dict:
    coordenador_dict = {}

    if public:
        coordenador_dict.update({
            'id': sala.id
        })
    return coordenador_dict


def return_curso(curso: Curso, public=True) -> dict:
    curso_dict = {}

    if public:
        curso_dict.update({
            'id': sala.id
        })
    return curso_dict


def return_naoletivo(naoletivo: NaoLetivo, public=True) -> dict:
    naoletivo_dict = {}

    if public:
        naoletivo_dict.update({
            'id': sala.id
        })
    return naoletivo_dict


def return_feriado(feriado: Feriado, public=True) -> dict:
    feriado_dict = {}

    if public:
        feriado_dict.update({
            'id': sala.id
        })
    return feriado_dict


def return_reposicao(reposicao: Reposicao, public=True) -> dict:
    reposicao_dict = {}

    if public:
        reposicao_dict.update({
            'id': sala.id
        })
    return reposicao_dict
