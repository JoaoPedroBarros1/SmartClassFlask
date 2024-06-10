from config import SECRET_KEY
from flask_bcrypt import generate_password_hash, check_password_hash
from return_dicts import *
from return_integrity import *
from models import *
from app import app, db
from authentication import login_required, admin_required
from flask import jsonify, g
import jwt
import requests
import datetime


# -------------- DEBUG --------------
@app.route('/template/coordenador', methods=['POST'])
def create_template():
    email = 'coordenador@gmail.com'
    senha = '1234'
    nome = 'default'
    cargo = 'cOorDeNADor'

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

    novo_coordenador = Coordenador()
    novo_usuario.coordenador = novo_coordenador
    db.session.add(novo_coordenador)
    user_response.update(return_coordenador(novo_coordenador, True))

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify(
        mensagem=f'{novo_usuario.cargo.name} Cadastrado com Sucesso',
        response=user_response
    ), 201


# -------------- AUTENTICAÇÃO --------------

@app.route('/login', methods=['POST'])
@check_integrity({"email", "senha"})
def login():
    user_email = g.data_request['email']
    user_senha = g.data_request['senha']

    usuario = Usuario.query.filter_by(email=user_email).first()
    if not usuario:
        return jsonify(mensagem='Dados incorretos'), 400

    senha = check_password_hash(usuario.senha, user_senha)
    if not senha:
        return jsonify(mensagem='Dados incorretos'), 400

    payload = {'id_usuario': usuario.id}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    user = return_usuario(usuario, True)
    response_dict = {
        'token': token,
        'usuario': user
    }
    return jsonify(mensagem='Login com sucesso', response=response_dict), 200


@app.route('/me', methods=['GET'])
@login_required
def get_me():
    return jsonify(
        mensagem='Informações do seu usuário',
        response=g.usuario
    ), 200


# -------------- REPOSIÇÕES --------------


@app.route("/reposicao", methods=['GET'])
@login_required
@admin_required
def get_reposicoes():
    reposicoes = Reposicao.query.all()

    if not reposicoes:
        return jsonify(mensagem='Não há reposições cadastradas'), 404

    reposicoes_dic = []
    for reposicao in reposicoes:
        reposicao_dic = return_reposicao(reposicao, True, True)
        reposicoes_dic.append(reposicao_dic)

    return jsonify(
        mensagem='Lista de reposições',
        response=reposicoes_dic
    ), 200


@app.route("/reposicao", methods=['POST'])
@login_required
@admin_required
@check_integrity({'data', 'id_curso', 'id_feriado'})
def post_reposicao():
    nova_reposicao = Reposicao(
        data =g.data_request['data'],
        id_curso=g.data_request['id_curso'],
        id_feriado=g.data_request['id_feriado']
    )

    db.session.add(nova_reposicao)
    db.session.commit()

    return jsonify(
        mensagem='Reposição criada com sucesso'
    )


@app.route("/reposicao/<int:id_reposicao>", methods=['GET'])
@login_required
@admin_required
def get_reposicao(id_reposicao):
    reposicao = Reposicao.query.filter_by(id=id_reposicao)

    if not reposicao:
        return jsonify(mensagem='Reposição não encontrada')

    return jsonify(
        mensagem='Informações da reposição',
        response=return_reposicao(reposicao, True, True)
    ), 200


@app.route("/reposicao/<int:id_reposicao>", methods=['PUT'])
@login_required
@admin_required
def put_reposicao(id_reposicao):
    reposicao = Reposicao.query.filter_by(id=id_reposicao).first()
    if not reposicao:
        return jsonify(mensagem='Reposição não encontrada'), 404

    if 'data' in g.data_request:
        reposicao.data = g.data_request['data']

    if 'id_curso' in g.data_request:
        reposicao.id_curso = g.data_request['id_curso']

    db.session.commit()

    return jsonify(
        mensagem='Reposição atualizada com sucesso',
        response=return_reposicao(reposicao, True, True)
    ), 200


