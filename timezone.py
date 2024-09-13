import pytz
from datetime import datetime, timedelta

class Fuso_Horario:

    async def fuso_horario(self, valor, data, horario):

        fuso_dict ={
            1 : 'Brazil/Acre',
            2 : 'Brazil/West',
            3 : 'Brazil/East',
            4: 'Brazil/DeNoronha',
        }

        data_hora_str = f"{data} {horario}"
        data_hora_ingenua = datetime.strptime(data_hora_str, '%Y-%m-%d %H:%M')
        fuso_horario = fuso_dict[valor]
        fuso = pytz.timezone(fuso_horario)
        start_time = fuso.localize(data_hora_ingenua)
        end_time = start_time + timedelta(hours=2)
        now_time = datetime.now()
        return start_time, end_time, now_time
