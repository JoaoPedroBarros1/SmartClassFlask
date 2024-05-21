from flask import jsonify, request
from main import app, db
from models import CargoChoices, Sala, Usuario, Curso, Matricula, Aluno, Professor, Coordenador, Reposicao, NaoLetivo, Feriado
from authentication import generate_token, is_allowed


# -------------- Rotas relacionadas aos usuários (Aluno, Professor ou Coordenador) --------------

# Rotas relacionadas aos alunos
@app.route("/aluno", methods=['GET'])
def get_alunos():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    alunos = Aluno.query.all()

    if not alunos:
        return jsonify(mensagem='Não há alunos cadastrados')

    alunos_dic = []
    for aluno in alunos:
        aluno_dic = {
            'id': aluno.id,
            'id_usuario': aluno.id_usuario,
        }
        alunos_dic.append(aluno_dic)

    return jsonify(
        mensagem='Lista de alunos',
        alunos=alunos_dic
    )

@app.route("/aluno/<int:id_aluno>", methods=['GET'])
def get_aluno(id_aluno):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    aluno = Aluno.query.get(id_aluno)

    if not aluno:
        return jsonify(mensagem='Aluno não encontrado')

    aluno_info = {
        'id': aluno.id,
        'id_usuario': aluno.id_usuario,
    }

    return jsonify(
        mensagem='Informações do aluno',
        aluno=aluno_info
    )

# Rotas relacionadas aos professores
@app.route("/professor", methods=['GET'])
def get_professores():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        professores=professores_dic
    )

@app.route("/professor/<int:id_professor>", methods=['GET'])
def get_professor(id_professor):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        professor=professor_info
    )

# Rotas relacionadas aos coordenadores
@app.route("/coordenador", methods=['GET'])
def get_coordenadores():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        coordenadores=coordenadores_dic
    )

@app.route("/coordenador/<int:id_coordenador>", methods=['GET'])
def get_coordenador(id_coordenador):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    coordenador = Coordenador.query.get(id_coordenador)

    if not coordenador:
        return jsonify(mensagem='Coordenador não encontrado')

    coordenador_info = {
        'id': coordenador.id,
        'id_usuario': coordenador.id_usuario,
    }

    return jsonify(
        mensagem='Informações do coordenador',
        coordenador=coordenador_info
    )

# ------------------ Rotas relacionadas ao próprio usuário ------------------

@app.route("/self/usuario", methods=['GET'])
def get_self_usuario():
    response = is_allowed(['ALUNO', 'PROFESSOR'])
    if not response['allowed']:
        return jsonify(response)

    return jsonify(
        mensagem='Informações do seu usuário',
        usuario=response['usuario']
    )

@app.route("/self/curso", methods=['GET'])
def get_self_cursos():
    response = is_allowed(['ALUNO', 'PROFESSOR'])
    if not response['allowed']:
        return jsonify(response)

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
        cursos=cursos
    )

# ---------------------- Cadastro e login de usuários ----------------------

@app.route("/usuario", methods=['GET'])
def get_usuario():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        usuarios=usuarios_dic
    )

@app.route('/usuario', methods=['POST'])
def post_usuario():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    usuario = request.json
    cargo_name = usuario.get('cargo').upper()

    novo_usuario = Usuario(
        email=usuario.get('email'),
        senha=usuario.get('senha'),
        nome=usuario.get('nome'),
        cargo=cargo_name
    )

    for cargo in CargoChoices:
        if novo_usuario.cargo == cargo.value:
            break
    else:
        return jsonify(mensagem='Cargo Não Reconhecido'), 401

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify(
        mensagem='Usuario Cadastrado com Sucesso',
        usuario={
            'email': novo_usuario.email,
            'senha': novo_usuario.senha,
            'nome': novo_usuario.nome,
            'cargo': novo_usuario.cargo.name
        }
    )

@app.route('/login', methods=['POST'])
def login():
    response = is_allowed(['ALUNO', 'PROFESSOR', 'COORDENADOR'])
    if response['allowed']:
        return jsonify({'mensagem': 'Usuário já está logado com uma conta'})

    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({'mensagem': 'Email inválido'}), 401

    if usuario.senha != senha:
        return jsonify({'mensagem': 'Senha inválida'}), 401

    token = generate_token(usuario.id)

    user = {
        'email': usuario.email,
        'senha': usuario.senha,
        'nome': usuario.nome,
        'cargo': usuario.cargo.name
    }
    return jsonify({'mensagem': 'Login com sucesso', 'token': token, 'usuario': user}), 200

# -------------------- Criação e modificação de cursos ----------------------

