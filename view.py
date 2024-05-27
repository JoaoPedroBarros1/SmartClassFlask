from flask import jsonify, request
from return_dicts import *
from models import *
from app import app, db
from authentication import generate_token, is_allowed


# -------------- AUTENTICAÇÃO --------------

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({'mensagem': 'Email inválido'}), 404

    if usuario.senha != senha:
        return jsonify({'mensagem': 'Senha inválida'}), 400

    token = generate_token(usuario.id)

    user = return_usuario(usuario, True)
    response_dict = {
        'token': token,
        'usuario': user
    }
    print(response_dict)
    return jsonify({'mensagem': 'Login com sucesso', 'response': response_dict}), 200


@app.route('/auth/me', methods=['GET'])
def get_me():
    response = is_allowed(['ALUNO', 'PROFESSOR', 'COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    return jsonify(
        mensagem='Informações do seu usuário',
        response=response['usuario']
    )


@app.route("/self/curso", methods=['GET'])
def get_self_cursos():
    response = is_allowed(['ALUNO', 'PROFESSOR'])
    if not response['allowed']:
        return jsonify(response), 403

    id_cursos = Matricula.query.filter_by(id_usuario=response['usuario']['id']).all()
    cursos = []
    for id_curso in id_cursos:
        curso = Curso.query.filter_by(id=id_curso).first()
        curso_dic = {
            'id': curso.id,
            'nome': curso.nome,
            'carga_horaria': curso.carga_horaria,
            'duracao': curso.duracao,
            'dias_da_semana': curso.dias_da_semana,
            'data_de_inicio': curso.data_de_inicio,
            'horario': curso.horario
        }
        cursos.append(curso_dic)

    return jsonify(
        mensagem='Lista de cursos matriculados',
        response=cursos
    )


# -------------- REPOSIÇÕES --------------


@app.route("/reposicao", methods=['GET'])
def get_reposicoes():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    reposicoes = Reposicao.query.all()

    if not reposicoes:
        return jsonify(mensagem='Não há reposições cadastradas')

    reposicoes_dic = []
    for reposicao in reposicoes:
        reposicao_dic = {
            'id': reposicao.id,
            'data': reposicao.data(),
            'id_curso': reposicao.id_curso
        }
        reposicoes_dic.append(reposicao_dic)

    return jsonify(
        mensagem='Lista de reposições',
        response=reposicoes_dic
    )


@app.route("/reposicao", methods=['POST'])
def post_reposicao():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    reposicao = request.json
    nova_reposicao = Reposicao(
        data=reposicao.get('data'),
        id_curso=reposicao.get('id_curso')
    )

    db.session.add(nova_reposicao)
    db.session.commit()

    return jsonify(
        mensagem='Reposição criada com sucesso',
        response={
            'id': nova_reposicao.id,
            'data': nova_reposicao.data(),
            'id_curso': nova_reposicao.id_curso
        }
    )


@app.route("/reposicao/<int:id_reposicao>", methods=['GET'])
def get_reposicao(id_reposicao):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    reposicao = Reposicao.query.get(id_reposicao)

    if not reposicao:
        return jsonify(mensagem='Reposição não encontrada')

    reposicao_info = {
        'id': reposicao.id,
        'data': reposicao.data(),
        'id_curso': reposicao.id_curso
    }

    return jsonify(
        mensagem='Informações da reposição',
        response=reposicao_info
    )


@app.route("/reposicao/<int:id_reposicao>", methods=['PUT'])
def put_reposicao(id_reposicao):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    reposicao = Reposicao.query.get(id_reposicao)

    if not reposicao:
        return jsonify(mensagem='Reposição não encontrada'), 404

    data = request.json
    reposicao.data = data.get('data', reposicao.data)
    reposicao.id_curso = data.get('id_curso', reposicao.id_curso)

    db.session.commit()

    return jsonify(
        mensagem='Reposição atualizada com sucesso',
        response={
            'id': reposicao.id,
            'data': reposicao.data(),
            'id_curso': reposicao.id_curso
        }
    )


@app.route("/reposicao/<int:id_reposicao>", methods=['DELETE'])
def delete_reposicao(id_reposicao):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    reposicao = Reposicao.query.get(id_reposicao)

    if not reposicao:
        return jsonify(mensagem='Reposição não encontrada')

    db.session.delete(reposicao)
    db.session.commit()

    return jsonify(mensagem='Reposição deletada com sucesso')


# -------------- DIAS NÃO LETIVOS --------------

@app.route("/naoletivo", methods=['GET'])
def get_nao_letivos():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    nao_letivos = NaoLetivo.query.all()

    if not nao_letivos:
        return jsonify(mensagem='Não há dias não letivos cadastrados')

    nao_letivos_dic = []
    for nao_letivo in nao_letivos:
        nao_letivo_dic = {
            'id': nao_letivo.id,
            'data': nao_letivo.data(),
            'nome': nao_letivo.nome
        }
        nao_letivos_dic.append(nao_letivo_dic)

    return jsonify(
        mensagem='Lista de dias não letivos',
        response=nao_letivos_dic
    )


@app.route("/naoletivo", methods=['POST'])
def post_nao_letivo():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    nao_letivo = request.json
    novo_nao_letivo = NaoLetivo(
        data=nao_letivo.get('data'),
        nome=nao_letivo.get('nome')
    )

    db.session.add(novo_nao_letivo)
    db.session.commit()

    return jsonify(
        mensagem='Dia não letivo cadastrado com sucesso',
        response={
            'id': novo_nao_letivo.id,
            'data': novo_nao_letivo.data(),
            'nome': novo_nao_letivo.nome
        }
    )


@app.route("/naoletivo/<int:id_nao_letivo>", methods=['GET'])
def get_nao_letivo(id_nao_letivo):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    nao_letivo = NaoLetivo.query.get(id_nao_letivo)

    if not nao_letivo:
        return jsonify(mensagem='Dia não letivo não encontrado')

    nao_letivo_info = {
        'id': nao_letivo.id,
        'data': nao_letivo.data(),
        'nome': nao_letivo.nome
    }

    return jsonify(
        mensagem='Informações do dia não letivo',
        response=nao_letivo_info
    )


@app.route("/naoletivo/<int:id_nao_letivo>", methods=['PUT'])
def put_nao_letivo(id_nao_letivo):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    nao_letivo = NaoLetivo.query.get(id_nao_letivo)

    if not nao_letivo:
        return jsonify(mensagem='Dia não letivo não encontrado'), 404

    data = request.json
    nao_letivo.data = data.get('data', nao_letivo.data)
    nao_letivo.nome = data.get('nome', nao_letivo.nome)

    db.session.commit()

    return jsonify(
        mensagem='Dia não letivo atualizado com sucesso',
        response={
            'id': nao_letivo.id,
            'data': nao_letivo.data(),
            'nome': nao_letivo.nome
        }
    )


@app.route("/naoletivo/<int:id_nao_letivo>", methods=['DELETE'])
def delete_nao_letivo(id_nao_letivo):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    nao_letivo = NaoLetivo.query.get(id_nao_letivo)

    if not nao_letivo:
        return jsonify(mensagem='Dia não letivo não encontrado')

    db.session.delete(nao_letivo)
    db.session.commit()

    return jsonify(mensagem='Dia não letivo deletado com sucesso')


# -------------- FERIADOS -----------------------

@app.route("/feriado", methods=['GET'])
def get_feriados():
    feriados = Feriado.query.all()
    feriados_list = []
    for feriado in feriados:
        feriado_dict = {
            "id": feriado.id,
            "nome": feriado.nome,
            "email": feriado.email
        }
        feriados_list.append(feriado_dict)
        
    return jsonify(mensagem="Todos os feriados fixos cadastrados", response=feriados_list)


@app.route("/feriado", methods=['POST'])
def create_feriado():
    data = request.json
    novo_feriado = Feriado(data=data['data'], nome=data['nome'])
    db.session.add(novo_feriado)
    db.session.commit()
    return jsonify(mensagem="Feriado criado com sucesso", response=novo_feriado)


@app.route("/feriado/<int:id_feriado>", methods=['GET'])
def get_feriado(id_feriado):
    feriado = Feriado.query.get(id_feriado)
    if not feriado:
        return jsonify(mensagem="Feriado não encontrado"), 404
    return jsonify(mensagem="", response=feriado)


@app.route("/feriado/<int:id_feriado>", methods=['PUT'])
def update_feriado(id_feriado):
    feriado = Feriado.query.get(id_feriado)
    if not feriado:
        return jsonify(mensagem="Feriado não encontrado"), 404

    data = request.json
    feriado.data = data['data']
    feriado.nome = data['nome']
    db.session.commit()

    return jsonify(mensagem="Feriado atualizado com sucesso", response=feriado)


@app.route("/feriado/<int:id_feriado>", methods=['DELETE'])
def delete_feriado(id_feriado):
    feriado = Feriado.query.get(id_feriado)
    if not feriado:
        return jsonify(mensagem="Feriado não encontrado"), 404

    db.session.delete(feriado)
    db.session.commit()

    return jsonify(mensagem="Feriado excluído com sucesso")


# ---------------------- USUÁRIO ----------------------


@app.route("/aluno", methods=['GET'])
def get_alunos():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    alunos = Aluno.query.all()

    if not alunos:
        return jsonify(mensagem='Não há alunos cadastrados')

    alunos_dic = []
    for aluno in alunos:
        cursos_list = []
        print(aluno)
        for curso in aluno.cursos:
            curso_dict = {

            }
            cursos_list.append(curso_dict)

        aluno_dic = {
            'id': aluno.usuario.id,
            'nome': aluno.usuario.id,
            'senha': aluno.usuario.id,
            'cursos': cursos_list
        }
        alunos_dic.append(aluno_dic)

    return jsonify(
        mensagem='Lista de alunos',
        response=alunos_dic
    )


@app.route("/aluno/<int:id_aluno>", methods=['GET'])
def get_aluno(id_aluno):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    aluno = Aluno.query.get(id_aluno)

    if not aluno:
        return jsonify(mensagem='Aluno não encontrado')

    aluno_info = {
        'id': aluno.id,
        'id_usuario': aluno.id_usuario,
    }

    return jsonify(
        mensagem='Informações do aluno',
        response=aluno_info
    )


@app.route("/professor", methods=['GET'])
def get_professores():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    professores = Professor.query.all()

    if not professores:
        return jsonify(mensagem='Não há professores cadastrados')

    professores_dic = []
    for professor in professores:
        professor_dic = {
            'id': professor.id,
            'id_usuario': professor.id_usuario,
            'start_turno': professor.start_turno,
            'end_turno': professor.end_turno,
            'dias_da_semana': professor.dias_da_semana,
        }
        professores_dic.append(professor_dic)

    return jsonify(
        mensagem='Lista de professores',
        response=professores_dic
    )


@app.route("/professor/<int:id_professor>", methods=['GET'])
def get_professor(id_professor):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    professor = Professor.query.get(id_professor)

    if not professor:
        return jsonify(mensagem='Professor não encontrado')

    professor_info = {
        'id': professor.id,
        'id_usuario': professor.id_usuario,
        'start_turno': professor.start_turno,
        'end_turno': professor.end_turno,
        'dias_da_semana': professor.dias_da_semana,
    }

    return jsonify(
        mensagem='Informações do professor',
        response=professor_info
    )


@app.route("/coordenador", methods=['GET'])
def get_coordenadores():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    coordenadores = Coordenador.query.all()

    if not coordenadores:
        return jsonify(mensagem='Não há coordenadores cadastrados')

    coordenadores_dic = []
    for coordenador in coordenadores:
        coordenador_dic = {
            'id': coordenador.id,
            'id_usuario': coordenador.id_usuario,
        }
        coordenadores_dic.append(coordenador_dic)

    return jsonify(
        mensagem='Lista de coordenadores',
        response=coordenadores_dic
    )


@app.route("/coordenador/<int:id_coordenador>", methods=['GET'])
def get_coordenador(id_coordenador):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    coordenador = Coordenador.query.get(id_coordenador)

    if not coordenador:
        return jsonify(mensagem='Coordenador não encontrado')

    coordenador_info = {
        'id': coordenador.id,
        'id_usuario': coordenador.id_usuario,
    }

    return jsonify(
        mensagem='Informações do coordenador',
        response=coordenador_info
    )


@app.route("/usuario", methods=['GET'])
def get_usuarios():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    usuarios = Usuario.query.all()
    usuarios_dic = []
    for usuario in usuarios:
        usuario_dic = {
            'id': usuario.id,
            'email': usuario.email,
            'senha': usuario.senha,
            'nome': usuario.nome,
            'cargo': usuario.cargo.name
        }
        usuarios_dic.append(usuario_dic)

    return jsonify(
        mensagem='Lista de Usuarios',
        response=usuarios_dic
    )


@app.route('/usuario', methods=['POST'])
def post_usuario():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
       return jsonify(response), 403

    usuario = request.json

    novo_usuario = Usuario(
        email=usuario.get('email'),
        senha=usuario.get('senha'),
        nome=usuario.get('nome'),
        cargo=usuario.get('cargo').upper()
    )

    user = Usuario.query.filter_by(email=novo_usuario.email).first()
    if user:
        return jsonify(mensagem="Email já cadastrado"), 400

    user_response = {}

    match novo_usuario.cargo:
        case CargoChoices.Professor.value:
            novo_professor = Professor(
                start_turno=usuario.get('start_turno'),
                end_turno=usuario.get('end_turno'),
                dias_da_semana=usuario.get('dias_da_semana')
            )

            novo_usuario.professor = novo_professor
            db.session.add(novo_professor)

            user_response = {
                "start_turno": novo_professor.start_turno,
                "end_turno": novo_professor.end_turno,
                "dias_da_semana": novo_professor.dias_da_semana
            }

        case CargoChoices.Coordenador.value:
            novo_coordenador = Coordenador()
            novo_usuario.coordenador = novo_coordenador
            db.session.add(novo_coordenador)

        case CargoChoices.Aluno.value:
            novo_aluno = Aluno()
            novo_usuario.aluno = novo_aluno
            db.session.add(novo_aluno)

        case _:
            return jsonify(mensagem='Cargo Não Reconhecido'), 400

    db.session.add(novo_usuario)
    db.session.commit()

    user_response.update(
        {
            'email': novo_usuario.email,
            'senha': novo_usuario.senha,
            'nome': novo_usuario.nome,
            'cargo': novo_usuario.cargo.name
        }
    )

    return jsonify(
        mensagem=f'{novo_usuario.cargo.name} Cadastrado com Sucesso',
        response=user_response
    ), 201


@app.route('/usuario/<int:id_usuario>', methods=['GET'])
def get_usuario(id_usuario):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    usuario = Usuario.query.filter_by(id=id_usuario).first()
    if not usuario:
        return jsonify(
            mensagem='Usuário não encontrado',
        ), 404

    usuario_dict = return_usuario(usuario, True)

    return jsonify(
        mensagem='Usuário retornado com sucesso',
        response=usuario_dict
    ), 200

    usuario = Usuario.query.filter_by(id=id_usuario).first()
    usuario_info = {
        'id': usuario.id,
        'email': usuario.email,
        'senha': usuario.senha,
        'nome': usuario.nome,
        'cargo': usuario.cargo.name
    }
    if usuario.cargo == CargoChoices.Professor.value:
        usuario_info['start_turno'] = usuario.professor.start_turno
        usuario_info['end_turno'] = usuario.professor.end_turno
        usuario_info['dias_da_semana'] = usuario.professor.dias_da_semana
    return jsonify(
        mensagem='Informações do usuário',
        response=usuario_info
    )

@app.route('/usuario/<int:id_usuario>', methods=['PUT'])
def put_usuario(id_usuario):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    usuario = Usuario.query.get_or_404(id_usuario)
    data = request.json

    usuario.email = data.get('email', usuario.email)
    usuario.senha = data.get('senha', usuario.senha)
    usuario.nome = data.get('nome', usuario.nome)

    if usuario.cargo == CargoChoices.Professor.value:
        usuario.professor.start_turno = data.get('start_turno', usuario.professor.start_turno)
        usuario.professor.end_turno = data.get('end_turno', usuario.professor.end_turno)
        usuario.professor.dias_da_semana = data.get('dias_da_semana', usuario.professor.dias_da_semana)

    db.session.commit()

    return jsonify(mensagem='Usuário modificado com sucesso'), 200


@app.route('/usuario/<int:id_usuario>', methods=['DELETE'])
def delete_usuario(id_usuario):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    usuario = Usuario.query.get_or_404(id_usuario)

    db.session.delete(usuario)
    db.session.commit()

    return jsonify(mensagem='Usuário deletado com sucesso'), 200


# -------------------- CURSOS ----------------------


@app.route("/curso", methods=['GET'])
def get_cursos():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    cursos = Curso.query.all()
    cursos_dic = []
    for curso in cursos:
        curso_dic = return_curso(curso, True)
        cursos_dic.append(curso_dic)

    return jsonify(
        mensagem='Lista de cursos',
        response=cursos_dic
    )


@app.route('/curso', methods=['POST'])
def post_curso():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    curso = request.json
    novo_curso = Curso(
        nome=curso.get('nome'),
        carga_horaria=curso.get('carga_horaria'),
        duracao=curso.get('duracao'),
        dias_da_semana=curso.get('dias_da_semana'),
        data_de_inicio=curso.get('data_de_inicio'),
        id_professor=curso.get('id_professor'),
        id_sala=curso.get('id_sala')
    )

    professor = Usuario.query.filter_by(
        id=novo_curso.id_professor,
        cargo=CargoChoices.Professor).first()
    if not professor:
        return jsonify({'mensagem': 'Professor não existe'})

    sala = Sala.query.filter_by(id=novo_curso.id_sala).first()
    if not sala:
        return jsonify({'mensagem': 'Sala não existe'})

    db.session.add(novo_curso)
    db.session.commit()

    return jsonify(
        mensagem='Curso Cadastrado com Sucesso',
        response=return_curso(curso, True)
    )


@app.route('/curso', methods=['PUT'])
def update_curso():
    return jsonify({'mensagem': 'Curso atualizado com sucesso'})


@app.route('/curso/<int:id_curso>', methods=['PUT'])
def put_curso(id_curso):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    curso = Curso.query.get(id_curso)

    if curso:
        data = request.json
        curso.nome = data.get('nome', curso.nome)
        curso.carga_horaria = data.get('cargaHoraria', curso.carga_horaria)
        curso.duracao = data.get('duracaoHoras', curso.duracao)
        curso.dias_da_semana = data.get('diasSemana', curso.dias_da_semana)
        curso.data_de_inicio = data.get('dataInicio', curso.data_de_inicio)
        curso.horario = data.get('horario', curso.horario)

        db.session.commit()

        return jsonify(
            mensagem='Curso atualizado com sucesso',
            curso={
                'id': curso.id,
                'nome': curso.nome,
                'carga_horaria': curso.carga_horaria.isoformat(),
                'duracao': curso.duracao.isoformat(),
                'dias_da_semana': curso.dias_da_semana,
                'data_de_inicio': curso.data_de_inicio.isoformat(),
                'id_professor': curso.id_professor,
                'id_sala': curso.id_sala
            }
        )

    return jsonify(mensagem='Curso não encontrado'), 404


@app.route('/curso/<int:id_curso>', methods=['DELETE'])
def delete_curso(id_curso):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    curso = Curso.query.get(id_curso)

    if curso:
        db.session.delete(curso)
        db.session.commit()

        return jsonify(mensagem='Curso removido com sucesso')

    return jsonify(mensagem='Curso não encontrado'), 404


# ---------------- SALA ------------------


@app.route('/sala', methods=['GET'])
def get_salas():
    salas = Sala.query.all()
    return jsonify([{'id': sala.id, 'nome': sala.nome} for sala in salas])


@app.route('/sala', methods=['POST'])
def post_sala():
    data = request.json
    nova_sala = Sala(nome=data['nome'])
    db.session.add(nova_sala)
    db.session.commit()
    return jsonify({'mensagem': 'Sala criada com sucesso!'})

@app.route('/sala/<int:id_sala>', methods=['GET'])
def get_sala(id_sala):
    sala = Sala.query.get_or_404(id_sala)
    return jsonify({'id': sala.id, 'nome': sala.nome})


@app.route('/sala/<int:id_sala>', methods=['PUT'])
def put_sala(id_sala):
    sala = Sala.query.get_or_404(id_sala)
    data = request.json
    sala.nome = data['nome']
    db.session.commit()
    return jsonify({'mensagem': 'Sala atualizada com sucesso!'})

@app.route('/sala/<int:id_sala>', methods=['DELETE'])
def delete_sala(id_sala):
    sala = Sala.query.get_or_404(id_sala)
    db.session.delete(sala)
    db.session.commit()
    return jsonify({'mensagem': 'Sala deletada com sucesso!'})

# -------------- MATRICULAS --------------


@app.route("/matricula", methods=['GET'])
def get_matriculas():
    response = is_allowed(['ALUNO', 'COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    matriculas = Matricula.query.all()

    if not matriculas:
        return jsonify(mensagem='Não há matrículas cadastradas')

    matriculas_dic = []
    for matricula in matriculas:
        matricula_dic = {
            'id': matricula.id,
            'id_usuario': matricula.id_usuario,
            'id_curso': matricula.id_curso
        }
        matriculas_dic.append(matricula_dic)

    return jsonify(
        mensagem='Lista de matrículas',
        response=matriculas_dic
    )


@app.route("/matricula", methods=['POST'])
def post_matricula():
    response = is_allowed(['ALUNO'])
    if not response['allowed']:
        return jsonify(response), 403

    matricula = request.json
    nova_matricula = Matricula(
        id_usuario=matricula.get('id_usuario'),
        id_curso=matricula.get('id_curso')
    )

    db.session.add(nova_matricula)
    db.session.commit()

    return jsonify(
        mensagem='Matrícula realizada com sucesso',
        response={
            'id': nova_matricula.id,
            'id_usuario': nova_matricula.id_usuario,
            'id_curso': nova_matricula.id_curso
        }
    )


@app.route("/matricula/usuario/<int:id_usuario>", methods=['GET'])
def get_matriculas_usuario(id_usuario):
    response = is_allowed(['ALUNO', 'COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    matriculas = Matricula.query.filter_by(id_usuario=id_usuario).all()

    if not matriculas:
        return jsonify(mensagem='Não há matrículas para este usuário')

    matriculas_dic = []
    for matricula in matriculas:
        matricula_dic = {
            'id': matricula.id,
            'id_usuario': matricula.id_usuario,
            'id_curso': matricula.id_curso
        }
        matriculas_dic.append(matricula_dic)

    return jsonify(
        mensagem=f'Lista de matrículas do usuário {id_usuario}',
        response=matriculas_dic
    )


@app.route("/matricula/matricula/<int:id_curso>", methods=['GET'])
def get_matricula_curso(id_curso):
    response = is_allowed(['ALUNO', 'COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    matricula = Matricula.query.filter_by(id_curso=id_curso).first()

    if not matricula:
        return jsonify(mensagem='Este curso não possui matrícula')

    matricula_info = {
        'id': matricula.id,
        'id_usuario': matricula.id_usuario,
        'id_curso': matricula.id_curso
    }

    return jsonify(
        mensagem='Informações da matrícula',
        response=matricula_info
    )


@app.route("/matricula/matricula/<int:id_curso>", methods=['DELETE'])
def delete_matricula_curso(id_curso):
    response = is_allowed(['ALUNO'])
    if not response['allowed']:
        return jsonify(response), 403

    matricula = Matricula.query.filter_by(id_curso=id_curso).first()

    if not matricula:
        return jsonify(mensagem='Matrícula não encontrada')

    db.session.delete(matricula)
    db.session.commit()

    return jsonify(mensagem='Matrícula deletada com sucesso')
