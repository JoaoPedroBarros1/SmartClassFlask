from flask import jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash
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
    senha = check_password_hash(usuario.senha, senha)
    if not usuario or not senha:
        return jsonify({'mensagem': 'Dados incorretos'}), 400

    token = generate_token(usuario.id)

    user = return_usuario(usuario, True)
    response_dict = {
        'token': token,
        'usuario': user
    }
    return jsonify({'mensagem': 'Login com sucesso', 'response': response_dict}), 200


@app.route('/self/me', methods=['GET'])
def get_me():
    response = is_allowed(['ALUNO', 'PROFESSOR', 'COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    return jsonify(
        mensagem='Informações do seu usuário',
        response=response['response']
    ), 200


@app.route("/self/curso", methods=['GET'])
def get_self_cursos():
    response = is_allowed(['ALUNO', 'PROFESSOR'])
    if not response['allowed']:
        return jsonify(response), 403

    self_user = Usuario.query.filter_by(id=response['usuario']['id']).first()
    cursos = []
    for curso in self_user.cursos:
        curso_dic = return_curso(curso, False,
                                 True,
                                 True,
                                 True,
                                 True)
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
        return jsonify(mensagem='Não há reposições cadastradas'), 404

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
    ), 200


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

@app.route("/emenda", methods=['GET'])
def get_emendas():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    emendas = Emenda.query.all()

    if not emendas:
        return jsonify(mensagem='Não há emendas cadastradas'), 404

    emendas_dic = []
    for emenda in emendas:
        nao_letivo_dic = return_emenda(emenda, True)
        emendas_dic.append(nao_letivo_dic)

    return jsonify(
        mensagem='Lista de emendas',
        response=emendas_dic
    ), 200


@app.route("/emenda/<int:id_emenda>", methods=['GET'])
def get_emenda(id_emenda):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    emenda = Emenda.query.filter_by(id=id_emenda).first()

    if not emenda:
        return jsonify(mensagem='Emenda não encontrada'), 404

    emenda_info = return_emenda(emenda, response['admin'])

    return jsonify(
        mensagem='Informações da emenda',
        response=emenda_info
    ), 200


@app.route("/emenda/<int:id_emenda>", methods=['PUT'])
def put_emenda(id_emenda):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    emenda = Emenda.query.filter_by(id=id_emenda).first()

    if not emenda:
        return jsonify(mensagem='Emenda não encontrada'), 404

    data_emenda = request.json
    emenda_bool = data_emenda['emenda']
    emenda.emenda = emenda_bool

    db.session.commit()

    emenda_info = return_emenda(emenda, response['admin'])

    return jsonify(
        mensagem='Emenda atualizada com sucesso',
        response=emenda_info
    ), 200


# -------------- FERIADOS -----------------------

@app.route("/feriado", methods=['GET'])
def get_feriados():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    feriados = Feriado.query.all()

    if not feriados:
        return jsonify(mensagem="Não há feriados cadastrados"), 404

    feriados_list = []
    for feriado in feriados:
        feriado_dict = return_feriado(feriado, True)
        feriados_list.append(feriado_dict)
        
    return jsonify(mensagem="Todos os feriados fixos cadastrados", response=feriados_list), 200


@app.route("/feriado", methods=['POST'])
def post_feriado():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    feriado = request.json
    nome: str = feriado['nome']
    data: str = feriado['data']
    novo_feriado = Feriado(data=data, nome=nome)
    feriado_dict = return_feriado(novo_feriado, False)

    db.session.add(novo_feriado)

    data: datetime.date = feriado_dict['data_feriado']
    match data.isoweekday():
        case 2:
            day_before = data - datetime.timedelta(1)
            nova_emenda = Emenda(data=day_before)
            novo_feriado.emenda = nova_emenda
            db.session.add(nova_emenda)

        case 4:
            day_after = data + datetime.timedelta(1)
            nova_emenda = Emenda(data=day_after)
            novo_feriado.emenda = nova_emenda
            db.session.add(nova_emenda)

    db.session.commit()
    return jsonify(mensagem="Feriado criado com sucesso", response=feriado_dict), 201


@app.route("/feriado/<int:id_feriado>", methods=['GET'])
def get_feriado(id_feriado):
    feriados = Feriado.query.get(id_feriado)
    if not feriados:
        return jsonify(mensagem="Feriado não encontrado"), 404

    feriados_list = []
    for feriado in feriados:
        feriados_list.append(return_feriado(feriado, True))

    return jsonify(mensagem="", response=feriados_list)


@app.route("/feriado/<int:id_feriado>", methods=['PUT'])
def put_feriado(id_feriado):
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
        return jsonify(mensagem='Não há alunos cadastrados'), 404

    alunos_dic = []
    for aluno in alunos:
        aluno_dic = return_aluno(aluno, True, True)
        alunos_dic.append(aluno_dic)

    return jsonify(
        mensagem='Lista de alunos',
        response=alunos_dic
    ), 200