@app.route("/reposicao/<int:id_reposicao>", methods=['DELETE'])
@login_required
@admin_required
def delete_reposicao(id_reposicao):
    reposicao = Reposicao.query.filter_by(id=id_reposicao)

    if not reposicao:
        return jsonify(mensagem='Reposição não encontrada'), 404

    db.session.delete(reposicao)
    db.session.commit()

    return jsonify(mensagem='Reposição deletada com sucesso'), 200


# -------------- DIAS NÃO LETIVOS --------------

@app.route("/emenda", methods=['GET'])
@login_required
@admin_required
def get_emendas():
    emendas = Emenda.query.all()

    if not emendas:
        return jsonify(mensagem='Não há emendas cadastradas'), 404

    emendas_dic = []
    for emenda in emendas:
        nao_letivo_dic = return_emenda(emenda, True, True)
        emendas_dic.append(nao_letivo_dic)

    return jsonify(
        mensagem='Lista de emendas',
        response=emendas_dic
    ), 200


@app.route("/emenda/<int:id_emenda>", methods=['GET'])
@login_required
@admin_required
def get_emenda(id_emenda):
    emenda = Emenda.query.filter_by(id=id_emenda).first()

    if not emenda:
        return jsonify(mensagem='Emenda não encontrada'), 404

    return jsonify(
        mensagem='Informações da emenda',
        response=return_emenda(emenda, True, True)
    ), 200


@app.route("/emenda/<int:id_emenda>", methods=['PUT'])
@login_required
@admin_required
def put_emenda(id_emenda):
    emenda = Emenda.query.filter_by(id=id_emenda).first()

    if not emenda:
        return jsonify(mensagem='Emenda não encontrada'), 404

    if 'emenda' in g.data_request:
        emenda.emenda = g.data_request['emenda']

    db.session.commit()

    return jsonify(
        mensagem='Emenda atualizada com sucesso',
        response=return_emenda(emenda, True, True)
    ), 200


# -------------- FERIADOS -----------------------
@app.route("/template/feriado/<int:year>", methods=['POST'])
@login_required
@admin_required
def registar_every_feriado(year):
    local_feriados = Feriado.query.filter(Feriado.data >= str(year)+'-01-01').first()
    if local_feriados:
        return jsonify(mensagem='Feriados nesse ano já existem, a requisição foi bloqueada para evitar réplicas'), 400

    holidays = requests.get(f'https://brasilapi.com.br/api/feriados/v1/{year}').json()
    for holiday in holidays:
        novo_feriado = Feriado(
            data=holiday['date'],
            nome=holiday['name'])

        db.session.add(novo_feriado)

        data_iso: datetime.date = datetime.date.fromisoformat(holiday['date'])
        match data_iso.isoweekday():
            case 2:
                day_before = data_iso - datetime.timedelta(1)
                nova_emenda = Emenda(data=day_before)
                novo_feriado.emenda = nova_emenda
                db.session.add(nova_emenda)

            case 4:
                day_after = data_iso + datetime.timedelta(1)
                nova_emenda = Emenda(data=day_after)
                novo_feriado.emenda = nova_emenda
                db.session.add(nova_emenda)

        db.session.commit()

    return jsonify(mensagem=f"Todos os feriados do ano de {year} foram cadastrados"), 200


@app.route("/feriado", methods=['GET'])
@login_required
@admin_required
def get_feriados():
    feriados = Feriado.query.all()

    if not feriados:
        return jsonify(mensagem="Não há feriados cadastrados"), 404

    feriados_list = []
    for feriado in feriados:
        feriado_dict = return_feriado(feriado, True)
        feriados_list.append(feriado_dict)
        
    return jsonify(mensagem="Todos os feriados cadastrados", response=feriados_list), 200


@app.route("/feriado/<int:id_feriado>", methods=['GET'])
@login_required
@admin_required
def get_feriado(id_feriado):
    feriado = Feriado.query.filter_by(id=id_feriado).first()
    if not feriado:
        return jsonify(mensagem="Feriado não encontrado"), 404

    feriado_dict = return_feriado(feriado, True)

    return jsonify(mensagem="Feriado encontrado", response=feriado_dict), 200


