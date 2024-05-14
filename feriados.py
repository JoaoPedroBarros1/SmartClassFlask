import enum
import requests


class WeekDays(enum.Enum):
    SEGUNDA = 1
    TERCA = 2
    QUARTA = 4
    QUINTA = 8
    SEXTA = 16
    SABADO = 32
    DOMINGO = 64


def handle_aulas(curso):
    print(curso.data_de_inicio.__dir__)
    response = requests.get('http://date.nager.at/api/v3/PublicHolidays/' + curso.data_de_inicio.year() + '/BR')
    if response.status_code != 200:
        return {'error': True, 'mensagem': 'Falha ao obter feriados'}

    feriados = response.json()
    dias_letivos = []

    qtd_dias_por_semana = 1
    qtd_aulas = (curso.carga_horaria / curso.duracao) / qtd_dias_por_semana

    dia = 1
    while dia <= qtd_aulas:
        date = {
            'dia': 0,
            'dia_da_semana': 0
        }
        dias_letivos.append(date)
        dia += 1

    return {'error': False,
            'mensagem': 'Dias letivos retornados',
            'dias_letivos': dias_letivos}


# TERCA QUINTA SEXTA SABADO - 116
days_count = 0
