import datetime
from dateutil.parser import parse
from models import *


def return_weekdays(dias_da_semana: int) -> dict:
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
        'list': weekdays_list,
        'names': weekdays_names,
        'bool': weekdays_bool
    }

    return weekdays_dict


def return_sala(sala: Sala, admin: bool, curso_recursive: bool) -> dict:
    sala_dict = {
        'nome': sala.nome
    }

    if curso_recursive:
        curso_list = []
        for curso in sala.cursos:
            curso_list.append(return_curso(curso, admin, True, True, False, True))
        sala_dict.update({
            'cursos': curso_list
        })

    if admin:
        sala_dict.update({
            'id': sala.id
        })
    return sala_dict


def return_usuario(usuario: Usuario, admin: bool) -> dict:
    usuario_dict = {
        'nome': usuario.nome,
        'cargo': usuario.cargo.name
    }

    if admin:
        usuario_dict.update({
            'id': usuario.id,
            'email': usuario.email,
            'senha': usuario.senha
        })
    return usuario_dict


def return_aluno(aluno: Aluno, admin: bool, curso_recursive: bool) -> dict:
    aluno_dict = {
        'nome': aluno.usuario.nome,
        'cargo': aluno.usuario.cargo.name
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
            'id': aluno.id,
            'email': aluno.usuario.email,
            'senha': aluno.usuario.senha
        })
    return aluno_dict


def return_professor(professor: Professor, admin: bool, curso_recursive: bool) -> dict:
    professor_dict = {
        'nome': professor.usuario.nome,
        'cargo': professor.usuario.cargo.name,
        'start_turno': professor.start_turno.isoformat(),
        'end_turno': professor.end_turno.isoformat(),
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
            'id': professor.id,
            'email': professor.usuario.email,
            'senha': professor.usuario.senha
        })
    return professor_dict


def return_coordenador(coordenador: Coordenador, admin: bool) -> dict:
    coordenador_dict = {
        'nome': coordenador.usuario.nome,
        'cargo': coordenador.usuario.cargo.name
    }

    if admin:
        coordenador_dict.update({
            'id': coordenador.id,
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
        'nome': curso.nome,
        'data_de_inicio': curso.data_de_inicio.isoformat(),
        'carga_horaria': curso.carga_horaria.isoformat(),
        'duracao': curso.duracao.isoformat(),
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
        'aulas': aulas,
        'feriados': all_feriados
    })

    if admin:
        curso_dict.update({
            'id': curso.id
        })
    return curso_dict


def return_emenda(emenda: Emenda, admin: bool) -> dict:
    emenda_dict = {
        'nome': emenda.feriado.nome,
        'data_feriado': emenda.feriado.data.strftime('%Y-%m-%d'),
        'data_emenda': emenda.data.strftime('%Y-%m-%d'),
        'emenda': emenda.emenda
    }

    if admin:
        emenda_dict.update({
            'id': emenda.id
        })
    return emenda_dict


def return_feriado(feriado: Feriado, admin: bool) -> dict:
    data = parse(str(feriado.data))
    feriado_dict = {
        'data_feriado': data.strftime('%Y-%m-%d'),
        'nome': feriado.nome
    }

    if feriado.emenda:
        feriado_dict.update(return_emenda(feriado.emenda, admin))
    else:
        print(feriado.emenda)

    if admin:
        feriado_dict.update({
            'id': feriado.id
        })
    return feriado_dict


def return_reposicao(reposicao: Reposicao, admin: bool, curso_recursive: bool) -> dict:
    reposicao_dict = {
        'data': reposicao.data
    }

    if curso_recursive:
        reposicao_dict.update({
            'curso': return_curso(reposicao.curso, admin, True, False, True, True)
        })

    if admin:
        reposicao_dict.update({
            'id': reposicao.id,
            'id_curso': reposicao.id_curso
        })
    return reposicao_dict
