import datetime
from models import *


def return_weekdays(dias_da_semana: int) -> dict:
    class WeekDays(enum.IntEnum):
        DOMINGO = 1
        SEGUNDA = 2
        TERCA = 4
        QUARTA = 8
        QUINTA = 16
        SEXTA = 32
        SABADO = 64

    weekdays_list = []
    weekdays_names = []
    weekdays_bool = []

    if dias_da_semana >= WeekDays.SABADO:
        dias_da_semana -= WeekDays.SABADO
        weekdays_list.append("Sábado")
        weekdays_names.append("Sat")
        weekdays_bool.append(True)
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.SEXTA:
        dias_da_semana -= WeekDays.SEXTA
        weekdays_list.append("Sexta")
        weekdays_names.append("Fri")
        weekdays_bool.append(True)
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.QUINTA:
        dias_da_semana -= WeekDays.QUINTA
        weekdays_list.append("Quinta")
        weekdays_names.append("Thu")
        weekdays_bool.append(True)
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.QUARTA:
        dias_da_semana -= WeekDays.QUARTA
        weekdays_list.append("Quarta")
        weekdays_names.append("Wed")
        weekdays_bool.append(True)
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.TERCA:
        dias_da_semana -= WeekDays.TERCA
        weekdays_list.append("Terça")
        weekdays_names.append("Tue")
        weekdays_bool.append(True)
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.SEGUNDA:
        dias_da_semana -= WeekDays.SEGUNDA
        weekdays_list.append("Segunda")
        weekdays_names.append("Mon")
        weekdays_bool.append(True)
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.DOMINGO:
        dias_da_semana -= WeekDays.DOMINGO
        weekdays_list.append("Domingo")
        weekdays_names.append("Sun")
        weekdays_bool.append(True)
    else:
        weekdays_bool.append(False)

    weekdays_list.reverse()
    weekdays_names.reverse()
    weekdays_bool.reverse()

    weekdays_dict = {
        'list': weekdays_list,
        'names': weekdays_names,
        'bool': weekdays_bool
    }

    return weekdays_dict


def return_sala(sala: Sala, public: bool) -> dict:
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


def return_usuario(usuario: Usuario, public: bool) -> dict:
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


def return_aluno(aluno: Aluno, public: bool) -> dict:
    aluno_dict = {
        'nome': aluno.usuario.nome,
        'cargo': aluno.usuario.cargo.name
    }

    cursos_list = []
    for curso in aluno.cursos:
        cursos_list.append(return_curso(curso, public))
    aluno_dict.update({
        'cursos': cursos_list
    })

    if public:
        aluno_dict.update({
            'id': aluno.id,
            'email': aluno.usuario.email,
            'senha': aluno.usuario.senha
        })
    return aluno_dict


def return_professor(professor: Professor, public: bool) -> dict:
    professor_dict = {
        'nome': professor.usuario.nome,
        'cargo': professor.usuario.cargo.name,
        'start_turno': professor.start_turno.isoformat(),
        'end_turno': professor.end_turno.isoformat(),
        'dias_da_semana': return_weekdays(professor.dias_da_semana)
    }

    cursos_list = []
    for curso in professor.cursos:
        cursos_list.append(return_curso(curso, public))
    professor_dict.update({
        'cursos': cursos_list
    })
    if public:
        professor_dict.update({
            'id': professor.id,
            'email': professor.usuario.email,
            'senha': professor.usuario.senha
        })
    return professor_dict


def return_coordenador(coordenador: Coordenador, public: bool) -> dict:
    coordenador_dict = {
        'nome': coordenador.usuario.nome,
        'cargo': coordenador.usuario.cargo.name
    }

    if public:
        coordenador_dict.update({
            'id': coordenador.id,
            'email': coordenador.usuario.email,
            'senha': coordenador.usuario.senha
        })
    return coordenador_dict


def return_curso(curso: Curso, public: bool) -> dict:
    curso_dict = {
        'nome': curso.nome,
        'professor': return_professor(curso.professor, public),
        'sala': return_sala(curso.sala, public),
        'data_de_inicio': curso.data_de_inicio.isoformat(),
        'carga_horaria': curso.carga_horaria.isoformat(),
        'duracao': curso.duracao.isoformat(),
    }
    alunos_list = []
    for aluno in curso.alunos:
        alunos_list.append(return_aluno(aluno, public))

    reposicoes_list = []
    for reposicao in curso.reposicoes:
        reposicoes_list.append(return_reposicao(reposicao, public))

    print(curso.data_de_inicio)
    print(curso.data_de_inicio.__dir__())
    curso_date = datetime.datetime(
        curso.data_de_inicio.year(),
        curso.data_de_inicio.month(),
        curso.data_de_inicio.day()
    )
    inicio_curso = datetime.time()
    dias_da_semana = return_weekdays(curso.dias_da_semana)
    aulas = []
    all_feriados = []

    curso_dict.update({
        'reposicoes': reposicoes_list,
        'alunos': alunos_list,
        'aulas': aulas,
        'feriados': all_feriados
    })

    if public:
        curso_dict.update({
            'id': curso.id
        })
    return curso_dict


def return_naoletivo(naoletivo: NaoLetivo, public: bool) -> dict:
    naoletivo_dict = {
        'data': naoletivo.data,
        'nome': naoletivo.nome,
        'emenda': naoletivo.emenda
    }

    if public:
        naoletivo_dict.update({
            'id': naoletivo.id
        })
    return naoletivo_dict


def return_feriado(feriado: Feriado, public: bool) -> dict:
    feriado_dict = {
        'data': feriado.data,
        'nome': feriado.nome,
        'emenda': feriado.emenda
    }

    if public:
        feriado_dict.update({
            'id': feriado.id
        })
    return feriado_dict


def return_reposicao(reposicao: Reposicao, public: bool) -> dict:
    reposicao_dict = {
        'data': reposicao.data
    }

    if public:
        reposicao_dict.update({
            'id': reposicao.id,
            'id_curso': reposicao.id_curso
        })
    return reposicao_dict
