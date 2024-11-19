import discord
import asyncio
import mysql_connection
import datetime
from decouple import config
from datetime import datetime

COLOR = int(config('COLOR'))

class Notificar():

    async def notificar_evento(client):

        print('- Task de notificação de eventos iniciada!')
        while True:
            MySQLConnector = mysql_connection.MySQLConnector()
            eventos = await MySQLConnector.pesquisar_eventos()
            for evento in eventos:
                if (evento[3] == 'NÃO'):
                    try:
                        canal_de_texto = await client.fetch_channel(int(evento[2]))
                        mensagem = await canal_de_texto.fetch_message(int(evento[0]))
                    except discord.NotFound as e:
                        # Se a mensagem ou o canal de texto não forem encontrados o dado é apagado do banco de dados
                        await MySQLConnector.excluir_evento(evento[0])
                        continue
                    except discord.HTTPException as e:
                        continue
                    except discord.Forbidden as e:
                        continue
                    embed_evento = mensagem.embeds[0]
                    campo_sim = embed_evento.fields[1]
                    value_sim = campo_sim.value
                    value_sim = value_sim.replace(">","").replace(" ","").replace("@","").replace("!","").replace("<","").replace("-","")
                    mencoes_sim = value_sim.split('\n')
                    time = embed_evento.timestamp
                    now_time = datetime.now()
                    segundos_agora = now_time.timestamp()
                    if((int(time.timestamp()) - segundos_agora) < 600):
                        for id_membro in mencoes_sim:
                            if (id_membro == ''):
                                continue
                            guild = client.get_guild(int(evento[1]))
                            membro = await guild.fetch_member(int(id_membro))
                            embed = discord.Embed(
                                title=":rotating_light: UM EVENTO COMEÇARÁ EM BREVE :rotating_light:",
                                color = COLOR
                            )
                            if (guild.icon is not None):
                                embed.set_thumbnail(url = guild.icon.url)
                            embed.add_field(name="Servidor:", value=f"{guild.name}", inline=False)
                            embed.add_field(name='Titulo:', value=f"{embed_evento.title}", inline=False)
                            embed.add_field(name='Horário:', value=f':alarm_clock: <t:{int(time.timestamp())}:f>\n:hourglass: <t:{int(time.timestamp())}:R>', inline=False)
                            if embed_evento.description is not None:
                                embed.add_field(name='Descrição:', value=f"{embed_evento.description}", inline=False)
                            if (embed_evento.image.url is not None):
                                embed.set_image(url=f"{embed_evento.image.url}")
                            try:
                                await membro.send(embed=embed)
                                await asyncio.sleep(0.1)
                            except:
                                continue
                        await MySQLConnector.alterar_evento(evento[0])
            await asyncio.sleep(30)