@app.route("/aluno/<int:id_aluno>", methods=['GET'])
def get_aluno(id_aluno):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    aluno = Aluno.query.filter_by(id=id_aluno).first()

    if not aluno:
        return jsonify(mensagem='Aluno não encontrado'), 404

    aluno_info = return_aluno(aluno, True, True)

    return jsonify(
        mensagem='Informações do aluno',
        response=aluno_info
    ), 200


@app.route("/professor", methods=['GET'])
def get_professores():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    professores = Professor.query.all()

    if not professores:
        return jsonify(mensagem='Não há professores cadastrados'), 404

    professores_dic = []
    for professor in professores:
        professor_dic = return_professor(professor, True, True)
        professores_dic.append(professor_dic)

    return jsonify(
        mensagem='Lista de professores',
        response=professores_dic
    ), 200


@app.route("/professor/<int:id_professor>", methods=['GET'])
def get_professor(id_professor):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    professor = Professor.query.filter_by(id=id_professor).first()

    if not professor:
        return jsonify(mensagem='Professor não encontrado'), 404

    professor_info = return_professor(professor, True, True)

    return jsonify(
        mensagem='Informações do professor',
        response=professor_info
    ), 200


@app.route("/coordenador", methods=['GET'])
def get_coordenadores():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    coordenadores = Coordenador.query.all()

    if not coordenadores:
        return jsonify(mensagem='Não há coordenadores cadastrados'), 404

    coordenadores_dic = []
    for coordenador in coordenadores:
        coordenador_dic = return_coordenador(coordenador, True)
        coordenadores_dic.append(coordenador_dic)

    return jsonify(
        mensagem='Lista de coordenadores',
        response=coordenadores_dic
    ), 200


@app.route("/coordenador/<int:id_coordenador>", methods=['GET'])
def get_coordenador(id_coordenador):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    coordenador = Coordenador.query.filter_by(id=id_coordenador).first()

    if not coordenador:
        return jsonify(mensagem='Coordenador não encontrado'), 404

    coordenador_info = return_coordenador(coordenador, True)

    return jsonify(
        mensagem='Informações do coordenador',
        response=coordenador_info
    ), 200


@app.route("/usuario", methods=['GET'])
def get_usuarios():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    usuarios = Usuario.query.all()

    if not usuarios:
        return jsonify(mensagem='Não há usuários'), 404

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
    ), 200


@app.route('/usuario', methods=['POST'])
def post_usuario():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    usuario = request.json
    email = usuario['email']
    senha = usuario['senha']
    nome = usuario['nome']
    cargo = usuario['cargo']

    user = Usuario.query.filter_by(email=email).first()
    if user:
        return jsonify(mensagem="Email já cadastrado"), 400

    senha_hash = generate_password_hash(senha).decode('utf-8')

    novo_usuario = Usuario(
        email=email,
        senha=senha_hash,
        nome=nome,
        cargo=cargo.upper()
    )

    user_response = {}

    match novo_usuario.cargo:
        case CargoChoices.Professor.value:
            start_turno = usuario['start_turno']
            end_turno = usuario['end_turno']
            dias_da_semana = usuario['dias_da_semana']
            novo_professor = Professor(
                start_turno=start_turno,
                end_turno=end_turno,
                dias_da_semana=dias_da_semana
            )
            novo_usuario.professor = novo_professor
            db.session.add(novo_professor)
            user_response.update(return_professor(novo_professor, True, False))

        case CargoChoices.Coordenador.value:
            novo_coordenador = Coordenador()
            novo_usuario.coordenador = novo_coordenador
            db.session.add(novo_coordenador)
            user_response.update(return_coordenador(novo_coordenador, True))

        case CargoChoices.Aluno.value:
            novo_aluno = Aluno()
            novo_usuario.aluno = novo_aluno
            db.session.add(novo_aluno)
            user_response.update(return_aluno(novo_aluno, True, False))

        case _:
            return jsonify(mensagem='Cargo Não Reconhecido'), 400

    db.session.add(novo_usuario)
    db.session.commit()

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


@app.route('/usuario/<int:id_usuario>', methods=['PUT'])
def put_usuario(id_usuario):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    usuario = Usuario.query.filter_by(id=id_usuario).first()
    if not usuario:
        return jsonify(
            mensagem='Usuário não encontrado',
        ), 404
    data = request.json

    novo_usuario = {
        'email': data['email'],
        'senha': data['senha'],
        'nome': data['nome']
    }

    user = Usuario.query.filter_by(email=novo_usuario['email']).first()
    if user and user != usuario:
        return jsonify(mensagem="Email já cadastrado"), 400

    match usuario.cargo.name:
        case CargoChoices.Professor.name:
            novo_professor = {
                'start_turno': data.get('start_turno'),
                'end_turno': data.get('end_turno'),
                'dias_da_semana': data.get('dias_da_semana')
            }
            usuario.professor.start_turno = novo_professor['start_turno']
            usuario.professor.end_turno = novo_professor['end_turno']
            usuario.professor.dias_da_semana = novo_professor['dias_da_semana']
            novo_usuario.update(novo_professor)

        case CargoChoices.Coordenador.name:
            pass

        case CargoChoices.Aluno.name:
            pass

    usuario.email = novo_usuario['email']
    usuario.senha = novo_usuario['senha']
    usuario.nome = novo_usuario['nome']

    db.session.commit()

    return jsonify(mensagem='Usuário modificado com sucesso', response=novo_usuario), 200


