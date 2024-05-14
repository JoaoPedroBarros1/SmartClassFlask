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


class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100))
    carga_horaria = db.Column(db.Time)
    duracao = db.Column(db.Time)
    dias_da_semana = db.Column(db.Integer)
    data_de_inicio = db.Column(db.DATETIME)
    id_professor = db.Column(db.Integer)
    id_sala = db.Column(db.Integer)


class Matricula(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    id_curso = db.Column(db.Integer, primary_key=True)
