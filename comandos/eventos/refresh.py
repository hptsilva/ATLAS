import discord
import asyncio
import mysql_connection
from decouple import config
import mysql_connection
from comandos.modal.evento.buttons import Menu_Enquete


COLOR = int(config('COLOR'))

class Refresh():

    async def refresh_views(client):

        MySQLConnector = mysql_connection.MySQLConnector()
        views = await MySQLConnector.pesquisar_all_view()
        for view in views:
            try:
                canal_de_texto = await client.fetch_channel(int(view[2]))
                mensagem = await canal_de_texto.fetch_message(int(view[0]))
            except discord.NotFound:
                await MySQLConnector.excluir_view(view[0])
                await MySQLConnector.excluir_evento(view[0])
                continue
            except discord.HTTPException as e:
                continue
            except discord.Forbidden as e:
                continue
            componentes = mensagem.components
            if componentes == []:
                await MySQLConnector.excluir_view(view[0])
                await MySQLConnector.excluir_evento(view[0])
                continue
            view = Menu_Enquete()
            children = componentes[0].children
            notificacao_button = children[3]
            label_notifacao_button = notificacao_button.label
            estilo_notificacao_button = notificacao_button.style
            children_view = view.children
            button = children_view[6]
            button.label = label_notifacao_button
            button.style = estilo_notificacao_button
            await mensagem.edit(view=view)
        print('- Views resetadas com sucesso!')

