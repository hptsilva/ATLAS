import discord
import asyncio
import mysql_connection
import pytz
from decouple import config
from discord.ext import commands
from mysql_connection import MySQLConnector
from comandos.modal.evento.buttons import Menu_Enquete
from comandos.eventos.notificar import Notificar
from comandos.eventos.refresh import Refresh

COLOR = int(config('COLOR'))

class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BOT_NAME = config('BOT_NAME')

    # Evento ativado quando o bot é iniciado.
    @commands.Cog.listener()
    async def on_ready(self):

        print('\nIniciando aplicação...')
        await asyncio.sleep(2)
        MySQLConnector = mysql_connection.MySQLConnector()
        await self.bot.tree.sync(guild = None)
        print(f'Número de servidores: {len(self.bot.guilds)}\n')
        print('--------------------------------------------------------')
        print(f'------------------- {self.BOT_NAME} INICIADO ----------------------')
        print('--------------------------------------------------------\n')
        self.bot.loop.create_task(Refresh.refresh_views(self.bot))
        self.bot.loop.create_task(Notificar.notificar_evento(self.bot))

    # Envia uma mensagem em um canal de texto quando o bot entrar no servidor
    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        MySQLConnector = mysql_connection.MySQLConnector()
        # Verifica se o servidor está na base de dados
        resultado = await MySQLConnector.procurar_servidor(guild.id)
        if resultado:
            # reinsere os novo dados do servidor.
            await MySQLConnector.alterar_nome_servidor(guild.id, guild.name)
        else:
            # insere dados do servidor na base da dados caso não esteja
            await MySQLConnector.inserir_servidor(guild.id, guild.name)

    # Evento ativado quando ocorre alteração no servidor (como nome do servidor, por exemplo)
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):

        MySQLConnector = mysql_connection.MySQLConnector()
        name_server = after.name
        if (name_server is not before.name):
            # altera o dado name_server caso o nome do servidor mude
            await MySQLConnector.alterar_nome_servidor(before.id, name_server)

    # Evento ativado quando um usuário entrar no servidor
    @commands.Cog.listener()
    async def on_member_join(self, member):

        MySQLConnector = mysql_connection.MySQLConnector()
        id_server = member.guild.id
        resultado = await MySQLConnector.procurar_servidor(id_server)
        if resultado[3] == 'quarentena':
            await member.kick(reason = "Não é permitido entrar no servidor quando o mesmo está em quarentena")
            return
        resultado = await MySQLConnector.procurar_canal_boas_vindas(id_server)
        if resultado:
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            nome = member.display_name
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
            await asyncio.sleep(0.35)
            await canal.send(content=f'{member.mention}',embed=embed)
            try:
                resultado = await MySQLConnector.pesquisar_cargo(id_server)
                if resultado:
                    role = member.guild.get_role(int(resultado[0]))
                    await member.add_roles(role)
            except:
                return

    # Evento ativado quando um membro sai do servidor. O membro ou o servidor não estão armazenados em cache.
    @commands.Cog.listener()
    async def on_raw_member_remove(self, payload):

        MySQLConnector = mysql_connection.MySQLConnector()
        id_server = payload.guild_id
        member = payload.user
        resultado = await MySQLConnector.pesquisar_canal_removidos(id_server)
        if resultado:
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            embed = discord.Embed(
                title = ':rotating_light: Um membro saiu do servidor :rotating_light:',
                description = f'{member.display_name} não está mais entre nós!',
                color = COLOR
            )
            embed.set_thumbnail(url=avatar_url)
            canal = member.guild.get_channel(int(resultado[0]))
            await canal.send(embed=embed)

    # Verifica se a mensagem enviada foi feita pelo bot e se ela possue uma view
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.id == self.bot.application_id and message.components != []:
            channel = message.channel
            channel_id = channel.id
            guild = message.guild
            guild_id = guild.id
            MySQLConnector = mysql_connection.MySQLConnector()
            await MySQLConnector.inserir_view(message.id, guild_id, channel_id)

async def setup(bot):
    await bot.add_cog(Eventos(bot))