@app.route("/feriado", methods=['POST'])
@login_required
@admin_required
@check_integrity({'nome', 'data'})
def post_feriado():
    novo_feriado = Feriado(
        data=g.data_request['data'],
        nome=g.data_request['nome'])

    db.session.add(novo_feriado)

    data_feriado: str = novo_feriado.data
    data_iso: datetime.date = datetime.date.fromisoformat(data_feriado)
    match data_iso.isoweekday():
        case 2:
            day_before = data_iso - datetime.timedelta(1)
            nova_emenda = Emenda(data=day_before)
            novo_feriado.emenda = nova_emenda
            db.session.add(nova_emenda)

        case 4:
            day_after = data_iso + datetime.timedelta(1)
            nova_emenda = Emenda(data=day_after)
            novo_feriado.emenda = nova_emenda
            db.session.add(nova_emenda)

    db.session.commit()
    return jsonify(mensagem="Feriado criado com sucesso"), 201


@app.route("/feriado/<int:id_feriado>", methods=['PUT'])
@login_required
@admin_required
def put_feriado(id_feriado):
    feriado : Feriado = Feriado.query.filter_by(id=id_feriado).first()
    if not feriado:
        return jsonify(mensagem="Feriado não encontrado"), 404

    feriado_dict = {}

    if 'nome' in g.data_request:
        feriado.nome = g.data_request['nome']

    if 'data' in g.data_request:
        feriado_data = g.data_request['data']
        feriado_datetime: datetime.date = datetime.date.fromisoformat(feriado_data)
        data_iso = feriado.data.isoformat()

        if (data_iso != feriado_data) and (feriado_data != ""):
            feriado.data = feriado_data

            match feriado_datetime.isoweekday():
                case 2:
                    day_before = feriado_datetime - datetime.timedelta(1)
                    feriado.emenda.data = day_before
                    feriado_dict.update(return_emenda(feriado.emenda, True, False))

                case 4:
                    day_after = feriado_datetime + datetime.timedelta(1)
                    feriado.emenda.data = day_after
                    feriado_dict.update(return_emenda(feriado.emenda, True, False))

                case _:
                    db.session.delete(feriado.emenda)

    db.session.commit()

    feriado_dict.update(return_feriado(feriado, True))

    return jsonify(mensagem="Feriado atualizado com sucesso", response=feriado_dict)


@app.route("/feriado/<int:id_feriado>", methods=['DELETE'])
@login_required
@admin_required
def delete_feriado(id_feriado):
    feriado = Feriado.query.filter_by(id=id_feriado).first()
    if not feriado:
        return jsonify(mensagem="Feriado não encontrado"), 404

    db.session.delete(feriado)
    db.session.commit()

    return jsonify(mensagem="Feriado excluído com sucesso"), 200


# ---------------------- USUÁRIO ----------------------


@app.route("/aluno", methods=['GET'])
@login_required
@admin_required
def get_alunos():
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
@login_required
@admin_required
def get_aluno(id_aluno):
    aluno = Aluno.query.filter_by(id=id_aluno).first()

    if not aluno:
        return jsonify(mensagem='Aluno não encontrado'), 404

    aluno_info = return_aluno(aluno, True, True)

    return jsonify(
        mensagem='Informações do aluno',
        response=aluno_info
    ), 200


@app.route("/professor", methods=['GET'])
@login_required
@admin_required
def get_professores():
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
@login_required
@admin_required
def get_professor(id_professor):
    professor = Professor.query.filter_by(id=id_professor).first()

    if not professor:
        return jsonify(mensagem='Professor não encontrado'), 404

    professor_info = return_professor(professor, True, True)

    return jsonify(
        mensagem='Informações do professor',
        response=professor_info
    ), 200


@app.route("/coordenador", methods=['GET'])
@login_required
@admin_required
def get_coordenadores():
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
@login_required
@admin_required
def get_coordenador(id_coordenador):
    coordenador = Coordenador.query.filter_by(id=id_coordenador).first()

    if not coordenador:
        return jsonify(mensagem='Coordenador não encontrado'), 404

    coordenador_info = return_coordenador(coordenador, True)

    return jsonify(
        mensagem='Informações do coordenador',
        response=coordenador_info
    ), 200


