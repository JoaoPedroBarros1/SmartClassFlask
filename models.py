import enum
from main import db


class CargoChoices(enum.Enum):
    COORDENADOR = 'Coordenador',
    PROFESSOR = 'Professor',
    ALUNO = 'Aluno'


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
    carga_horaria = db.Column(db.Integer)
    duracao = db.Column(db.Integer)
    dias_da_semana = db.Column(db.Integer)
    data_de_inicio = db.Column(db.Date)
    horario = db.Column(db.Time)
    id_professor = db.Column(db.Integer)
    id_sala = db.Column(db.Integer)
