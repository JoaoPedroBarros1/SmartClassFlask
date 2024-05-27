import requests
from datetime import datetime


def handle_aulas(curso):
    response = requests.get('http://date.nager.at/api/v3/PublicHolidays/{}/BR'.format(curso.data_de_inicio.year))
    if response.status_code != 200:
        return {'error': True, 'mensagem': 'Falha ao obter feriados'}

    feriados = response.json()
    dias_letivos = []
    qtd_dias_por_semana = 1
    qtd_aulas = (curso.carga_horaria / curso.duracao) / qtd_dias_por_semana

    dia_corrente = curso.data_de_inicio
    dias_perdidos = 0