@app.route("/usuario", methods=['GET'])
@login_required
@admin_required
def get_usuarios():
    usuarios = Usuario.query.all()

    if not usuarios:
        return jsonify(mensagem='Não há usuários'), 404

    usuarios_dic = []
    for usuario in usuarios:
        usuario_dic = return_usuario(usuario, True)
        usuarios_dic.append(usuario_dic)

    return jsonify(
        mensagem='Lista de Usuarios',
        response=usuarios_dic
    ), 200


@app.route('/usuario', methods=['POST'])
@login_required
@admin_required
@check_integrity({'email', 'senha', 'nome', 'cargo'})
@check_cargo_post({'start_turno', 'end_turno', 'dias_da_semana'})
def post_usuario():
    email = g.data_request['email']
    senha = g.data_request['senha']
    nome = g.data_request['nome']
    cargo = g.data_request['cargo']

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

    match novo_usuario.cargo:
        case CargoChoices.Professor.value:
            novo_professor = Professor(
                start_turno=g.data_request['start_turno'],
                end_turno=g.data_request['end_turno'],
                dias_da_semana=int(g.data_request['dias_da_semana'])
            )
            novo_usuario.professor = novo_professor
            db.session.add(novo_professor)

        case CargoChoices.Coordenador.value:
            novo_coordenador = Coordenador()
            novo_usuario.coordenador = novo_coordenador
            db.session.add(novo_coordenador)

        case CargoChoices.Aluno.value:
            novo_aluno = Aluno()
            novo_usuario.aluno = novo_aluno
            db.session.add(novo_aluno)

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify(
        mensagem=f'{novo_usuario.cargo.name} Cadastrado com Sucesso'
    ), 201


@app.route('/usuario/<int:id_usuario>', methods=['GET'])
@login_required
@admin_required
def get_usuario(id_usuario):
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
@login_required
@check_cargo_put
def put_usuario(id_usuario):
    usuario = Usuario.query.filter_by(id=id_usuario).first()
    if not usuario:
        return jsonify(
            mensagem='Usuário não encontrado',
        ), 404

    if g.usuario['id'] != id_usuario and g.usuario['cargo'] != CargoChoices.Coordenador.value:
        return jsonify(mensagem="Usuário não possui permissão para editar"), 403

    user_response = {}

    match usuario.cargo.value:
        case CargoChoices.Professor.value:
            if usuario.professor.cursos:
                return jsonify(mensagem='Há cursos que dependem desse professor'), 400
            for curso in usuario.professor.cursos:
                if curso['start_curso'] < g.data_request['start_turno'] or curso['end_curso'] > g.data_request['end_curso']:
                    return jsonify(mensagem="Horários de curso conflitantes com horário do professor", curso=curso), 400



            if 'start_turno' in g.data_request:
                usuario.professor.start_turno = g.data_request['start_turno']

            if 'end_turno' in g.data_request:
                usuario.professor.end_turno = g.data_request['end_turno']

            if 'dias_da_semana' in g.data_request:
                usuario.professor.dias_da_semana = int(g.data_request['dias_da_semana'])

            user_response.update(return_professor(usuario.professor, True, True))

    if 'email' in g.data_request:
        user = Usuario.query.filter_by(email=g.data_request['email']).first()
        if user and user != usuario:
            return jsonify(mensagem="Email já cadastrado"), 400

        usuario.email = g.data_request['email']

    if 'senha' in g.data_request:
        usuario.senha = generate_password_hash(g.data_request['senha']).decode('utf-8')

    if 'nome' in g.data_request:
        usuario.nome = g.data_request['nome']

    db.session.commit()

    user_response.update(return_usuario(usuario, True))
    return jsonify(mensagem='Usuário modificado com sucesso', response=user_response), 200


@app.route('/usuario/<int:id_usuario>', methods=['DELETE'])
@login_required
@admin_required
def delete_usuario(id_usuario):
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
@login_required
@admin_required
def get_cursos():
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
    ), 200


