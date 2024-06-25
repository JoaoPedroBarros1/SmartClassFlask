import datetime

from dateutil.parser import parse
from math import ceil
from models import *


def return_weekdays(dias_da_semana: int) -> dict:
    dias_da_semana = int(dias_da_semana)
    int_dias_semana = 0

    class WeekDays(enum.IntEnum):
        SABADO = 64
        SEXTA = 32
        QUINTA = 16
        QUARTA = 8
        TERCA = 4
        SEGUNDA = 2
        DOMINGO = 1

    weekdays_list = []
    weekdays_names = []
    weekdays_bool = []
    weekdays_iso = []

    if dias_da_semana >= WeekDays.SABADO.value:
        dias_da_semana -= WeekDays.SABADO.value
        weekdays_list.append("Sábado")
        weekdays_names.append("Sat")
        weekdays_bool.append(True)
        weekdays_iso.append(6)
        int_dias_semana += 1
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.SEXTA.value:
        dias_da_semana -= WeekDays.SEXTA.value
        weekdays_list.append("Sexta")
        weekdays_names.append("Fri")
        weekdays_bool.append(True)
        weekdays_iso.append(5)
        int_dias_semana += 1
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.QUINTA.value:
        dias_da_semana -= WeekDays.QUINTA.value
        weekdays_list.append("Quinta")
        weekdays_names.append("Thu")
        weekdays_bool.append(True)
        weekdays_iso.append(4)
        int_dias_semana += 1
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.QUARTA.value:
        dias_da_semana -= WeekDays.QUARTA.value
        weekdays_list.append("Quarta")
        weekdays_names.append("Wed")
        weekdays_bool.append(True)
        weekdays_iso.append(3)
        int_dias_semana += 1
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.TERCA.value:
        dias_da_semana -= WeekDays.TERCA.value
        weekdays_list.append("Terça")
        weekdays_names.append("Tue")
        weekdays_bool.append(True)
        weekdays_iso.append(2)
        int_dias_semana += 1
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.SEGUNDA.value:
        dias_da_semana -= WeekDays.SEGUNDA.value
        weekdays_list.append("Segunda")
        weekdays_names.append("Mon")
        weekdays_bool.append(True)
        weekdays_iso.append(1)
        int_dias_semana += 1
    else:
        weekdays_bool.append(False)

    if dias_da_semana >= WeekDays.DOMINGO.value:
        dias_da_semana -= WeekDays.DOMINGO.value
        weekdays_list.append("Domingo")
        weekdays_names.append("Sun")
        weekdays_bool.append(True)
        weekdays_iso.append(0)
        int_dias_semana += 1
    else:
        weekdays_bool.append(False)

    weekdays_list.reverse()
    weekdays_names.reverse()
    weekdays_bool.reverse()
    weekdays_iso.reverse()

    days_interval = []
    for iso_n in range(1, len(weekdays_iso)):
        days_interval.append((weekdays_iso[iso_n] + 6 - weekdays_iso[iso_n - 1]) % 7 + 1)
    days_interval.append((weekdays_iso[0] + 6 - weekdays_iso[-1]) % 7 + 1)

    weekdays_dict = {
        'num': int_dias_semana,
        'list': weekdays_list,
        'names': weekdays_names,
        'bool': weekdays_bool,
        'iso_days': weekdays_iso,
        'days_interval': days_interval
    }

    return weekdays_dict


def return_sala(sala: Sala, admin: bool, curso_recursive: bool) -> dict:
    sala_dict = {
        'nome': sala.nome,
        'id': sala.id
    }

    if curso_recursive:
        curso_list = []
        for curso in sala.cursos:
            curso_list.append(return_curso(curso,
                                           admin,
                                           True,
                                           True,
                                           False,
                                           True))
        sala_dict.update({
            'cursos': curso_list
        })

    return sala_dict


def return_usuario(usuario: Usuario, admin: bool) -> dict:
    usuario_dict = {
        'id': usuario.id,
        'nome': usuario.nome,
        'cargo': usuario.cargo.name
    }

    if admin:
        usuario_dict.update({
            'email': usuario.email,
            'senha': usuario.senha
        })
    return usuario_dict


def return_aluno(aluno: Aluno, admin: bool, curso_recursive: bool) -> dict:
    aluno_dict = {
        'id': aluno.id,
        'nome': aluno.usuario.nome,
        'cargo': 'ALUNO'
    }

    if curso_recursive:
        cursos_list = []
        for curso in aluno.cursos:
            cursos_list.append(return_curso(curso, admin, False, True, True, True))
        aluno_dict.update({
            'cursos': cursos_list
        })

    if admin:
        aluno_dict.update({
            'email': aluno.usuario.email,
            'senha': aluno.usuario.senha
        })
    return aluno_dict


def return_professor(professor: Professor, admin: bool, curso_recursive: bool) -> dict:
    professor_dict = {
        'id': professor.id,
        'nome': professor.usuario.nome,
        'cargo': 'PROFESSOR',
        'start_turno': str(professor.start_turno),
        'end_turno': str(professor.end_turno),
        'dias_da_semana': return_weekdays(professor.dias_da_semana)
    }

    if curso_recursive:
        cursos_list = []
        for curso in professor.cursos:
            cursos_list.append(return_curso(curso, admin, True, True, True, False))
        professor_dict.update({
            'cursos': cursos_list
        })
    if admin:
        professor_dict.update({
            'email': professor.usuario.email,
            'senha': professor.usuario.senha,
        })
    return professor_dict