@app.route("/curso", methods=['GET'])
def get_curso():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    cursos = Curso.query.all()
    cursos_dic = []
    for curso in cursos:
        curso_dic = {
            'id': curso.id,
            'nome': curso.nome,
            'dias_da_semana': curso.dias_da_semana,
            'id_professor': curso.id_professor,
            'id_sala': curso.id_sala,
            'carga_horaria': curso.carga_horaria.isoformat(),
            'duracao': curso.duracao.isoformat(),
            'data_de_inicio': curso.data_de_inicio.isoformat(),
        }
        cursos_dic.append(curso_dic)

    return jsonify(
        mensagem='Lista de cursos',
        cursos=cursos_dic
    )

@app.route('/curso', methods=['POST'])
def post_curso():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        curso={
            'id': novo_curso.id,
            'nome': novo_curso.nome,
            'carga_horaria': novo_curso.carga_horaria.isoformat(),
            'duracao': novo_curso.duracao.isoformat(),
            'dias_da_semana': novo_curso.dias_da_semana,
            'data_de_inicio': novo_curso.data_de_inicio.isoformat(),
            'id_professor': novo_curso.id_professor,
            'id_sala': novo_curso.id_sala
        }
    )

@app.route('/curso/<int:id_curso>', methods=['PUT'])
def put_curso(id_curso):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        return jsonify(response)

    curso = Curso.query.get(id_curso)

    if curso:
        db.session.delete(curso)
        db.session.commit()

        return jsonify(mensagem='Curso removido com sucesso')

    return jsonify(mensagem='Curso não encontrado'), 404


# -------------- Rotas relacionadas às matrículas --------------

# Rota para listar todas as matrículas
@app.route("/matricula", methods=['GET'])
def get_matriculas():
    response = is_allowed(['ALUNO', 'COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        matriculas=matriculas_dic
    )

# Rota para realizar uma nova matrícula
@app.route("/matricula", methods=['POST'])
def post_matricula():
    response = is_allowed(['ALUNO'])
    if not response['allowed']:
        return jsonify(response)

    matricula = request.json
    nova_matricula = Matricula(
        id_usuario=matricula.get('id_usuario'),
        id_curso=matricula.get('id_curso')
    )

    db.session.add(nova_matricula)
    db.session.commit()

    return jsonify(
        mensagem='Matrícula realizada com sucesso',
        matricula={
            'id': nova_matricula.id,
            'id_usuario': nova_matricula.id_usuario,
            'id_curso': nova_matricula.id_curso
        }
    )

# Rota para listar todas as matrículas de um usuário específico
@app.route("/matricula/usuario/<int:id_usuario>", methods=['GET'])
def get_matriculas_usuario(id_usuario):
    response = is_allowed(['ALUNO', 'COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        matriculas=matriculas_dic
    )

# Rota para listar informações de um curso matriculado por um usuário específico
@app.route("/matricula/matricula/<int:id_curso>", methods=['GET'])
def get_matricula_curso(id_curso):
    response = is_allowed(['ALUNO', 'COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        matricula=matricula_info
    )

# Rota para deletar uma matrícula específica
@app.route("/matricula/matricula/<int:id_curso>", methods=['DELETE'])
def delete_matricula_curso(id_curso):
    response = is_allowed(['ALUNO'])
    if not response['allowed']:
        return jsonify(response)

    matricula = Matricula.query.filter_by(id_curso=id_curso).first()

    if not matricula:
        return jsonify(mensagem='Matrícula não encontrada')

    db.session.delete(matricula)
    db.session.commit()

    return jsonify(mensagem='Matrícula deletada com sucesso')

# -------------- Rotas relacionadas às reposições --------------

# Rota para listar todas as reposições
@app.route("/reposicao", methods=['GET'])
def get_reposicoes():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        reposicoes=reposicoes_dic
    )

# Rota para criar uma nova reposição
@app.route("/reposicao", methods=['POST'])
def post_reposicao():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    reposicao = request.json
    nova_reposicao = Reposicao(
        data=reposicao.get('data'),
        id_curso=reposicao.get('id_curso')
    )

    db.session.add(nova_reposicao)
    db.session.commit()

    return jsonify(
        mensagem='Reposição criada com sucesso',
        reposicao={
            'id': nova_reposicao.id,
            'data': nova_reposicao.data(),
            'id_curso': nova_reposicao.id_curso
        }
    )

# Rota para obter informações de uma reposição específica
@app.route("/reposicao/<int:id_reposicao>", methods=['GET'])
def get_reposicao(id_reposicao):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        reposicao=reposicao_info
    )

# Rota para atualizar informações de uma reposição específica
@app.route("/reposicao/<int:id_reposicao>", methods=['PUT'])
def put_reposicao(id_reposicao):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    reposicao = Reposicao.query.get(id_reposicao)

    if not reposicao:
        return jsonify(mensagem='Reposição não encontrada'), 404

    data = request.json
    reposicao.data = data.get('data', reposicao.data)
    reposicao.id_curso = data.get('id_curso', reposicao.id_curso)

    db.session.commit()

    return jsonify(
        mensagem='Reposição atualizada com sucesso',
        reposicao={
            'id': reposicao.id,
            'data': reposicao.data(),
            'id_curso': reposicao.id_curso
        }
    )

# Rota para deletar uma reposição específica
@app.route("/reposicao/<int:id_reposicao>", methods=['DELETE'])
def delete_reposicao(id_reposicao):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    reposicao = Reposicao.query.get(id_reposicao)

    if not reposicao:
        return jsonify(mensagem='Reposição não encontrada')

    db.session.delete(reposicao)
    db.session.commit()

    return jsonify(mensagem='Reposição deletada com sucesso')


# -------------- Rotas relacionadas aos dias não letivos --------------

# Rota para listar todos os dias não letivos
@app.route("/naoletivo", methods=['GET'])
def get_nao_letivos():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        nao_letivos=nao_letivos_dic
    )

