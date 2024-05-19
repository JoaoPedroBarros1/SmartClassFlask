from flask import jsonify, request
from main import app, db
from models import CargoChoices, Sala, Usuario, Curso, Matricula
from authentication import generate_token, is_allowed
from feriados import handle_aulas


# {
#     "nome": "Técnico em Desenvolvimento de Sistemas",
#     "carga_horaria": "",
#     "duracao": "",
#     "dias_da_semana": "",
#     "data_de_inicio": "",
#     "id_professor": "",
#     "id_sala": ""
# }


# -------------- GET usuários (Aluno, Professor ou Coordenador) --------------
@app.route("/usuario/<string:nome_cargo>", methods=['GET'])
def get_cargos(nome_cargo):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    usuarios = Usuario.query.filter_by(cargo=nome_cargo).all()

    if not usuarios:
        return jsonify(mensagem='Não há usuários neste cargo')

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
        mensagem='Lista do cargo: '+nome_cargo,
        usuarios=usuarios_dic
    )


# -------------- GET self --------------
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


# -------------- Cadastro e login de usuários --------------
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


# ---------------- Criação e modificação de cursos --------------
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
                'id_curso': curso.id,
                'nome': curso.nome,
                'cargaHoraria': curso.carga_horaria,
                'duracaoHoras': curso.duracao,
                'diasSemana': curso.dias_da_semana,
                'dataInicio': curso.data_de_inicio,
                'horario': curso.horario
            }
        )

    else:
        return jsonify({'mensagem': 'Curso não encontrado'})


@app.route('/curso/<int:id_curso>', methods=['DELETE'])
def delete_curso(id_curso):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    curso = Curso.query.get(id_curso)

    if curso:
        db.session.delete(curso)
        db.session.commit()
        return jsonify({'mensagem': 'Curso excluído com sucesso'})

    else:
        return jsonify({'mensagem': 'Curso não encontrado'})


# --------------------- Criação e modificação de Salas ------------------------
@app.route("/sala", methods=['GET'])
def get_sala():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    salas = Sala.query.all()
    salas_dic = []
    for sala in salas:
        sala_dic = {
            'id_sala': sala.id,
            'nome': sala.nome,
        }
        salas_dic.append(sala_dic)

    return jsonify(
        mensagem='Lista de salas',
        salas=salas_dic
    )


@app.route('/sala', methods=['POST'])
def post_sala():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    sala = request.json
    nova_sala = Sala(
        nome=sala.get('nome'),
    )

    db.session.add(nova_sala)
    db.session.commit()

    return jsonify(
        mensagem='Sala cadastrada com sucesso',
        sala={
            'id_sala': nova_sala.id,
            'nome': nova_sala.nome,
        }
    )


@app.route('/sala/<int:id_sala>', methods=['PUT'])
def put_sala(id_sala):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    sala = Sala.query.get(id_sala)

    if not sala:
        return jsonify({'mensagem': 'Sala não encontrada'})

    data = request.json
    sala.nome = data.get('nome', sala.nome)

    db.session.commit()

    return jsonify(
        mensagem='Sala atualizada com sucesso',
        sala={
            'id_sala': sala.id,
            'nome': sala.nome,
        }
    )


@app.route('/sala/<int:id_sala>', methods=['DELETE'])
def delete_sala(id_sala):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    sala = Sala.query.get(id_sala)

    if not sala:
        return jsonify({'mensagem': 'Sala não encontrada'})

    cursos = Curso.query.filter_by(id_sala=id_sala).all()
    if cursos:
        cursos_dict = []
        for curso in cursos:
            curso_dict = {
                'id': curso.id,
                'nome': curso.nome
            }
            cursos_dict.append(curso_dict)

        return jsonify({
            'mensagem': 'Essa sala está sendo utilizada por algum curso',
            'cursos': cursos_dict})

    db.session.delete(sala)
    db.session.commit()
    return jsonify({'mensagem': 'Sala excluída com sucesso'})


# --------------------- Gerenciamento das matrículas ------------------------
@app.route("/matricula", methods=['GET'])
def get_matricula():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    matriculas = Matricula.query.filter_by(id_usuario=response['usuario']['id']).all()
    matriculas_dic = {}
    for matricula in matriculas:
        curso = Curso.query.filter_by(id=matricula.id_curso).first()

        dias_letivos = handle_aulas(curso=curso)
        matricula_dic = {
            'nome': curso.nome,
            'id_professor': curso.id_professor,
            'id_sala': curso.id_sala,
            'duracao': curso.duracao,
            'dias_letivos': dias_letivos
        }
        matriculas_dic[matricula.id_curso] = matricula_dic

    return jsonify({"mensagem": 'Lista de matrículas',
                    "matriculas": matriculas_dic})


@app.route('/matricula', methods=['POST'])
def post_matricula():
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    matricula = request.json
    nova_matricula = Matricula(
        id_curso=matricula.get('id_curso'),
        id_usuario=matricula.get('id_usuario')
    )

    usuario = Usuario.query.filter_by(
        id=nova_matricula.id_usuario, cargo=CargoChoices.Aluno).first()

    if not usuario:
        return jsonify({'mensagem': 'Aluno não existe'})

    matricula_existente = matricula.query.filter_by(
        id_curso=nova_matricula.id_curso,
        id_usuario=nova_matricula.id_usuario).first()

    if matricula_existente:
        return jsonify({'mensagem': 'Aluno já matriculado'})

    db.session.add(nova_matricula)
    db.session.commit()

    return jsonify({
        'mensagem': 'Matrícula cadastrada com sucesso',
        'matricula': {
            'id_curso': nova_matricula.id_curso,
            'id_usuario': nova_matricula.id_usuario,
        }
    })


@app.route('/matricula/<int:id_curso>', methods=['DELETE'])
def delete_matricula(id_curso):
    response = is_allowed(['COORDENADOR'])
    if not response['allowed']:
        return jsonify(response)

    matricula = Matricula.query.filter_by(
        id_usuario=response['usuario']['id'],
        id_curso=id_curso).first()

    if matricula:
        db.session.delete(matricula)
        db.session.commit()
        return jsonify({'mensagem': 'Matrícula excluída com sucesso'})

    else:
        return jsonify({'mensagem': 'Matrícula não encontrada'})