@app.route('/usuario/<int:id_usuario>', methods=['DELETE'])
def delete_usuario(id_usuario):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    usuario = Usuario.query.filter_by(id=id_usuario).first()
    if not usuario:
        return jsonify(
            mensagem='Usuário não encontrado',
        ), 404

    match usuario.cargo:
        case CargoChoices.Professor:
            if usuario.professor.cursos:
                cursos_list = []
                for curso in usuario.professor.cursos:
                    cursos_list.append(return_curso(curso, True,
                                                    False,
                                                    False,
                                                    False,
                                                    False))
                return jsonify(mensagem='Professor está cadastrado em um curso',
                               response=cursos_list), 400

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
        curso_dic = return_curso(curso, True,
                                 True,
                                 True,
                                 True,
                                 True)
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

    professor = Professor.query.filter_by(id=novo_curso.id_professor).first()
    if not professor:
        return jsonify({'mensagem': 'Professor não existe'}), 400

    sala = Sala.query.filter_by(id=novo_curso.id_sala).first()
    if not sala:
        return jsonify({'mensagem': 'Sala não existe'}), 400

    db.session.add(novo_curso)
    db.session.commit()

    return jsonify(
        mensagem='Curso Cadastrado com Sucesso',
        response=return_curso(curso, True, False, False, True, True)
    )


@app.route('/curso', methods=['PUT'])
def put_curso():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

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
        ), 200

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
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    salas = Sala.query.all()
    salas_list = []
    for sala in salas:
        sala_dict = return_sala(sala, True, True)
        salas_list.append(sala_dict)

    return jsonify({'mensagem': 'Todas as salas cadastradas', 'response': salas_list}), 200


@app.route('/sala', methods=['POST'])
def post_sala():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    sala = request.json
    nome = sala['nome']
    nova_sala = Sala(nome=nome)

    if not nova_sala.nome:
        return jsonify({'mensagem': 'Nome inválido'}), 400

    db.session.add(nova_sala)
    db.session.commit()
    return jsonify({'mensagem': 'Sala criada com sucesso!', 'response': return_sala(nova_sala, True, False)}), 201


@app.route('/sala/<int:id_sala>', methods=['GET'])
def get_sala(id_sala):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    sala = Sala.query.filter_by(id=id_sala).first()
    if not sala:
        return jsonify({'mensagem': 'Sala não encontrada'}), 404

    sala_dict = return_sala(sala, True, True)
    return jsonify({'mensagem': 'Sala encontrada', 'response': sala_dict}), 200


@app.route('/sala/<int:id_sala>', methods=['PUT'])
def put_sala(id_sala):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    sala = Sala.query.filter_by(id=id_sala).first()
    if not sala:
        return jsonify({'mensagem': 'Sala não encontrada'}), 404

    data = request.json
    nome = data['nome']

    if not nome:
        return jsonify({'mensagem': 'Nome inválido'}), 400

    sala.nome = nome
    db.session.commit()
    sala_dict = return_sala(sala, True, True)
    return jsonify({'mensagem': 'Sala atualizada com sucesso!', 'response': sala_dict})


@app.route('/sala/<int:id_sala>', methods=['DELETE'])
def delete_sala(id_sala):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    sala = Sala.query.filter_by(id=id_sala).first()
    if not sala:
        return jsonify({'mensagem': 'Sala não encontrada'}), 404

    db.session.delete(sala)
    db.session.commit()
    return jsonify({'mensagem': 'Sala deletada com sucesso!'}), 200


# -------------- MATRICULAS --------------


@app.route("/matricula", methods=['GET'])
def get_matriculas():
    response = is_allowed(['COORDENADOR'])
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
    response = is_allowed(['COORDENADOR'])
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


@app.route("/matricula/<int:id_curso>/<int:id_usuario>", methods=['DELETE'])
def delete_matricula_curso(id_curso, id_usuario):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response), 403

    matricula = Matricula.query.filter_by(id_curso=id_curso, id_usuario=id_usuario).first()

    if not matricula:
        return jsonify(mensagem='Matrícula não encontrada'), 404

    db.session.delete(matricula)
    db.session.commit()

    return jsonify(mensagem='Matrícula deletada com sucesso'), 200
