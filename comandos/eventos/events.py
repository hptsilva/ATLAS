import discord
import asyncio
from discord.ext import commands
from mysql_Connector import MySQLConnector

class Eventos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Evento ativado quando o bot é iniciado.
    @commands.Cog.listener()
    async def on_ready(self):

        await self.bot.tree.sync(guild = None)
        # Altera a atividade do bot
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Starfield'))
        print(f'\nBot ({self.bot.user}) iniciado - (ID: {self.bot.user.id})')
        ordem = 1
        # Lista os nomes e IDs do servidores que o Bot é membro e atualiza o banco de dados caso o nome do servidor foi alterado
        print(f'Número de servidores: {len(self.bot.guilds)}\n')
        print(f'--------------------------------------------------------')
        for guild in self.bot.guilds:
            print(f'#{ordem} Servidor ({guild.name}) - ID ({guild.id})')
            resultado = MySQLConnector.procurar_servidor(MySQLConnector, guild.id)
            if resultado is None:
                MySQLConnector.inserir_servidor(MySQLConnector,guild.id, guild.name)
            elif resultado[2] is not guild.name:
                MySQLConnector.alterar_nome_servidor(MySQLConnector,guild.id, guild.name)
            ordem += 1
        print(f'--------------------------------------------------------\n')

    # Envia uma mensagem em um canal de texto quando o bot entrar no servidor
    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        # Verifica se o servidor está na base de dados
        resultado = MySQLConnector.procurar_Servidor(MySQLConnector,guild.id)
        if resultado:
            # reinsere os novo dados do servidor.
            MySQLConnector.alterar_nome_servidor(MySQLConnector,guild.id, guild.name)
        else:
            # insere dados do servidor na base da dados caso não esteja
            MySQLConnector.inserir_servidor(MySQLConnector,guild.id, guild.name)

    # Evento ativado quando ocorre alteração no servidor (como nome do servidor, por exemplo)
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):

        name_server = after.name
        if (name_server is not before.name):
            # altera o dado name_server caso o nome do servidor mude
            MySQLConnector.alterar_nome_servidor(MySQLConnector,before.id, name_server)

    # Evento ativado quando um usuário entrar no servidor
    @commands.Cog.listener()
    async def on_member_join(self, member):

        id_server = member.guild.id
        resultado = MySQLConnector.procurar_servidor(MySQLConnector,id_server)
        if resultado[3] == 'quarentena':
            await member.kick(reason = "Não é permitido entrar no servidor quando o mesmo está em quarentena")
            return
        resultado = MySQLConnector.procurar_canal_boas_vindas(MySQLConnector, id_server)
        if resultado:
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            nome = member.name
            embed = discord.Embed(
                title = f':rotating_light: Seja bem-vindo :rotating_light:',
                description = f'{nome} entrou no servidor!',
                color = 0x1948bf
            )
            embed.set_thumbnail(url=avatar_url)
            canal = member.guild.get_channel(int(resultado[0]))
            await asyncio.sleep(1.5)
            await canal.send(embed=embed)

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        
        if before.activity == after.activity:
            return
        if type(after.activity) is discord.activity.Streaming:
            resultado = MySQLConnector.procurar_canal_twitch(MySQLConnector, after.guild.id)
            if resultado:
                name = after.activity.name
                game = after.activity.game
                twitch_name = after.activity.twitch_name
                twitch_url = after.activity.url
                canal = before.guild.get_channel(int(resultado[0]))
                await canal.send(f'Stream iniciada {name}, {game}, {twitch_name}, {twitch_url}')

async def setup(bot):
    await bot.add_cog(Eventos(bot))