@app.route('/curso', methods=['POST'])
@login_required
@admin_required
@check_integrity({'nome', 'carga_horaria', 'start_curso',
                  'end_curso', 'dias_da_semana', 'data_de_inicio',
                  'id_professor', 'id_sala'})
def post_curso():
    novo_curso = Curso(
        nome=g.data_request['nome'],
        carga_horaria=g.data_request['carga_horaria'],
        start_curso=g.data_request['start_curso'],
        end_curso=g.data_request['end_curso'],
        dias_da_semana=g.data_request['dias_da_semana'],
        data_de_inicio=g.data_request['data_de_inicio'],
        id_professor=g.data_request['id_professor'],
        id_sala=g.data_request['id_sala']
    )

    professor : Professor = Professor.query.filter_by(id=novo_curso.id_professor).first()
    if not professor:
        return jsonify(mensagem='Professor não existe'), 400

    sala = Sala.query.filter_by(id=novo_curso.id_sala).first()
    if not sala:
        return jsonify(mensagem='Sala não existe'), 400

    print(novo_curso.start_curso, professor.start_turno)
    if novo_curso.start_curso < professor.start_turno or novo_curso.end_curso > professor.end_turno:
        return jsonify(mensagem="Horários de curso conflitante com horário do professor"), 400

    db.session.add(novo_curso)
    db.session.commit()

    return jsonify(
        mensagem='Curso Cadastrado com Sucesso'
    ), 201


@app.route('/curso<int:id_curso>', methods=['GET'])
@login_required
@admin_required
def get_curso(id_curso):
    curso = Curso.query.filter_by(id=id_curso).first()
    if not curso:
        return jsonify(mensagem='Curso não encontrado'), 404
    
    curso_dict = return_curso(curso, True,
                              True, 
                              True, 
                              True, 
                              True)
    
    return jsonify(mensagem='Curso encontrado', response=curso_dict), 200


@app.route('/curso/<int:id_curso>', methods=['PUT'])
@login_required
@admin_required
def put_curso(id_curso):
    curso = Curso.query.filter_by(id=id_curso).first()
    
    if not curso:
        return jsonify(mensagem='Curso não encontrado'), 404

    if 'nome' in g.data_request:
        curso.nome = g.data_request['nome']
    if 'carga_horaria' in g.data_request:
        curso.carga_horaria = g.data_request['carga_horaria']
    if 'start_curso' in g.data_request:
        curso.start_curso = g.data_request['start_curso']
    if 'end_curso' in g.data_request:
        curso.end_curso = g.data_request['end_curso']
    if 'dias_da_semana' in g.data_request:
        curso.dias_da_semana = g.data_request['dias_da_semana']
    if 'data_de_inicio' in g.data_request:
        curso.data_de_inicio = g.data_request['data_de_inicio']
    if 'id_professor' in g.data_request:
        curso.id_professor = g.data_request['id_professor']
    if 'id_sala' in g.data_request:
        curso.id_sala = g.data_request['id_sala']
    
    db.session.commit()

    return jsonify(
        mensagem='Curso atualizado com sucesso',
        curso=return_curso(curso, True, 
                           True, 
                           True, 
                           True, 
                           True)
    ), 200


@app.route('/curso/<int:id_curso>', methods=['DELETE'])
@login_required
@admin_required
def delete_curso(id_curso):
    curso = Curso.query.filter_by(id=id_curso)
    if not curso:
        return jsonify(mensagem='Curso não encontrado'), 404

    db.session.delete(curso)
    db.session.commit()

    return jsonify(mensagem='Curso removido com sucesso'), 200


# ---------------- SALA ------------------


@app.route('/sala', methods=['GET'])
@login_required
@admin_required
def get_salas():
    salas = Sala.query.all()

    if not salas:
        return jsonify(mensagem='Nenhuma sala encontrada'), 404

    salas_list = []
    for sala in salas:
        sala_dict = return_sala(sala, True, True)
        salas_list.append(sala_dict)

    return jsonify(mensagem='Todas as salas cadastradas', response=salas_list), 200


