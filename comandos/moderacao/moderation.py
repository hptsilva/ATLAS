import discord
import asyncio
import datetime
from discord.ext import commands
from datetime import timedelta
from logComando import ComandoLog
from guild_owner import GuildOwner
from mysql_Connector import MySQLConnector

class Moderacao(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Expulsar alguém do servidor
    @commands.hybrid_command(description='Expulsar alguém do servidor - Apenas administradores usam o comando.')
    @commands.has_permissions(administrator=True)
    async def expulsar(self, ctx, membro: discord.Member):

        await membro.kick(reason="Expulso por solicitação do dono do servidor")
        await ctx.send(f'{membro.mention} foi expulso do servidor.')
        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $iexpulsar {membro.display_name}\n"
        ComandoLog.salvar_log(comando_log)

    # Banir alguém do servidor
    @commands.hybrid_command(description ='Banir alguém do servidor - Apenas administradores usam o comando.')
    @commands.has_permissions(administrator=True)
    async def banir(self, ctx, membro: discord.Member):

        await membro.ban(reason="Banido por solicitação do dono do servidor")
        await ctx.send(f'{membro.mention} foi banido do servidor.')
        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $ibanir {membro.display_name}\n"
        ComandoLog.salvar_log(comando_log)

    # Aplica timeout a alguém no servidor
    @commands.hybrid_command(description='Colocar um membro em timeout (tempo em minutos) - Apenas administradores usam o comando.')
    @commands.has_permissions(administrator=True)
    async def castigo(self, ctx, membro: discord.Member, *, tempo: int):    

        await membro.timeout(timedelta(minutes = tempo), reason="Solitação do dono do servidor")
        await ctx.send(f'{membro.mention} foi colocado de castigo.')
        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $icastigo {membro.display_name}\n"
        ComandoLog.salvar_log(comando_log)

    # Coloca todos os membros do servidor em timeout, exceto os administradores.
    @commands.hybrid_command(description = 'Coloca o servidor em quarentena - Apenas administradores usam o comando.')
    @commands.has_permissions(administrator=True)
    async def quarentena(self, ctx):

        id_server = ctx.guild.id
        resultado = MySQLConnector.procurar_servidor(MySQLConnector,id_server)
        if resultado:
            # alterar status do servidor
            MySQLConnector.alterar_quarentena(MySQLConnector, id_server, 'quarentena')
            for member in ctx.guild.members:
                if not member.guild_permissions.administrator:
                    # coloca os membros em timeout num período de 24 horas
                    await member.timeout(timedelta(hours=24), reason='Servidor em quarentena')
            await ctx.send('**Protoco de quarentena ativado**', ephemeral=True)
        else:
            await ctx.send('Servidor não encontrado na base de dados. Informe o dono do bot', ephemeral=True)

    # Retira o timeout para todos os membros do servidor.
    @commands.hybrid_command(description='Libera o servidor da quarentena - Apenas administradores usam o comando.')
    @commands.has_permissions(administrator=True)
    async def liberar(self, ctx):

        id_server = ctx.guild.id
        resultado = MySQLConnector.procurar_servidor(MySQLConnector,id_server)
        if resultado:
            MySQLConnector.alterar_quarentena(MySQLConnector, id_server, 'liberado')
            for member in ctx.guild.members:
                if not member.guild_permissions.administrator:
                    # retira timeout dos membros do servidor
                    await member.timeout(None, reason=None)
            await ctx.send('**Protocolo de quarentena desativado**', ephemeral=True)
        else:
            await ctx.send('Servidor não encontrado na base de dados. Informe o dono do bot', ephemeral=True)

    # Mostra a lista de pessoas banidas no servidor
    @commands.hybrid_command(description='Lista os membros banidos do servidor - Apenas administradores usam o comando.')
    @commands.has_permissions(administrator=True)
    async def banlist(self, ctx):

        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $ibanlist\n"
        ComandoLog.salvar_log(comando_log)
        await ctx.send(f'Lista de banidos:')
        async for entry in ctx.guild.bans():
            texto += await ctx.send(f'Nome: {entry.user}. Motivo: {entry.reason}')

    # Apague um número determinado de mensagens
    @commands.hybrid_command(name='apagar', description='(Teste) Apague mensagens - Apenas administradores usam o comando.')
    @commands.has_permissions(administrator=True)
    async def apagar(self, ctx, valor: int):

        if valor < 0:
            await ctx.send('Envie um valor positivo', ephemeral=True)
            return
        await ctx.send(f'Deletando mensagens...\n**Obs: Por motivos de sobrecarga, as mensagens serão apagadas uma a uma a cada 500 milissegundos**', ephemeral=True)
        numero = 1
        while numero <= valor:
            mensagem = await ctx.channel.purge(limit=1)
            if mensagem == []:
                return
            await asyncio.sleep(0.5)
            numero += 1

    @commands.hybrid_command(name='escolher_canal_de_boas_vindas', description='Escolha um canal de texto, que será o canal de boas-vindas.')
    @commands.check_any(GuildOwner.is_guild_owner())
    async def escolher_canal(self, ctx, canal: discord.TextChannel):

        MySQLConnector.escolher_canal_de_boas_vindas(MySQLConnector, ctx.guild.id, canal)
        await ctx.send(f'Canal de boas-vindas escolhido', ephemeral=True)

    @commands.hybrid_command(name='escolher_canal_twitch', description='(Teste) Escolha um canal de texto, que será o canal de notificações da twitch.')
    @commands.check_any(GuildOwner.is_guild_owner())
    async def escolher_canal(self, ctx, canal: discord.TextChannel):

        MySQLConnector.escolher_canal_twitch(MySQLConnector, ctx.guild.id, canal)
        await ctx.send(f'Canal da twitch escolhido', ephemeral=True)

    @commands.hybrid_command(name='inserir_streamer', description='(Teste) Escolha o streamer que terá a live notificada')
    @commands.check_any(GuildOwner.is_guild_owner())
    async def escolher_canal(self, ctx, membro: discord.Member):

        MySQLConnector.escolher_streamer(MySQLConnector, ctx.guild.id, membro)
        await ctx.send(f'Streamer inserido', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderacao(bot))