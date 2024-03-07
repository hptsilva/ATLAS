import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from guild_owner import GuildOwner
import sql_connection

class Moderacao(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Expulsar alguém do servidor
    @commands.hybrid_command(description='Expulse alguém do servidor.')
    @commands.guild_only()
    @app_commands.default_permissions(kick_members=True)
    async def expulsar(self, ctx, membro: discord.Member):

        await membro.kick(reason="Expulso por solicitação do dono do servidor")
        await ctx.send(f'{membro.display_name} foi expulso do servidor.')

    # Banir alguém do servidor
    @commands.hybrid_command(description ='Bane alguém do servidor.')
    @commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    async def banir(self, ctx, membro: discord.Member):

        await membro.ban(reason="Banido por solicitação do dono do servidor")
        await ctx.send(f'{membro.display_name} foi banido do servidor.')

    # Aplica timeout a alguém no servidor
    @commands.hybrid_command(name='colocar_castigo', description='Coloque um membro em timeout (tempo em segundos).')
    @commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    async def colocar_castigo(self, ctx, membro: discord.Member, *, tempo: float):

        await membro.timeout(timedelta(seconds = tempo), reason='Solitação do dono do servidor')
        await ctx.send(f'{membro.display_name} foi colocado de castigo.')

    # Retira o timeout de alguém no servidor (É possível usar o comando em alguém mesmo ele não tendo recebido timeout. O discord.py não dá suporte para reconhecer qual membro recebeu timeout)
    @commands.hybrid_command(name='tirar_castigo', description='Retire um membro do timeout.')
    @commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    async def tirar_castigo(self, ctx, membro: discord.Member):

        await membro.timeout(None, reason='Solicitação do dono do servidor')
        await ctx.send(f'{membro.display_name} saiu do castigo.')

    # Coloca todos os membros do servidor em timeout, exceto os administradores.
    @commands.hybrid_command(description = 'Coloque o servidor em quarentena.')
    @commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def quarentena(self, ctx):


        MySQLConnector = sql_connection.MySQLConnector()
        id_server = ctx.guild.id
        resultado = await MySQLConnector.procurar_servidor(id_server)
        if resultado:
            # alterar status do servidor
            await MySQLConnector.alterar_quarentena(id_server, 'quarentena')
            for member in ctx.guild.members:
                if not member.guild_permissions.administrator:
                    # coloca os membros em timeout num período de 24 horas
                    await member.timeout(timedelta(hours=24), reason='Servidor em quarentena')
            await ctx.send('**Protoco de quarentena ativado**', ephemeral=True)
        else:
            await ctx.send('Servidor não encontrado na base de dados. Informe o dono do bot', ephemeral=True)

    # Retira o timeout para todos os membros do servidor.
    @commands.hybrid_command(description='Libere o servidor da quarentena.')
    @commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def liberar(self, ctx):

        MySQLConnector = sql_connection.MySQLConnector()
        id_server = ctx.guild.id
        resultado = await MySQLConnector.procurar_servidor(id_server)
        if resultado:
            await MySQLConnector.alterar_quarentena(id_server, 'liberado')
            for member in ctx.guild.members:
                if not member.guild_permissions.administrator:
                    # retira timeout dos membros do servidor
                    await member.timeout(None, reason=None)
            await ctx.send('**Protocolo de quarentena desativado**', ephemeral=True)
        else:
            await ctx.send('Servidor não encontrado na base de dados. Informe o dono do bot', ephemeral=True)

    # Apague um número determinado de mensagens
    @commands.hybrid_command(name='apagar_mensagens', description='Apague mensagens do servidor.')
    @app_commands.default_permissions(administrator=True)
    @commands.guild_only()
    async def apagar(self, ctx, quantidade: int):

        if quantidade < 0:
            await ctx.send('Envie um valor positivo', ephemeral=True)
            return
        await ctx.send(f'Deletando mensagens...', ephemeral=True)
        numero = 1
        while numero <= quantidade:
            mensagem = await ctx.channel.purge(limit=1)
            if mensagem == []:
                return
            await asyncio.sleep(0.35)
            numero += 1

    # Escolhe o canal de boas-vindas do servidor
    @commands.hybrid_command(name='escolher_canal_de_boas_vindas', description='Escolhe um canal de texto, que será o canal de boas-vindas.')
    @commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def escolher_canal_boas_vindas(self, ctx, canal: discord.TextChannel):

        MySQLConnector = sql_connection.MySQLConnector()
        await MySQLConnector.escolher_canal_de_boas_vindas(ctx.guild.id, canal)
        await ctx.send(f'Canal de boas-vindas escolhido', ephemeral=True)

    @commands.hybrid_command(name='apagar_dm_mensagens', description='Comando usado para apagar mensagens do bot em mensagens diretas.')
    @commands.cooldown(1, 7200, commands.BucketType.member)
    async def apagar_dm_mensagens(self, ctx):

        member_obj = self.bot.get_user(ctx.author.id)
        await ctx.send('Pesquisando mensagens do bot na sua DM...', ephemeral=True)
        messages = [message async for message in member_obj.history(limit=None)]
        if messages == []:
            await ctx.send('Não há mensagens a serem apagadas.', ephemeral=True)
            return
        for message in messages:
            try:
                await message.delete()
            except:
                pass
            await asyncio.sleep(0.5)

async def setup(bot):
    await bot.add_cog(Moderacao(bot))

