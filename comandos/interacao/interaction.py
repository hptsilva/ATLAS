import discord
import random
import re
import requests
import timezone
from discord.ext import commands
from mysql_connection import MySQLConnector
from decouple import config

COLOR = int(config('COLOR'))

class Interacao(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Converte o link da imagem para o formato bytes
    async def get_image_bytes(self, url):

        response = requests.get(url)
        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            return response.content
        else:
            # Lida com o erro, por exemplo, levanta uma exceção
            raise Exception(f"Erro ao obter imagem da URL. Código de status: {response.status_code}")


    # Comando usado para mostrar a foto do perfil de um usuário
    @commands.hybrid_command(name='avatar', description='Veja a foto de perfil de alguém.')
    async def avatar(self, ctx, usuario: discord.User = None):

        if usuario is None:
            usuario = ctx.author
        avatar_url = usuario.avatar.url if usuario.avatar else usuario.default_avatar.url
        embed = discord.Embed(color=COLOR)
        embed.set_image(url=avatar_url)
        display_name = usuario.display_name
        embed.set_author(name=display_name,
                        icon_url="https://onedrive.live.com/embed?resid=4304D643148B3DFB%214304&authkey=%21AET1i2KgxBylAUo&width=677&height=684")
        await ctx.send(embed=embed)

    # Gera um número aletório de 1 até o valor especificado pelo usuário
    @commands.hybrid_command(name='roll', description='Deixe o bot gerar um valor aleatório de 1 até o número especificado.')
    async def roll(self, ctx, valor: int):

        if(valor < 0):
            await ctx.send(f'Digite um valor maior ou igual a 1', ephemeral=True)
            return
        numero = random.randint(1, valor)
        await ctx.send(f'O valor gerado é: {numero}.')

    # O bot cria um evento personalizado
    @commands.hybrid_command(name='evento2', description='#2 Evento - Crie um evento no servidor.')
    @commands.guild_only()
    async def evento(self, ctx, fuso_horario: int, horario: str, data: str, canal: discord.VoiceChannel, titulo: str, descricao: str = None, url_da_imagem: str = None):

        await ctx.send('Processando...', ephemeral=True)
        padrao_horario = r'^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9])$'
        padra_data = r'^(202[3-9])-(0[0-9]|1[0-2])-(0[0-9]|1[0-9]|2[0-9]|3(0-1))$'
        corresponde_horario = re.match(padrao_horario, horario)
        corresponde_data = re.match(padra_data, data)
        if corresponde_horario and corresponde_data:
            try:
                Fuso_Horario = timezone.Fuso_Horario()
                start_time, end_time, now_time = await Fuso_Horario.fuso_horario(fuso_horario, data, horario)
            except:
                await ctx.send(f'Fuso horário inválido.', ephemeral=True)
                return
            try:
                if descricao is None:
                    descricao = ''
                # Faz o upload da imagem para o discord, caso o link seja inválido retorna mensagem de aviso e interrompe o comando.
                try:
                    image_bytes = await self.get_image_bytes(url_da_imagem)
                except:
                    if url_da_imagem is None:
                        image_bytes = None
                    else:
                        await ctx.send('Link da imagem inválido', ephemeral=True)
                        return
                guild = ctx.guild
                privacy_level = discord.PrivacyLevel.guild_only
                entity_type=discord.EntityType.voice
                # Cria um evento sem uma imagem.
                if image_bytes == None:
                    event = await guild.create_scheduled_event(name=f'{titulo}',
                                                               description=f'{descricao}',
                                                               channel=canal,
                                                               start_time=start_time,
                                                               end_time=end_time,
                                                               entity_type=entity_type,
                                                               privacy_level=privacy_level,
                                                               reason=f'Evento criado por {ctx.author.name} usando o comando /evento2')
                # Cira um evento com uma imagem.
                else:
                    event = await guild.create_scheduled_event(name=f'{titulo}',
                                                               description=f'{descricao}',
                                                               channel=canal,
                                                               start_time=start_time,
                                                               end_time=end_time,
                                                               entity_type=entity_type,
                                                               privacy_level=privacy_level,
                                                               image=image_bytes,
                                                               reason=f'Evento criado por {ctx.author.name} usando o comando /evento2')
                uuid = await MySQLConnector.inserir_evento(MySQLConnector, event.id, ctx.guild.id, ctx.author.id)
                member_obj = self.bot.get_user(ctx.author.id)
                embed = discord.Embed(title='Evento criado',
                                      color=COLOR)
                embed.add_field(name='ID do evento:',
                                value=f'```{uuid}```',
                                inline=False)
                embed.add_field(name='Título do evento:',
                                value=f'{titulo}',
                                inline=False)
                embed.add_field(name='Descrição:',
                                value= f'{descricao}' if descricao else 'None',
                                inline=False)
                # Se o servidor não tiver um banner, o bot irá desconsiderar essa condição.
                try:
                    guild_banner_url = ctx.guild.icon.url
                    embed.set_thumbnail(url=f'{guild_banner_url}')
                except:
                    pass
                embed.set_footer(text=f'Servidor: {ctx.guild.name}')
                try:
                    # Envia informações do evento na dm do criador.
                    dm = await member_obj.send(embed=embed)
                except:
                    await ctx.send('Não foi possível enviar uma mensagem direta informando a ID do evento para realizar a edição.',ephemeral=True)
                await MySQLConnector.inserir_dm_evento(MySQLConnector, dm.id, uuid)
                await ctx.send(f'{event.url}')
            except:
                await ctx.send('Ocorreu um erro durante o processo de criação do evento. Se o problema persistir, informe o dono da aplicação.', ephemeral=True)
        else:
            await ctx.send('O horário e data devem estar no formato HH:MM e AAAA:MM:DD respectivamente.', ephemeral=True)

    # Comando para ajudar a usar o comando de eventos
    @commands.hybrid_command(name='timezone', description='Zonas de tempo disponíveis para o comando /evento1 e /evento2.')
    @commands.guild_only()
    async def ajuda_evento(self, ctx):

        fuso_valor = '1 : Brazil/Acre (GMT-5)\n2 : Brazil/West (GMT-4)\n3 : Brazil/East (GMT-3)\n4 : Brazil/DeNoronha (GMT-2)'

        embed = discord.Embed(title='Zonas de tempo disponíveis.',
                              color=COLOR)
        embed.add_field(name='',
                        value=f'{fuso_valor}',
                        inline=True)
        await ctx.send(embed=embed, ephemeral=True)

    # Edita um evento no servidor.
    @commands.hybrid_command(name='editar_evento2', description='#2 Evento - Edite um evento no servidor.')
    @commands.guild_only()
    async def editar_evento(self, ctx, id: str, titulo: str = None, descricao: str = None, url_da_imagem: str = None, channel: discord.VoiceChannel = None):

        if titulo == None and descricao == None and url_da_imagem == None and channel == None:
            await ctx.send('Nenhum parâmetro foi alterado.', ephemeral=True)
            return
        uuid_regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        padrao_uuid = re.match(uuid_regex, id)
        if padrao_uuid:
            pesquisar = await MySQLConnector.pesquisar_evento(MySQLConnector, id, ctx.author.id, ctx.guild.id)
        else:
            await ctx.send("ID inválido.", ephemeral=True)
            return
        await ctx.send('Procurando evento...', ephemeral=True)
        if pesquisar:
            id_evento = pesquisar[1]
            scheduled_event = await ctx.guild.fetch_scheduled_event(id_evento)
            end_time = scheduled_event.end_time
            start_time = scheduled_event.start_time
            status = scheduled_event.status
            title = titulo if titulo is not None else scheduled_event.name
            description = descricao if descricao is not None else scheduled_event.description
            if description == '{apagar}':
                description = ''
            try:
               image = await self.get_image_bytes(url_da_imagem) if url_da_imagem is not None else await self.get_image_bytes(scheduled_event.cover_image.url)
            except:
                image = None
            voice_channel = channel if channel is not None else scheduled_event.channel
            if image == None:
                await scheduled_event.edit(name=title,
                                       description=description,
                                       channel=voice_channel,
                                       start_time=start_time,
                                       end_time=end_time,
                                       privacy_level=discord.PrivacyLevel.guild_only,
                                       entity_type=discord.EntityType.voice,
                                       status=status)
            else:
                await scheduled_event.edit(name=title,
                                           description=description,
                                           channel=voice_channel,
                                           start_time=start_time,
                                           end_time=end_time,
                                           privacy_level=discord.PrivacyLevel.guild_only,
                                           entity_type=discord.EntityType.voice,
                                           status=status,
                                           image=image)
            await ctx.send('Alteração realizada.', ephemeral=True)
            id_dm_mensagem = pesquisar[4]
            DMChannel = self.bot.get_user(ctx.author.id)
            try:
                dm_message = await DMChannel.fetch_message(id_dm_mensagem)
            except:
                await ctx.send('Não foi encontrada a mensagem enviada por DM para alteração.', ephemeral=True)
                return
            # Altera as informações dos dados enviado na dm do criador do evento.
            novo_embed = discord.Embed(title='Evento Criado',
                                      color=COLOR)
            novo_embed.add_field(name='ID do evento:',
                                 value=f'```{id}```',
                                 inline=False)
            novo_embed.add_field(name='Título do evento:',
                                 value=f'{title}',
                                 inline=False)
            novo_embed.add_field(name='Descrição:',
                                 value=f'{description}',
                                 inline=False)
            try:
                guild_banner_url = ctx.guild.icon.url
                novo_embed.set_thumbnail(url=f'{guild_banner_url}')
            except:
                pass
            novo_embed.set_footer(text=f'Servidor: {ctx.guild.name}')
            try:
                await dm_message.edit(embed=novo_embed)
            except:
                await ctx.send('Não foi possível alterar a mensagem enviada na DM.', ephemeral=True)
                return
        else:
            await ctx.send('O evento não foi encontrado no servidor ou você não é o criador do evento.', ephemeral=True)

    # Cancela o evento no servidor. Apenas o criador do evento pode cancelar o evento.
    @commands.hybrid_command(name='cancelar_evento2', description='#2 Evento - Cancele um evento no servidor.')
    @commands.guild_only()
    async def cancelar_evento(self, ctx, id: str):

        uuid_regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        padrao_uuid = re.match(uuid_regex, id)
        if padrao_uuid:
            pesquisar = await MySQLConnector.pesquisar_evento(MySQLConnector, id, ctx.author.id, ctx.guild.id)
        else:
            await ctx.send("ID inválido.", ephemeral=True)
            return
        await ctx.send('Procurando evento...', ephemeral=True)
        if pesquisar:
            id_evento = pesquisar[1]
            scheduled_event = await ctx.guild.fetch_scheduled_event(id_evento)
            await scheduled_event.delete()
            await ctx.send('Evento cancelado.', ephemeral=True)
        else:
            await ctx.send('O evento não foi encontrado no servidor ou você não é o criador do evento.', ephemeral=True)

    # Inicia o evento no servidor. Apenas o criador do evento pode iniciar o evento.
    @commands.hybrid_command(name='iniciar_evento2', description='#2 Evento - Inicie um evento no servidor.')
    @commands.guild_only()
    async def iniciar_evento(self, ctx, id: str):

        uuid_regex = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        padrao_uuid = re.match(uuid_regex, id)
        if padrao_uuid:
            pesquisar = await MySQLConnector.pesquisar_evento(MySQLConnector, id, ctx.author.id, ctx.guild.id)
        else:
            await ctx.send("ID inválido.", ephemeral=True)
            return
        await ctx.send('Procurando evento...', ephemeral=True)
        if pesquisar:
            # Se o evento existir e o autor do comando for o criador do evento, o mesmo é iniciado.
            try:
                id_evento = pesquisar[1]
                event = await ctx.guild.fetch_scheduled_event(id_evento)
                await event.start(reason=None)
                await ctx.send('Evento iniciado.', ephemeral=True)
            except:
                await ctx.send('Não foi possível iniciar o evento.', ephemeral=True)
        else:
            await ctx.send('O evento não foi encontrado no servidor ou você não é o criador do evento.', ephemeral=True)

    # Cria um convite para o servidor
    @commands.hybrid_command(name='criar_convite', description='Crie um convite. O convite expira depois de 10 min após a criação.')
    @commands.guild_only()
    @commands.cooldown(7, 60, commands.BucketType.member) # Limita o uso do comando para 7 usos a cada 60 segundos
    async def criar_convite(self, ctx):

        channel = ctx.channel
        invite = await channel.create_invite(max_age=600, max_uses=1, reason=f'Convite criado por {ctx.author.name} usando o comando /criar_convite.')
        await ctx.send(f'Convite criado: {invite.url}', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Interacao(bot))
