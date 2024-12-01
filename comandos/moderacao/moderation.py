import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import mysql_connection
from datetime import datetime

connection = mysql_connection.MySQLConnector
cnx_user, cursor_user = connection.conectar_user()

class Moderacao(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Expulsar alguém do servidor
    @commands.hybrid_command(name='expulsar',description='Expulse um membro do servidor.')
    @commands.guild_only()
    @commands.cooldown(50, 120, commands.BucketType.member)
    @app_commands.default_permissions(kick_members=True)
    async def expulsar(self, ctx, membro: discord.Member):

        try:
            await membro.kick(reason=f"Expulso(a) via comando por {ctx.author.name}")
        except discord.Forbidden:
            await ctx.send('**O usuário alvo possui um cargo superior ou o ATLAS não tem as permissões necessárias.**', ephemeral=True)
            return
        nome = membro.display_name
        await ctx.send(f'{nome} foi expulso(a) do servidor.')

    # Banir alguém do servidor
    @commands.hybrid_command(name='banir', description ='Bane um membro do servidor.')
    @commands.guild_only()
    @commands.cooldown(50, 120, commands.BucketType.member)
    @app_commands.default_permissions(ban_members=True)
    async def banir(self, ctx, membro: discord.Member):

        try:
            await membro.ban(reason=f"Banido(a) via comando por {ctx.author.name}")
        except discord.Forbidden:
            await ctx.send('**O usuário alvo possui um cargo superior ou o ATLAS não tem as permissões necessárias.**', ephemeral=True)
            return
        nome = membro.display_name
        await ctx.send(f'{nome} foi banido(a) do servidor.')

    # Aplica timeout a alguém no servidor
    @commands.hybrid_command(name='castigar', description='Coloque um membro de castigo (tempo em segundos).')
    @commands.guild_only()
    @commands.cooldown(50, 120, commands.BucketType.member)
    @app_commands.default_permissions(moderate_members=True)
    async def castigar(self, ctx, membro: discord.Member, *, tempo: int):

        try:
            await membro.timeout(timedelta(seconds = tempo))
        except discord.Forbidden:
            await ctx.send('**O usuário alvo possui um cargo superior ou o ATLAS não tem as permissões necessárias.**', ephemeral=True)
            return
        nome = membro.display_name
        await ctx.send(f'{nome} foi colocado(a) de castigo.')

    # Retira o timeout de alguém no servidor
    @commands.hybrid_command(name='tirar_castigo', description='Retire um membro do castigo.')
    @commands.guild_only()
    @commands.cooldown(10, 30, commands.BucketType.member)
    @app_commands.default_permissions(moderate_members=True)
    async def tirar_castigo(self, ctx, membro: discord.Member):

        try:
            if (membro.timed_out_until):
                await membro.timeout(None)
            else:
                await ctx.send('**O usuário alvo não está de castigo.**', ephemeral=True)
                return
        except discord.Forbidden:
            await ctx.send('**O usuário alvo possui um cargo superior ou o ATLAS não tem as permissões necessárias.**', ephemeral=True)
            return
        nome = membro.display_name
        await ctx.send(f'{nome} saiu do castigo.')

    # Excluir todos os convites do servidor
    @commands.hybrid_command(name='excluir_convites', description = 'Exclui todos os convites ativos do servidor.')
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.guild) # Limita o uso de 10 comandos para cada 1 min
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

    # Apague um número determinado de mensagens
    @commands.hybrid_command(name='apagar', description='Apague mensagens do servidor.')
    @app_commands.default_permissions(manage_messages=True)
    @commands.cooldown(5, 60, commands.BucketType.member) # Limita o uso de 5 comandos para cada 1 min
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
    @commands.hybrid_command(name='canal_de_entrada', description='Escolhe um canal de boas-vindas no servidor.')
    @commands.guild_only()
    @commands.cooldown(10, 60, commands.BucketType.guild) # Limita o uso de 10 comandos para cada 1 min
    @app_commands.default_permissions(administrator=True)
    async def escolher_canal_boas_vindas(self, ctx, canal: discord.TextChannel):

        consulta = 'SELECT * FROM canal_de_boas_vindas WHERE fk_id_servidor = %s'
        cursor_user.execute(consulta, (ctx.guild.id,))
        resultado = cursor_user.fetchone()
        if resultado:
            alterar = 'UPDATE canal_de_boas_vindas SET id = %s, updated_at = %s WHERE fk_id_servidor = %s'
            cursor_user.execute(alterar, (canal.id, datetime.now(), ctx.guild.id, ))
            cnx_user.commit()
        else:
            inserir = 'INSERT INTO canal_de_boas_vindas VALUES(%s,%s, %s, %s)'
            cursor_user.execute(inserir, (canal.id, ctx.guild.id, datetime.now(), None, ))
            cnx_user.commit()
        await ctx.send(f'Canal de entrada escolhido.', ephemeral=True)

    # Escolher cargo de boas vindas
    @commands.hybrid_command(name='cargo_de_entrada', description='Escolhe um cargo de entrada no servidor.')
    @commands.guild_only()
    @commands.cooldown(10, 60, commands.BucketType.guild) # Limita o uso de 10 comandos para cada 1 min
    @app_commands.default_permissions(administrator=True)
    async def escolher_cargo_boas_vindas(self, ctx, cargo: discord.Role):

        pesquisar = 'SELECT * FROM cargo_de_boas_vindas WHERE fk_id_servidor = %s'
        cursor_user.execute(pesquisar, (ctx.guild.id,))
        resultado = cursor_user.fetchone()
        if resultado:
            alterar = 'UPDATE cargo_de_boas_vindas SET id = %s, updated_at = %s WHERE fk_id_servidor = %s'
            cursor_user.execute(alterar, (cargo.id, datetime.now(), ctx.guild.id, ))
            cnx_user.commit()
        else:
            inserir = 'INSERT INTO cargo_de_boas_vindas VALUES(%s, %s, %s, %s)'
            cursor_user.execute(inserir, (cargo.id, ctx.guild.id, datetime.now(), None, ))
            cnx_user.commit()
        await ctx.send(f'Cargo de entrada escolhido.', ephemeral=True)

    # Escolher canal de membros que saiu do servidor
    @commands.hybrid_command(name='canal_de_saida', description='Escolhe um canal de saída no servidor.')
    @commands.guild_only()
    @commands.cooldown(10, 60, commands.BucketType.guild) # Limita o uso de 10 comandos para cada 1 min
    @app_commands.default_permissions(administrator=True)
    async def escolher_canal_membros_removidos(self, ctx, canal: discord.TextChannel):

        pesquisar = 'SELECT * FROM canal_de_membros_removidos WHERE fk_id_servidor = %s'
        cursor_user.execute(pesquisar, (ctx.guild.id,))
        resultado = cursor_user.fetchone()
        if resultado:
            alterar = 'UPDATE canal_de_membros_removidos SET id = %s, updated_at = %s WHERE fk_id_servidor = %s'
            cursor_user.execute(alterar, (canal.id, datetime.now(), ctx.guild.id,))
            cnx_user.commit()
        else:
            inserir = 'INSERT INTO canal_de_membros_removidos VALUES(%s, %s, %s, %s)'
            cursor_user.execute(inserir, (canal.id, ctx.guild.id, datetime.now(), None,))
            cnx_user.commit()
        await ctx.send(f'Canal de saída escolhido.', ephemeral=True)

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