def return_coordenador(coordenador: Coordenador, admin: bool) -> dict:
    coordenador_dict = {
        'id': coordenador.id,
        'nome': coordenador.usuario.nome,
        'cargo': 'COORDENADOR'
    }

    if admin:
        coordenador_dict.update({
            'email': coordenador.usuario.email,
            'senha': coordenador.usuario.senha
        })
    return coordenador_dict


def return_curso(curso: Curso, admin: bool,
                 aluno_recursive: bool,
                 reposicoes_recursive: bool,
                 sala_recursive: bool,
                 prof_recursive: bool
                 ) -> dict:
    curso_dict = {
        'id': curso.id,
        'nome': curso.nome,
        'data_de_inicio': str(curso.data_de_inicio),
        'carga_horaria': curso.carga_horaria,
        'start_curso': str(curso.start_curso),
        'end_curso': str(curso.end_curso),
        'dias_da_semana': return_weekdays(curso.dias_da_semana)
    }

    if aluno_recursive:
        alunos_list = []
        for aluno in curso.alunos:
            alunos_list.append(return_aluno(aluno, admin, False))
        curso_dict.update({
            'alunos': alunos_list
        })

    if reposicoes_recursive:
        reposicoes_list = []
        for reposicao in curso.reposicoes:
            reposicoes_list.append(return_reposicao(reposicao, admin, False))
        curso_dict.update({
            'reposicoes': reposicoes_list
        })

    if sala_recursive:
        curso_dict.update({
            'sala': return_sala(curso.sala, admin, False)
        })

    if prof_recursive:
        curso_dict.update({
            'professor': return_professor(curso.professor, admin, False)
        })

    dias_letivos = return_aulas(curso)

    curso_dict.update({
        'aulas': dias_letivos['aulas'],
        'feriados': dias_letivos['feriados'],
        'qtd_feriados': len(dias_letivos['feriados']),
        'qtd_reposicoes': len(curso.reposicoes)
    })

    return curso_dict


def return_emenda(emenda: Emenda, feriado_recursive: bool) -> dict:
    emenda_dict = {
        'id': emenda.id,
        'nome': emenda.feriado.nome,
        'data_emenda': emenda.data.strftime('%Y-%m-%d'),
        'emenda': emenda.emenda
    }

    if feriado_recursive:
        emenda_dict.update({
            'data_feriado': emenda.feriado.data.strftime('%Y-%m-%d')
        })
    return emenda_dict


def return_feriado(feriado: Feriado) -> dict:
    data = parse(str(feriado.data))
    feriado_dict = {
        'id': feriado.id,
        'data_feriado': data.strftime('%Y-%m-%d'),
        'nome': feriado.nome
    }

    if feriado.emenda:
        feriado_dict.update(return_emenda(feriado.emenda, False))

    return feriado_dict


def return_reposicao(reposicao: Reposicao, admin: bool, curso_recursive: bool) -> dict:
    reposicao_dict = {
        'id': reposicao.id,
        'id_curso': reposicao.id_curso,
        'data': reposicao.data
    }

    if curso_recursive:
        reposicao_dict.update({
            'curso': return_curso(reposicao.curso, admin, True, False, True, True)
        })

    return reposicao_dict


def return_aulas(curso: Curso) -> dict:
    time_start_curso = datetime.datetime.combine(datetime.date.today(), datetime.time.fromisoformat(str(curso.start_curso)))
    time_end_curso = datetime.datetime.combine(datetime.date.today(), datetime.time.fromisoformat(str(curso.end_curso)))
    time_delta = (time_end_curso - time_start_curso).total_seconds() / 3600
    total_days: int = ceil(int(curso.carga_horaria)/time_delta)

    _data_inicio: datetime.date = datetime.date.fromisoformat(str(curso.data_de_inicio))

    dias_semana_dict = return_weekdays(curso.dias_da_semana)
    _days_offset = 0
    for num in dias_semana_dict['iso_days']:
        if num >= _data_inicio.isoweekday():
            break
        else:
            _days_offset += 1
    else:
        _days_offset = 0

    _first_day_offset = (dias_semana_dict['iso_days'][_days_offset % len(dias_semana_dict['iso_days'])]
                         + 7 - _data_inicio.isoweekday()) % 7
    first_day = _data_inicio + datetime.timedelta(days=_first_day_offset)
    aulas_days = set()
    for i in range(total_days):
        aulas_days.update([first_day.isoformat()])
        day_offset = dias_semana_dict['days_interval'][(i + _days_offset) % len(dias_semana_dict['days_interval'])]
        first_day += datetime.timedelta(days=day_offset)

    feriados_days = {str(x.data) for x in Feriado.query.all()}
    feriados_days.update({str(x.data) for x in Emenda.query.all() if bool(x.emenda)})

    feriados_days.intersection_update(aulas_days)
    aulas_days.difference_update(feriados_days)

    reposicoes_days = set()
    for reposicao in Reposicao.query.filter_by(id_curso=curso.id).all():
        reposicoes_days.update([reposicao.data])

    return {'aulas': list(aulas_days),
            'feriados': list(feriados_days),
            'reposicoes': list(reposicoes_days),
            'aulas_set': aulas_days,
            'feriados_set': feriados_days,
            'reposicoes_set': reposicoes_days
            }
