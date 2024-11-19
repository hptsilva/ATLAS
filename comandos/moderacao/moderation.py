import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import mysql_connection

class Moderacao(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Expulsar alguém do servidor
    @commands.hybrid_command(name='expulsar',description='Expulse alguém do servidor.')
    @commands.guild_only()
    @app_commands.default_permissions(kick_members=True)
    async def expulsar(self, ctx, membro: discord.Member):

        await membro.kick(reason=f"Expulso(a) via comando por {ctx.author.name}")
        nome = membro.display_name
        await ctx.send(f'{nome} foi expulso(a) do servidor.')

    # Banir alguém do servidor
    @commands.hybrid_command(name='banir', description ='Bane alguém do servidor.')
    @commands.guild_only()
    @app_commands.default_permissions(ban_members=True)
    async def banir(self, ctx, membro: discord.Member):

        await membro.ban(reason=f"Banido(a) via comando por {ctx.author.name}")
        nome = membro.display_name
        await ctx.send(f'{nome} foi banido(a) do servidor.')

    # Aplica timeout a alguém no servidor
    @commands.hybrid_command(name='castigar', description='Coloque um membro de castigo (tempo em segundos).')
    @commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    async def castigar(self, ctx, membro: discord.Member, *, tempo: int):

        await membro.timeout(timedelta(seconds = tempo))
        nome = membro.display_name
        await ctx.send(f'{nome} foi colocado(a) de castigo.')

    # Retira o timeout de alguém no servidor
    @commands.hybrid_command(name='tirar_castigo', description='Retire um membro do castigo.')
    @commands.guild_only()
    @app_commands.default_permissions(moderate_members=True)
    async def tirar_castigo(self, ctx, membro: discord.Member):

        await membro.timeout(None)
        nome = membro.display_name
        await ctx.send(f'{nome} saiu do castigo.')

    # Excluir todos os convites do servidor
    @commands.hybrid_command(name='excluir_convites', description = 'Exclui todos os convites do servidor.')
    @commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def excluir_convites(self, ctx):

        await ctx.send('**Processando...**', ephemeral=True)
        id_server = ctx.guild.id
        guild = self.bot.get_guild(id_server)
        invites = await guild.invites()
        if(invites):
            for invite in invites:
                await self.bot.delete_invite(invite)
            await ctx.send('Convite(s) excluído(s) com sucesso.', ephemeral=True)
        else:
            await ctx.send('Não existem convites ativos no servidor.', ephemeral=True)

    # Coloca todos os membros do servidor em timeout, exceto os administradores.
    @commands.hybrid_command(name='quarentena', description = 'Coloque o servidor em quarentena.')
    @commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def quarentena(self, ctx):

        await ctx.send('**Ativando quarentena no servidor...**', ephemeral=True)
        MySQLConnector = mysql_connection.MySQLConnector()
        id_server = ctx.guild.id
        guild = self.bot.get_guild(id_server)
        resultado = await MySQLConnector.procurar_servidor(id_server)
        if resultado:
            try:
                # Revoga todos os convites ativos no servidor
                invites = await guild.invites()
                for invite in invites:
                    await self.bot.delete_invite(invite)
                for member in ctx.guild.members:
                    if not member.guild_permissions.administrator:
                        # coloca os membros em timeout num período de 24 horas
                        await member.timeout(timedelta(hours=24), reason='Servidor em quarentena')
                # altera o status do servidor para quarentena
                await MySQLConnector.alterar_quarentena(id_server, 'quarentena')
                await ctx.send('**Servidor fechado.**', ephemeral=True)
            except:
                await ctx.send('Ocorreu algum erro durante o comando. Informe o dono da aplicação.', ephemeral=True)
        else:
            await ctx.send('Servidor não encontrado na base de dados. Informe o dono da aplicação.', ephemeral=True)

    # Retira o timeout para todos os membros do servidor.
    @commands.hybrid_command(name='liberar', description='Libere o servidor da quarentena.')
    @commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def liberar(self, ctx):

        await ctx.send('**Desativando quarentena no servidor...**', ephemeral=True)
        MySQLConnector = mysql_connection.MySQLConnector()
        id_server = ctx.guild.id
        # procura o servidor na base de dados
        resultado = await MySQLConnector.procurar_servidor(id_server)
        if resultado:
            try:
                for member in ctx.guild.members:
                    if not member.guild_permissions.administrator:
                        # retira timeout dos membros do servidor
                        await member.timeout(None, reason=None)
                # altera os status do servidor para liberado
                await MySQLConnector.alterar_quarentena(id_server, 'liberado')
                await ctx.send('**Servidor liberado.**', ephemeral=True)
            except:
                await ctx.send('Ocorreu algum erro durante o comando. Informe o dono da aplicação.', ephemeral=True)
        else:
            await ctx.send('Servidor não encontrado na base de dados. Informe o dono da aplicação.', ephemeral=True)

    # Apague um número determinado de mensagens
    @commands.hybrid_command(name='apagar', description='Apague mensagens do servidor.')
    @app_commands.default_permissions(administrator=True)
    @commands.guild_only()
    async def apagar(self, ctx, quantidade: int):

        if quantidade <= 0:
            await ctx.send('Digite um valor maior que 0.', ephemeral=True)
            return
        await ctx.send(f'Deletando mensagens...', ephemeral=True)
        numero = 1
        while numero <= quantidade:
            mensagem = await ctx.channel.purge(limit=1)
            if mensagem == []:
                return
            await asyncio.sleep(0.35)
            numero += 1

    # Escolhe o canal de boas vindas
    @commands.hybrid_command(name='canal_de_boas_vindas', description='Escolhe um canal de texto para ser o canal de boas-vindas.')
    @commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def escolher_canal_boas_vindas(self, ctx, canal: discord.TextChannel):

        MySQLConnector = mysql_connection.MySQLConnector()
        await MySQLConnector.escolher_canal_de_boas_vindas(ctx.guild.id, canal)
        await ctx.send(f'Canal de boas-vindas escolhido.', ephemeral=True)

    # Escolher cargo de boas vindas
    @commands.hybrid_command(name='cargo_de_boas_vindas', description='Escolhe um cargo que o membro irá ganhar ao entrar no servidor.')
    @commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def escolher_cargo_boas_vindas(self, ctx, cargo: discord.Role):

        MySQLConnector = mysql_connection.MySQLConnector()
        await MySQLConnector.inserir_cargo(cargo, ctx.guild.id)
        await ctx.send(f'Cargo de boas-vindas escolhido.', ephemeral=True)

    # Escolher canal de membros que saiu do servidor
    @commands.hybrid_command(name='canal_membros_removidos', description='Escolhe um canal de texto para notificação quando um membro sair do servidor.')
    @commands.guild_only()
    @app_commands.default_permissions(administrator=True)
    async def escolher_canal_membros_removidos(self, ctx, canal: discord.TextChannel):

        MySQLConnector = mysql_connection.MySQLConnector()
        await MySQLConnector.escolher_canal_removidos(canal, ctx.guild.id)
        await ctx.send(f'Canal de membros removidos escolhido.', ephemeral=True)

    # Comando usado para apagar mensagens privadas do bot
    @commands.hybrid_command(name='apagar_dm', description='Apague mensagens privadas do ATLAS.')
    @commands.cooldown(1, 300, commands.BucketType.member) # Limita o uso do comando para a cada 5 min
    @commands.dm_only()
    async def apagar_dm_mensagens(self, ctx):

        member_obj = self.bot.get_user(ctx.author.id)
        await ctx.send('Pesquisando mensagens...', ephemeral=True)
        messages = [message async for message in member_obj.history(limit=None)]
        if messages == []:
            await ctx.send('Não existem mensagens do ATLAS na sua dm.', ephemeral=True)
            return
        for message in messages:
            try:
                await message.delete()
            except:
                pass
            await asyncio.sleep(0.5)
        await ctx.send('Concluído.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderacao(bot))
