import pytz
from datetime import datetime, timedelta

class Fuso_Horario():

    def fuso_horario(self, valor, data, horario):

        fuso_dict ={1 : 'America/Sao_Paulo',
                    2 : 'America/Noronha',
                    3 : 'America/Belem',
                    4 : 'America/Fortaleza',
                    5 : 'America/Recife',
                    6 : 'America/Araguaina',
                    7 : 'America/Maceio',
                    8 : 'America/Bahia',
                    9 : 'America/Campo_Grande',
                    10 : 'America/Cuiaba',
                    11 : 'America/Boa_Vista',
                    12 : 'America/Manaus',
                    13 : 'America/Eirunepe',
                    14 : 'America/Rio_Branco'
                    }

        data_hora_str = f"{data} {horario}"
        data_hora_ingenua = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')
        fuso_horario = fuso_dict[valor]
        fuso = pytz.timezone(fuso_horario)
        start_time = fuso.localize(data_hora_ingenua)
        end_time = start_time + timedelta(hours=1)
        return start_time, end_time