# Rota para criar um novo dia não letivo
@app.route("/naoletivo", methods=['POST'])
def post_nao_letivo():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    nao_letivo = request.json
    novo_nao_letivo = NaoLetivo(
        data=nao_letivo.get('data'),
        nome=nao_letivo.get('nome')
    )

    db.session.add(novo_nao_letivo)
    db.session.commit()

    return jsonify(
        mensagem='Dia não letivo cadastrado com sucesso',
        nao_letivo={
            'id': novo_nao_letivo.id,
            'data': novo_nao_letivo.data(),
            'nome': novo_nao_letivo.nome
        }
    )

# Rota para obter informações de um dia não letivo específico
@app.route("/naoletivo/<int:id_nao_letivo>", methods=['GET'])
def get_nao_letivo(id_nao_letivo):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

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
        nao_letivo=nao_letivo_info
    )

# Rota para atualizar informações de um dia não letivo específico
@app.route("/naoletivo/<int:id_nao_letivo>", methods=['PUT'])
def put_nao_letivo(id_nao_letivo):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    nao_letivo = NaoLetivo.query.get(id_nao_letivo)

    if not nao_letivo:
        return jsonify(mensagem='Dia não letivo não encontrado'), 404

    data = request.json
    nao_letivo.data = data.get('data', nao_letivo.data)
    nao_letivo.nome = data.get('nome', nao_letivo.nome)

    db.session.commit()

    return jsonify(
        mensagem='Dia não letivo atualizado com sucesso',
        nao_letivo={
            'id': nao_letivo.id,
            'data': nao_letivo.data(),
            'nome': nao_letivo.nome
        }
    )

# Rota para deletar um dia não letivo específico
@app.route("/naoletivo/<int:id_nao_letivo>", methods=['DELETE'])
def delete_nao_letivo(id_nao_letivo):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    nao_letivo = NaoLetivo.query.get(id_nao_letivo)

    if not nao_letivo:
        return jsonify(mensagem='Dia não letivo não encontrado')

    db.session.delete(nao_letivo)
    db.session.commit()

    return jsonify(mensagem='Dia não letivo deletado com sucesso')


# -------------- Rotas relacionadas aos feriados -----------------------

# Rota para listar todos os feriados
@app.route("/feriado", methods=['GET'])
def get_feriados():
    feriados = Feriado.query.all()
    return jsonify(feriados=[])


# Rota para criar um novo feriado
@app.route("/feriado", methods=['POST'])
def create_feriado():
    data = request.json
    novo_feriado = Feriado(data=data['data'], nome=data['nome'])
    db.session.add(novo_feriado)
    db.session.commit()
    return jsonify(message="Feriado criado com sucesso", feriado=novo_feriado)


# Rota para obter detalhes de um feriado específico
@app.route("/feriado/<int:id>", methods=['GET'])
def get_feriado(id):
    feriado = Feriado.query.get(id)
    if not feriado:
        return jsonify(message="Feriado não encontrado"), 404
    return jsonify(feriado=feriado)


# Rota para atualizar os detalhes de um feriado
@app.route("/feriado/<int:id>", methods=['PUT'])
def update_feriado(id):
    feriado = Feriado.query.get(id)
    if not feriado:
        return jsonify(message="Feriado não encontrado"), 404

    data = request.json
    feriado.data = data['data']
    feriado.nome = data['nome']
    db.session.commit()

    return jsonify(message="Feriado atualizado com sucesso", feriado=feriado)


# Rota para excluir um feriado
@app.route("/feriado/<int:id>", methods=['DELETE'])
def delete_feriado(id):
    feriado = Feriado.query.get(id)
    if not feriado:
        return jsonify(message="Feriado não encontrado"), 404

    db.session.delete(feriado)
    db.session.commit()

    return jsonify(message="Feriado excluído com sucesso")

