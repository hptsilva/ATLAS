import discord
import asyncio
import sql_connection
import reactions
from discord.ext import commands
from sql_connection import MySQLConnector
from reactions import Reacoes_Enquete

COLOR_ATLAS = 0x1414b8

class Eventos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Evento ativado quando o bot é iniciado.
    @commands.Cog.listener()
    async def on_ready(self):

        MySQLConnector = sql_connection.MySQLConnector()
        await self.bot.tree.sync(guild = None)
        print(f'\nBot ({self.bot.user}) iniciado - (ID: {self.bot.user.id})')
        ordem = 1
        # Lista os nomes e IDs do servidores que o Bot é membro e atualiza o banco de dados caso o nome do servidor foi alterado
        print(f'Número de servidores: {len(self.bot.guilds)}\n')
        print(f'--------------------------------------------------------')
        for guild in self.bot.guilds:
            print(f'#{ordem} Servidor ({guild.name}) - ID ({guild.id})')
            resultado = await MySQLConnector.procurar_servidor(guild.id)
            if resultado is None:
                await MySQLConnector.inserir_servidor(guild.id, guild.name)
            elif resultado[2] is not guild.name:
                await MySQLConnector.alterar_nome_servidor(guild.id, guild.name)
            ordem += 1
        print(f'--------------------------------------------------------')
        print('--------------------APLICAÇÃO INICIADA------------------')
        print(f'--------------------------------------------------------')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        MySQLConnector = sql_connection.MySQLConnector()
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

        MySQLConnector = sql_connection.MySQLConnector()
        name_server = after.name
        if (name_server is not before.name):
            # altera o dado name_server caso o nome do servidor mude
            await MySQLConnector.alterar_nome_servidor(before.id, name_server)

    # Evento ativado quando um usuário entrar no servidor
    @commands.Cog.listener()
    async def on_member_join(self, member):

        MySQLConnector = sql_connection.MySQLConnector()
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
                title = f':rotating_light: Seja bem-vindo :rotating_light:',
                description = f'{nome} entrou no servidor!',
                color = COLOR_ATLAS
            )
            embed.set_thumbnail(url=avatar_url)
            canal = member.guild.get_channel(int(resultado[0]))
            try:
                await canal.send(embed=embed)
            except:
                return

async def setup(bot):
    await bot.add_cog(Eventos(bot))
