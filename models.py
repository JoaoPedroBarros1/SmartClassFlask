import enum
from main import db


class CargoChoices(enum.Enum):
    Coordenador = 'COORDENADOR'
    Professor = 'PROFESSOR'
    Aluno = 'ALUNO'


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100))
    senha = db.Column(db.String(100))
    nome = db.Column(db.String(100))
    cargo = db.Column(db.Enum(CargoChoices))
    aluno = db.relationship('Aluno', backref='usuario', uselist=False)
    professor = db.relationship('Professor', backref='usuario', uselist=False)
    coordenador = db.relationship('Coordenador', backref='usuario', uselist=False)


class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    carga_horaria = db.Column(db.Time)
    duracao = db.Column(db.Time)
    dias_da_semana = db.Column(db.Integer)
    data_de_inicio = db.Column(db.DateTime)
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id'))
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id'))


class Aluno(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))


class Professor(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    carga_horaria = db.Column(db.Time)
    start_turno = db.Column(db.Time)
    end_turno = db.Column(db.Time)
    dias_da_semana = db.Column(int)


class Coordenador(db.Model):
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))


class Matricula(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    id_curso = db.Column(db.Integer, primary_key=True)

class NaoLetivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    nome = db.Column(db.String(255), nullable=False)

class Reposicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)

class Feriado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    nome = db.Column(db.String(255), nullable=False)
