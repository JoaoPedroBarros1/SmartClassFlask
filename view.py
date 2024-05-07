from flask import jsonify, request, session
from main import app, db
from models import CargoChoices, Sala, Usuario, Curso
from authentication import generate_token, is_allowed


# -------------- Cadastro, login e logout --------------
@app.route("/usuario", methods=['GET'])
def get_usuario():
    usuarios = Usuario.query.all()
    usuarios_dic = []
    for usuario in usuarios:
        usuario_dic = {
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
    data = request.json
    email = data.get('email')
    senha = data.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and usuario.senha == senha:
        token = generate_token(usuario.id)
        return jsonify({'mensagem': 'Login com sucesso', 'token': token}), 200

    else:
        return jsonify({'mensagem': 'Email ou senha inválido'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    response = is_allowed()
    return jsonify(response)


# ---------------- Criação e modificação de cursos --------------
@app.route("/curso", methods=['GET'])
def get_curso():
    if 'id_usuario' in session:
        cursos = Curso.query.all()
        cursos_dic = []
        for curso in cursos:
            curso_dic = {
                'id': curso.id,
                'nome': curso.nome,
                'carga_horaria': curso.carga_horaria,
                'duracao': curso.duracao,
                'dias_da_semana': curso.dias_da_semana,
                'data_de_inicio': curso.data_de_inicio,
                'horario': curso.horario
            }
            cursos_dic.append(curso_dic)

        return jsonify(
            mensagem='Lista de cursos',
            cursos=cursos_dic
        )
    else:
        return jsonify({'mensagem': 'Você não está logado'})


@app.route('/curso', methods=['POST'])
def post_curso():
    if 'id_usuario' in session:
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

        db.session.add(novo_curso)
        db.session.commit()

        return jsonify(
            mensagem='Curso Cadastrado com Sucesso',
            curso={
                'id_curso': novo_curso.id,
                'nome': novo_curso.nome,
                'cargaHoraria': novo_curso.carga_horaria,
                'duracaoHoras': novo_curso.duracao,
                'diasSemana': novo_curso.dias_da_semana,
            }
        )

    else:
        return jsonify({'mensagem': 'Você não está logado'})


@app.route('/curso/<int:id_curso>', methods=['PUT'])
def put_curso(id_curso):
    if 'id_usuario' in session:
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
    else:
        return jsonify({'mensagem': 'Usuário não está logado'})


@app.route('/curso/<int:id_curso>', methods=['DELETE'])
def delete_curso(id_curso):
    if 'id_usuario' in session:
        curso = Curso.query.get(id_curso)

        if curso:
            db.session.delete(curso)
            db.session.commit()

            return jsonify({'mensagem': 'Curso excluído com sucesso'})

        else:
            return jsonify({'mensagem': 'Curso não encontrado'})
    else:
        return jsonify({'mensagem': 'Usuário não está logado'})


# --------------------- Criação e modificação de Salas ------------------------
@app.route("/sala", methods=['GET'])
def get_sala():
    if 'id_usuario' in session:
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
    else:
        return jsonify({'mensagem': 'Você não está logado'})


@app.route('/sala', methods=['POST'])
def post_sala():
    if 'id_usuario' in session:
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

    else:
        return jsonify({'mensagem': 'Você não está logado'})


@app.route('/sala/<int:id_sala>', methods=['PUT'])
def put_sala(id_sala):
    if 'id_usuario' in session:
        sala = Sala.query.get(id_sala)

        if sala:
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

        else:
            return jsonify({'mensagem': 'Sala não encontrada'})
    else:
        return jsonify({'mensagem': 'Usuário não está logado'})


@app.route('/sala/<int:id_sala>', methods=['DELETE'])
def delete_sala(id_sala):
    if 'id_usuario' in session:
        sala = Sala.query.get(id_sala)

        if sala:
            db.session.delete(sala)
            db.session.commit()

            return jsonify({'mensagem': 'Sala excluída com sucesso'})

        else:
            return jsonify({'mensagem': 'Sala não encontrada'})
    else:
        return jsonify({'mensagem': 'Usuário não está logado'})
