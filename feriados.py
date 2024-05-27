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


#--------------------- Verificando os dias da semana e dos feriados: --------------
    while len(dias_letivos) < qtd_aulas:
        if dia_corrente.weekday() in curso.dias_da_semana:
            date = {
                'dia': dia_corrente.strftime('%Y-%m-%d'),
                'dia_da_semana': dia_corrente.weekday()
            }

            feriado = next((f for f in feriados if f['date'] == date['dia']), None) #vai verificar se tem feriado no dia do curso


# ------------------- Verificar se o curso é na quinta ou na terça----------------
            if feriado:
                if dia_corrente.weekday() == WeekDays.QUINTA:
                    dias_perdidos += 2
                elif dia_corrente.weekday() == WeekDays.TERCA:
                    dias_perdidos += 2
                else:
                    dias_letivos.append (date)

