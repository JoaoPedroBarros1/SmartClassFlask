from dateutil.parser import parse
from models import *


def return_weekdays(dias_da_semana: int) -> dict:
    int_dias_semana = dias_da_semana

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
        'num': int_dias_semana,
        'list': weekdays_list,
        'names': weekdays_names,
        'bool': weekdays_bool
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
            curso_list.append(return_curso(curso, admin, True, True, False, True))
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
        'data_de_inicio': curso.data_de_inicio.isoformat(),
        'carga_horaria': curso.carga_horaria,
        'start_curso': curso.start_curso,
        'end_curso': curso.end_curso,
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

    aulas = []
    all_feriados = []

    dias_por_semana = 0
    print(curso_dict)
    for _dia in curso_dict['dias_da_semana']['bool']:
        dias_por_semana += _dia

    total_semanas = 0
    for semana in range(total_semanas):  # 0, 1, 2, 3...
        pass

    curso_dict.update({
        'aulas': aulas,
        'feriados': all_feriados,
        'qtd_feriados': len(all_feriados),
        'qtd_reposicoes': len(curso.reposicoes)
    })

    return curso_dict


def return_emenda(emenda: Emenda, admin: bool, feriado_recursive: bool) -> dict:
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


def return_feriado(feriado: Feriado, admin: bool) -> dict:
    data = parse(str(feriado.data))
    feriado_dict = {
        'id': feriado.id,
        'data_feriado': data.strftime('%Y-%m-%d'),
        'nome': feriado.nome
    }

    if feriado.emenda:
        feriado_dict.update(return_emenda(feriado.emenda, admin, False))

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