@app.route('/sala', methods=['POST'])
@login_required
@admin_required
@check_integrity({'nome'})
def post_sala():
    nome = g.data_request['nome']

    sala_existente = Sala.query.filter_by(nome=nome).first()
    if sala_existente:
        return jsonify(mensagem='Sala de mesmo nome já existe'), 400

    nova_sala = Sala(nome=nome)

    db.session.add(nova_sala)
    db.session.commit()
    return jsonify(mensagem='Sala criada com sucesso!'), 201


@app.route('/sala/<int:id_sala>', methods=['GET'])
@login_required
@admin_required
def get_sala(id_sala):
    sala = Sala.query.filter_by(id=id_sala).first()
    if not sala:
        return jsonify(mensagem='Sala não encontrada'), 404

    sala_dict = return_sala(sala, True, True)
    return jsonify(mensagem='Sala encontrada', response=sala_dict), 200


@app.route('/sala/<int:id_sala>', methods=['PUT'])
@login_required
@admin_required
def put_sala(id_sala):
    sala = Sala.query.filter_by(id=id_sala).first()
    if not sala:
        return jsonify(mensagem='Sala não encontrada'), 404

    if 'nome' in g.data_request:
        sala.nome = g.data_request['nome']
    
    db.session.commit()
    sala_dict = return_sala(sala, True, True)
    return jsonify(mensagem='Sala atualizada com sucesso', response=sala_dict), 200


@app.route('/sala/<int:id_sala>', methods=['DELETE'])
@login_required
@admin_required
def delete_sala(id_sala):
    sala: Sala = Sala.query.filter_by(id=id_sala).first()
    if not sala:
        return jsonify(mensagem='Sala não encontrada'), 404

    if sala.cursos:
        cursos_list = []
        for curso in sala.cursos:
            cursos_list.append(return_curso(curso,
                                            True,
                                            True,
                                            True,
                                            False,
                                            True
                                            ))

        return jsonify(mensagem='Há cursos que dependem dessa sala', cursos=cursos_list), 400

    db.session.delete(sala)
    db.session.commit()
    return jsonify(mensagem='Sala deletada com sucesso!'), 200


# -------------- MATRICULAS --------------


@app.route("/matricula", methods=['GET'])
@login_required
@admin_required
def get_matriculas():
    matriculas = Matricula.query.all()

    if not matriculas:
        return jsonify(mensagem='Não há matrículas cadastradas')

    matriculas_dic = []
    for matricula in matriculas:
        matricula_dic = {
            'id_usuario': matricula.id_usuario,
            'id_curso': matricula.id_curso
        }
        matriculas_dic.append(matricula_dic)

    return jsonify(
        mensagem='Lista de matrículas',
        response=matriculas_dic
    ), 200


@app.route("/matricula", methods=['POST'])
@login_required
@admin_required
@check_integrity({'id_usuario', 'id_curso'})
def post_matricula():
    local_aluno = Aluno.query.filter_by(id=g.data_request['id_usuario']).first()
    if not local_aluno:
        return jsonify(mensagem='Usuário não encontrado'), 404

    local_curso = Curso.query.filter_by(id=g.data_request['id_curso']).first()
    if not local_curso:
        return jsonify(mensagem='Curso não encontrado'), 404

    local_aluno.cursos.append(local_curso)
    db.session.commit()

    return jsonify(
        mensagem='Matrícula realizada com sucesso'
    ), 201


@app.route("/matricula/<int:id_curso>/<int:id_usuario>", methods=['DELETE'])
@login_required
@admin_required
def delete_matricula_curso(id_curso, id_usuario):
    local_aluno: Aluno = Aluno.query.filter_by(id=id_usuario).first()
    if not local_aluno:
        return jsonify(mensagem='Aluno não encontrado'), 404

    local_curso: Curso = Curso.query.filter_by(id=id_curso).first()
    if not local_curso:
        return jsonify(mensagem='Curso não encontrado'), 404

    local_aluno.cursos.remove(local_curso)
    db.session.commit()

    return jsonify(
        mensagem='Matrícula deletada com sucesso'
    ), 200
