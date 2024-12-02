import discord
import random
import requests
from discord.ext import commands
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
    @commands.hybrid_command(name='avatar', description='Veja a foto de perfil de um membro do servidor.')
    @commands.cooldown(10, 120, commands.BucketType.member)
    async def avatar(self, ctx, usuario: discord.User = None):

        if usuario is None:
            usuario = ctx.author
        avatar_url = usuario.avatar.url if usuario.avatar else usuario.default_avatar.url
        embed = discord.Embed(color=COLOR)
        embed.set_image(url=avatar_url)
        display_name = usuario.display_name
        embed.set_author(name=display_name,
                        icon_url="https://cdn.discordapp.com/attachments/1302022249389363210/1302022403605659720/warning.png?ex=6741a11b&is=67404f9b&hm=b938c823f51bb59036433b7549074f0d6667a5f580d28e9bae169707427f5d0e&")
        await ctx.send(embed=embed)

    # Gera um número aletório de 1 até o valor especificado pelo usuário
    @commands.hybrid_command(name='aleatorio', description='Gere um número aleatório de 1 até o valor especificado.')
    @commands.cooldown(50, 60, commands.BucketType.member)
    async def aleatorio(self, ctx, valor: int):

        if(valor < 0):
            await ctx.send(f'Digite um valor maior ou igual a 1', ephemeral=True)
            return
        numero = random.randint(1, valor)
        await ctx.send(f'O valor gerado é: {numero}.')

    # Comando para ajudar a usar o comando de eventos
    @commands.hybrid_command(name='timezone', description='Zonas de tempo disponíveis para o comando /evento.')
    @commands.cooldown(50, 60, commands.BucketType.member)
    @commands.guild_only()
    async def ajuda_evento(self, ctx):

        fuso_valor = '1 : Brazil/Acre (GMT-5)\n2 : Brazil/West (GMT-4)\n3 : Brazil/East (GMT-3)\n4 : Brazil/DeNoronha (GMT-2)'

        embed = discord.Embed(title='Zonas de tempo disponíveis:',
                              color=COLOR)
        embed.add_field(name='',
                        value=f'{fuso_valor}',
                        inline=True)
        await ctx.send(embed=embed, ephemeral=True)

    # Cria um convite para o servidor
    @commands.hybrid_command(name='convite', description='Crie um convite.')
    @commands.guild_only()
    @commands.cooldown(10, 60, commands.BucketType.member) # Limita o uso do comando para 7 usos a cada 60 segundos
    async def criar_convite(self, ctx, segundos: int = None):

        channel = ctx.channel
        if segundos == None:
            invite = await channel.create_invite(max_age=1800, max_uses=1, reason=f'Convite criado por {ctx.author.name} usando o comando /convite.')
        elif (segundos >= 0 and segundos <= 604800):
            invite = await channel.create_invite(max_age=f'{segundos}', max_uses=1, reason=f'Convite criado por {ctx.author.name} usando o comando /convite.')
        else:
            await ctx.send('**Tempo em segundos inválido.**', ephemeral=True)
            return
        await ctx.send(f'Convite criado: {invite.url}', ephemeral=True)

    #Latencia do bot
    @commands.hybrid_command(name='ping', description='Latência da aplicação.')
    @commands.cooldown(10, 120, commands.BucketType.member)
    @commands.cooldown(5, 60, commands.BucketType.member) # Limita o uso do comando para 5 usos a cada 60 segundos
    async def ping(self, ctx):

        ping = self.bot.latency
        ping = "{:.2f}".format(ping)
        await ctx.send(f'Latência: {ping} segundo(s)', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Interacao(bot))
