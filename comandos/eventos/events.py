import discord
import asyncio
import mysql_connection
import pytz
from decouple import config
from discord.ext import commands
from comandos.eventos.notificar import Notificar
from comandos.eventos.refresh import Refresh
from datetime import datetime

# Conexão com o banco de dados
connection = mysql_connection.MySQLConnector
cnx_user, cursor_user = connection.conectar_user()
cnx_admin, cursor_admin = connection.conectar_admin()

COLOR = int(config('COLOR'))

class Eventos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.BOT_NAME = config('BOT_NAME')
        self.BOT_ID = int(config('BOT_ID'))

    # Evento ativado quando o bot é iniciado.
    @commands.Cog.listener()
    async def on_ready(self):

        print('\nIniciando aplicação...')
        await asyncio.sleep(2)
        await self.bot.tree.sync(guild = None)
        print(f'Número de servidores: {len(self.bot.guilds)}\n')
        print('--------------------------------------------------------')
        print(f'------------------- {self.BOT_NAME} INICIADO ----------------------')
        print('--------------------------------------------------------\n')
        self.bot.loop.create_task(Refresh.refresh_views(self.bot)) # Reseta todos as views do ATLAS.
        self.bot.loop.create_task(Notificar.notificar_evento(self.bot)) #Inicia o processo de notificação automática  de evento.

    # Envia uma mensagem em um canal de texto quando o bot entrar no servidor
    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        # Verifica se o servidor está na base de dados
        consulta = 'SELECT * FROM servidor WHERE id = %s'
        cursor_user.execute(consulta, (guild.id,))
        resultado = cursor_user.fetchone()
        if resultado:
            update_server = 'UPDATE servidor SET nome_servidor = %s, updated_at = %s WHERE id = %s'
            cursor_admin.execute(update_server, (guild.name, datetime.now(), guild.id,))
            cnx_admin.commit()
        else:
            # insere dados do servidor na base da dados caso não esteja
            inserir_server = 'INSERT INTO servidor VALUES(%s, %s, %s, %s, %s, %s)'
            cursor_admin.execute(inserir_server,(guild.id, guild.name, 'Não','liberado', datetime.now(), None))
            cnx_admin.commit()

    # Evento ativado quando ocorre alteração no servidor (como nome do servidor, por exemplo)
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):

        MySQLConnector = mysql_connection.MySQLConnector()
        name_server = after.name
        if (name_server is not before.name):
            # altera o dado name_server caso o nome do servidor mude
            update_server = 'UPDATE servidor SET nome_servidor = %s, updated_at = %s WHERE id = %s'
            cursor_admin.execute(update_server, (name_server, datetime.now(), before.id,))
            cnx_admin.commit()

    # Evento ativado quando um usuário entrar no servidor
    @commands.Cog.listener()
    async def on_member_join(self, member):

        MySQLConnector = mysql_connection.MySQLConnector()
        id_server = member.guild.id
        # Verifica se o servidor possue um canal de entrada cadastrado, se sim, envia a mensagem por ele. Se não nenhuma mensagem de aviso é enviada.
        resultado = await MySQLConnector.procurar_canal_boas_vindas(id_server)
        consulta = 'SELECT * FROM canal_de_boas_vindas WHERE fk_id_servidor = %s'
        cursor_user.execute(consulta, (id_server,))
        resultado = cursor_user.fetchone()
        if resultado:
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            embed = discord.Embed(
                title = f':shield: Bem-vindo ao servidor {member.guild.name} :shield:',
                description = f'{member.display_name}, estamos felizes em tê-lo(a) conosco. Aproveite!',
                color = COLOR
           )
            embed.add_field(name="Nome de usuário:", value=f"`{member.name}`", inline=True)
            embed.add_field(name="ID:", value=f"`{member.id}`", inline=True)
            bot_timezone = pytz.timezone('UTC')
            joined_at_timezone = member.joined_at.astimezone(bot_timezone)
            embed.add_field(name="Entrou em:", value=f"<t:{int(joined_at_timezone.timestamp())}:f>", inline=False)
            embed.set_thumbnail(url=avatar_url)
            canal = member.guild.get_channel(int(resultado[0]))
            try:
                await canal.send(content=f'{member.mention}',embed=embed)
            except:
                pass
            pesquisar = 'SELECT * FROM cargo_de_boas_vindas WHERE fk_id_servidor = %s'
            cursor_user.execute(pesquisar, (id_server,))
            resultado = cursor_user.fetchone()
            if resultado:
                try:
                    role = member.guild.get_role(int(resultado[0]))
                    await member.add_roles(role)
                except:
                    return

    # Evento ativado quando um membro sai do servidor.
    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload):

        MySQLConnector = mysql_connection.MySQLConnector()
        id_server = payload.guild_id
        member = payload.user
        pesquisar = 'SELECT * FROM canal_de_membros_removidos WHERE fk_id_servidor = %s'
        cursor_user.execute(pesquisar, (id_server,))
        resultado = cursor_user.fetchone()
        if resultado:
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            embed = discord.Embed(
                title = ':rotating_light: Um membro saiu do servidor :rotating_light:',
                description = f'{member.display_name} não está mais entre nós!',
                color = COLOR
            )
            embed.set_thumbnail(url=avatar_url)
            canal = member.guild.get_channel(int(resultado[0]))
            try:
                await canal.send(embed=embed)
            except:
                return

    @commands.Cog.listener()
    async def on_message(self, message):

        # Verifica se a mensagem enviada foi feita pelo bot e se ela possue uma view
        if message.author.id == self.bot.application_id and message.components != []:
            channel = message.channel
            guild = message.guild
            MySQLConnector = mysql_connection.MySQLConnector()
            inserir = 'INSERT INTO views VALUES(%s, %s, %s, %s, %s)'
            cursor_user.execute(inserir, (message.id, guild.id, channel.id, datetime.now(), None, ))
            cnx_user.commit()

    @commands.Cog.listener()
    async def on_interaction(self, interaction):

        bot_id = interaction.application_id
        try:
            command = interaction.command
            name = command.name
        except:
            return
        if (bot_id == self.BOT_ID and name):
            MySQLConnector = mysql_connection.MySQLConnector()
            pesquisar = 'SELECT * FROM comandos_usos WHERE comando = %s'
            cursor_admin.execute(pesquisar, (name, ))
            quantidade = cursor_admin.fetchone()
            alterar = 'UPDATE comandos_usos SET quantidade = %s WHERE comando = %s'
            cursor_admin.execute(alterar, (quantidade[1] + 1, name, ))
            cnx_admin.commit()

async def setup(bot):
    await bot.add_cog(Eventos(bot))
