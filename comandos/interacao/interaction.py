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


    # Comando para ajudar a usar o comando de eventos
    @commands.hybrid_command(name='timezone', description='Zonas de tempo disponíveis para o comando /evento.')
    @commands.guild_only()
    async def ajuda_evento(self, ctx):

        fuso_valor = '1 : Brazil/Acre (GMT-5)\n2 : Brazil/West (GMT-4)\n3 : Brazil/East (GMT-3)\n4 : Brazil/DeNoronha (GMT-2)'

        embed = discord.Embed(title='Zonas de tempo disponíveis.',
                              color=COLOR)
        embed.add_field(name='',
                        value=f'{fuso_valor}',
                        inline=True)
        await ctx.send(embed=embed, ephemeral=True)

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
