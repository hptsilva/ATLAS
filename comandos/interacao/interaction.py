import discord
import datetime
import random
import re
from datetime import datetime
from discord.ext import commands
from logComando import ComandoLog
from mysql_Connector import MySQLConnector
from fuso_horario import Fuso_Horario

instanceLog = ComandoLog

class Interacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando usado para mostrar a foto do perfil de um usuário
    @commands.hybrid_command(description='Veja a foto de perfil de alguém.')
    async def avatar(self, ctx, usuario: discord.User = None):

        if usuario is None:
            usuario = ctx.author
        avatar_url = usuario.avatar.url if usuario.avatar else usuario.default_avatar.url
        embed = discord.Embed(color=0xf24f00)
        embed.set_image(url=avatar_url)
        display_name = usuario.display_name
        embed.set_author(name=display_name,
                        icon_url="https://lh3.googleusercontent.com/drive-viewer/AK7aPaBPRFRq_BBCPOK65PnGCT7xaY9PxPonJh-mc3_urBV1YGgLcF1ujGdS6JwCCPoMa3jpMbSmGWcoL8KYz-kMSseYsZk0pQ=s2560")
        await ctx.send(embed=embed)
        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $iavatar {usuario.display_name}\n"
        instanceLog.salvar_log(comando_log)

    # Gera um número aletório de 1 até o valor especificado pelo usuário
    @commands.hybrid_command(description='Deixe o bot gerar um valor aleatório de 1 até o número especificado.')
    async def roll(self, ctx, valor: int):

        if(valor < 0):
            await ctx.send(f'Digite um valor maior ou igual a 1', ephemeral=True)
            return
        numero = random.randint(1, valor)
        await ctx.send(f'O valor gerado é: {numero}.')
        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $iroll {numero}\n"
        instanceLog.salvar_log(comando_log)

    # O bot irá enviar uma mensagem chamando todos os membros do servidor
    @commands.hybrid_command(description='Chame todos do servidor para uma raid - Limite de uso de 5 min por servidor.')
    @commands.cooldown(1, 300, commands.BucketType.guild) # Limita o uso do comando para cada 5 min por servidor (300seg = 5min)
    async def raid(self, ctx):

        allowed_mentions = discord.AllowedMentions(everyone=True) # Permite o bot mencionar todos os membros do servidor
        await ctx.send(content=f'**Chamando todos os agentes para uma Raid** @everyone', allowed_mentions=allowed_mentions)
        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $iraid\n"
        instanceLog.salvar_log(comando_log)

    # O bot irá enviar uma mensagem chamando todos os membros do servidor
    @commands.hybrid_command(description='Chame agentes para uma Incursão')
    @commands.cooldown(1, 300, commands.BucketType.guild) # Limita o uso do comando para cada 5 min por servidor (300seg = 5min)
    async def incursao(self, ctx):

        allowed_mentions = discord.AllowedMentions(everyone=True) # Permite o bot mencionar todos os membros do servidor
        await ctx.send(content=f'**Chamando agentes para uma Incursão** @everyone', allowed_mentions=allowed_mentions)
        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $iincursao\n"
        instanceLog.salvar_log(comando_log)

    # O bot irá enviar uma dm chamando os membros do servidor para uma raid
    @commands.hybrid_command(name='dm_raid', description='O bot enviará um convite para uma raid aos membros escolhidos. (2 min a cada uso)')
    @commands.cooldown(1, 120, commands.BucketType.member) # Limita o uso do comando para cada 2 min por servidor (120seg = 2min)
    async def raid_dm(self, ctx, membro1: discord.User, membro2: discord.User = None, membro3: discord.User = None, membro4: discord.User = None, membro5: discord.User = None, membro6: discord.User = None, membro7: discord.User = None):

        invite = await ctx.channel.create_invite(max_age=300, max_uses=1)
        member_list = [membro1, membro2, membro3, membro4, membro5, membro6, membro7]
        author = ctx.author.display_name
        name_guild = ctx.guild
        embed = discord.Embed(title=':rotating_light: Você recebeu um convite para um grupo de raid :rotating_light:',
                            description=f'Convite  de {author} feito no servidor {name_guild}\nLink: {invite.url}',
                            color = 0xf24f00)
        for member in member_list:
            if member is None:
                continue
            member_id = member.id
            guild_banner_url = ctx.guild.icon.url
            member_obj = self.bot.get_user(member_id)
            embed.set_thumbnail(url=guild_banner_url)
            embed.set_footer(text='Não é necessário responder a mensagem. Não irei enviar nenhuma confirmação.')
            await member_obj.send(embed=embed)
        await ctx.send('**Convite enviado**', ephemeral=True)
        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $iraid_dm\n"
        instanceLog.salvar_log(comando_log)

    @commands.hybrid_command(name='dm_incursao', description='O bot enviará um convite para uma incursão aos membros escolhidos. (2 min a cada uso)')
    @commands.cooldown(1, 120, commands.BucketType.member) # Limita o uso do comando para cada 2 min por membro (120seg = 2min)
    async def incursao_dm(self, ctx, membro1: discord.User, membro2: discord.User = None, membro3: discord.User = None):

        invite = await ctx.channel.create_invite(max_age=300, max_uses=1)
        member_list = [membro1, membro2, membro3]
        author = ctx.author.display_name
        name_guild = ctx.guild
        embed = discord.Embed(title=':rotating_light: Você recebeu um convite para um grupo de incursão :rotating_light:',
                            description=f'Convite  de {author} feito no servidor {name_guild}\nLink: {invite.url}',
                            color = 0xf24f00)
        for member in member_list:
            if member is None:
                continue
            member_id = member.id
            guild_banner_url = ctx.guild.icon.url
            member_obj = self.bot.get_user(member_id)
            embed.set_thumbnail(url=guild_banner_url)
            embed.set_footer(text='Não é necessário responder a mensagem. Não irei enviar nenhuma confirmação.')
            await member_obj.send(embed=embed)
        await ctx.send('**Convite enviado**', ephemeral=True)
        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $iincursao_dm\n"
        instanceLog.salvar_log(comando_log)

    @commands.hybrid_command(name='evento_terra_de_cego', description='(Teste) Cria um evento sobre raid Terra de Cego.')
    async def enquete_raid(self, ctx, fuso_horario: int, horario: str, data: str, canal: discord.VoiceChannel):

        padrao_horario = r'^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$'
        padra_data = r'^(202[3-9])-(0[0-9]|1[0-2])-(0[0-9]|1[0-9]|2[0-9]|3(0-1))$'
        corresponde_horario = re.match(padrao_horario, horario)
        corresponde_data = re.match(padra_data, data)
        if corresponde_horario and corresponde_data:
            try:
                start_time, end_time = Fuso_Horario.fuso_horario(Fuso_Horario, fuso_horario, data, horario)
            except:
                await ctx.send('Fuso horário inválido.', ephemeral=True)
                return
            embed = discord.Embed(title=f'**Você irá participar da raid Terra de Cego?**',
                                  description='Use as reações disponíveis para interagir',
                                  color=0xf24f00)
            embed.add_field(name='Presença:', value='✅ - Sim\n❌ - Não\n⚠️ - Talvez', inline=False)
            embed.timestamp = start_time
            embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
            embed.add_field(name='Nomes: ✅ - Sim', value=f'', inline=True)
            embed.add_field(name='Nomes: ❌ - Não', value=f'', inline=True)
            embed.add_field(name='Nomes: ⚠️ - Talvez', value=f'', inline=True)
            embed.set_image(url='https://lh3.googleusercontent.com/drive-viewer/AK7aPaA4YP60IYRiofNZhCo0tMpaZKoy9gZKeUvpphtzCYSwx_FXiq4i7yGHJG1GjgmL4oHe1dwMHmuQOTmdoE5W2b4BVj8Abg=s1600')
            embed.set_footer(text=f'Enquete criada por {ctx.author.display_name}\nVersão de teste')
            mensagem = await ctx.send(embed=embed)
            await mensagem.add_reaction('✅')
            await mensagem.add_reaction('❌')
            await mensagem.add_reaction('⚠️')
            MySQLConnector.inserir_enquete(MySQLConnector, ctx.guild.id, mensagem.id)
            guild = ctx.guild
            privacy_level = discord.PrivacyLevel.guild_only
            entity_type=discord.EntityType.voice
            try:
                await guild.create_scheduled_event(name=embed.title,
                                                description='',
                                                channel=canal,
                                                start_time=start_time,
                                                end_time=end_time,
                                                entity_type=entity_type,
                                                privacy_level=privacy_level,
                                                reason='Evento criado para o jogo The Division 2')
            except:
                await ctx.channel.purge(limit=1)
                await ctx.send('Não é possível criar um evento do passado.', ephemeral=True)
        else:
            await ctx.send('O horário ou a data não estão nos formatos corretos (hh:mm) e (aaaa-mm-dd) ou não são válidos.', ephemeral=True)

    @commands.hybrid_command(name='evento_cavalo_de_ferro', description='(Teste) Cria um evento sobre a Raid Cavalo de Ferro.')
    async def enquete_incursao(self, ctx, fuso_horario: int, horario: str, data: str, canal: discord.VoiceChannel):

        padrao_horario = r'^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$'
        padra_data = r'^(202[3-9])-(0[0-9]|1[0-2])-(0[0-9]|1[0-9]|2[0-9]|3(0-1))$'
        corresponde_horario = re.match(padrao_horario, horario)
        corresponde_data = re.match(padra_data, data)
        if corresponde_horario and corresponde_data:
            try:
                start_time, end_time = Fuso_Horario.fuso_horario(Fuso_Horario, fuso_horario, data, horario)
            except:
                await ctx.send('Fuso horário inválido.', ephemeral=True)
                return
            embed = discord.Embed(title=f'**Você irá participar da Raid Cavalo de Ferro?**',
                                  description='Use as reações disponíveis para interagir',
                                  color=0xf24f00)
            embed.add_field(name='Presença:', value='✅ - Sim\n❌ - Não\n⚠️ - Talvez', inline=False)
            embed.timestamp = start_time
            embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
            embed.add_field(name='Nomes: ✅ - Sim', value=f'', inline=True)
            embed.add_field(name='Nomes: ❌ - Não', value=f'', inline=True)
            embed.add_field(name='Nomes: ⚠️ - Talvez', value=f'', inline=True)
            embed.set_image(url='https://lh3.googleusercontent.com/drive-viewer/AK7aPaDPDTP1zz19DzlSM2KV0WRydIMOQpYYrCxaRGQ3lbUkallxyp4gFySGPOMzXDRRhoVRr7ca-UzgYnUN9lhBqCKE4f29=s1600')
            embed.set_footer(text=f'Enquete criada por {ctx.author.display_name}\nVersão de teste')
            mensagem = await ctx.send(embed=embed)
            await mensagem.add_reaction('✅')
            await mensagem.add_reaction('❌')
            await mensagem.add_reaction('⚠️')
            MySQLConnector.inserir_enquete(MySQLConnector, ctx.guild.id, mensagem.id)
            guild = ctx.guild
            privacy_level = discord.PrivacyLevel.guild_only
            entity_type=discord.EntityType.voice
            try:
                await guild.create_scheduled_event(name=embed.title,
                                                description='',
                                                channel=canal,
                                                start_time=start_time,
                                                end_time=end_time,
                                                entity_type=entity_type,
                                                privacy_level=privacy_level,
                                                reason='Evento criado para o jogo The Division 2')
            except:
                await ctx.channel.purge(limit=1)
                await ctx.send('Não é possível criar um evento do passado.', ephemeral=True)
        else:
            await ctx.send('O horário ou a data não estão nos formatos corretos (hh:mm) e (aaaa-mm-dd) ou não são válidos.', ephemeral=True)

    @commands.hybrid_command(name='ajuda_evento', description='Ajuda para os comandos de evento.')
    async def ajuda_evento(self, ctx):
        
        fuso_valor = '1 : America/Sao_Paulo\n2 : America/Noronha\n3 : America/Belem\n4 : America/Fortaleza\n5 : America/Recife\n6 : America/Araguaina\n7 : America/Maceio\n8 : America/Bahia\n9 : Amercia/Campo_Grande\n10 : America/Cuiaba\n11 : America/Boa_Vista\n12 : America/Manaus\n13 : America/Eirunepe\n14 : America/Rio_Branco'

        embed = discord.Embed(title='Instruções para usar o comando de eventos',
                              color=0xf24f00)
        embed.add_field(name='fuso_horario',
                        value=f'{fuso_valor}',
                        inline=True)
        embed.add_field(name='horario',
                        value='Tipo: HH:MM',
                        inline=False)
        embed.add_field(name='data',
                        value='Tipo: AAAA-MM-DD',
                        inline=False)
        embed.add_field(name='canal',
                        value='Canal de voz do servidor',
                        inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Interacao(bot))