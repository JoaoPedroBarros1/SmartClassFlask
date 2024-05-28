import enum
from app import db


class CargoChoices(enum.Enum):
    Coordenador = 'COORDENADOR'
    Professor = 'PROFESSOR'
    Aluno = 'ALUNO'


Matricula = db.Table(
    'matricula',
    db.Column('id_aluno', db.Integer, db.ForeignKey('aluno.id'), primary_key=True),
    db.Column('id_curso', db.Integer, db.ForeignKey('curso.id'), primary_key=True)
)


class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)

    cursos = db.relationship('Curso', back_populates='sala', lazy=True)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.Enum(CargoChoices), nullable=False)

    aluno = db.relationship('Aluno', back_populates='usuario', uselist=False, cascade="all, delete-orphan")
    professor = db.relationship('Professor', back_populates='usuario', uselist=False, cascade="all, delete-orphan")
    coordenador = db.relationship('Coordenador', back_populates='usuario', uselist=False, cascade="all, delete-orphan")


class Aluno(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)

    usuario = db.relationship('Usuario', back_populates='aluno')
    cursos = db.relationship('Curso', secondary=Matricula, back_populates='alunos')


class Professor(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    start_turno = db.Column(db.Time, nullable=False)
    end_turno = db.Column(db.Time, nullable=False)
    dias_da_semana = db.Column(db.Integer, nullable=False)

    usuario = db.relationship('Usuario', back_populates='professor')
    cursos = db.relationship('Curso', back_populates='professor', lazy=True)


class Coordenador(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)

    usuario = db.relationship('Usuario', back_populates='coordenador')


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    carga_horaria = db.Column(db.Time, nullable=False)
    duracao = db.Column(db.Time, nullable=False)
    dias_da_semana = db.Column(db.Integer, nullable=False)
    data_de_inicio = db.Column(db.DateTime, nullable=False)
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)

    sala = db.relationship('Sala', back_populates='cursos', lazy=True)
    professor = db.relationship('Professor', back_populates='cursos', lazy=True)
    alunos = db.relationship('Aluno', secondary=Matricula, back_populates='cursos')
    reposicoes = db.relationship('Reposicao', back_populates='curso', lazy=True)


class NaoLetivo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    nome = db.Column(db.String(100), nullable=False)

    emenda = db.Column(db.Boolean, nullable=False)


class Feriado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    nome = db.Column(db.String(100), nullable=False)

    emenda = db.Column(db.Boolean, nullable=False)


class Reposicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    id_curso = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)

    curso = db.relationship('Curso', back_populates='reposicoes')
