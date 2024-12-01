import discord
import mysql_connection
from decouple import config
import mysql_connection
from comandos.modal.evento.buttons import Menu_Enquete


COLOR = int(config('COLOR'))
connection = mysql_connection.MySQLConnector
cnx_user, cursor_user = connection.conectar_user()
cnx_admin, cursor_admin = connection.conectar_admin()


class Refresh():

    async def refresh_views(client):

        recuperar = 'SELECT * FROM views'
        cursor_user.execute(recuperar)
        views = cursor_user.fetchall()
        for view in views:
            try:
                canal_de_texto = await client.fetch_channel(int(view[2]))
                mensagem = await canal_de_texto.fetch_message(int(view[0]))
            except discord.NotFound:
                excluir = 'DELETE FROM views WHERE id = %s'
                cursor_admin.execute(excluir, (view[0], ))
                cnx_admin.commit()
                excluir = 'DELETE FROM eventos WHERE id = %s'
                cursor_admin.execute(excluir, (view[0], ))
                cnx_admin.commit()
                continue
            except discord.HTTPException as e:
                continue
            except discord.Forbidden as e:
                continue
            componentes = mensagem.components
            if componentes == []:
                excluir = 'DELETE FROM views WHERE id = %s'
                cursor_admin.execute(excluir, (view[0], ))
                cnx_admin.commit()
                excluir = 'DELETE FROM eventos WHERE id = %s'
                cursor_admin.execute(excluir, (view[0], ))
                cnx_admin.commit()
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

