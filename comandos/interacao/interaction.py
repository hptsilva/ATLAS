import discord
import random
import re
import requests
import fuso
import asyncio
from discord.ext import commands
from sql_connection import MySQLConnector

COLOR_ATLAS = 0x1414b8

class Interacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Comando usado para mostrar a foto do perfil de um usuário
    @commands.hybrid_command(description='Veja a foto de perfil de alguém.')
    async def avatar(self, ctx, usuario: discord.User = None):

        if usuario is None:
            usuario = ctx.author
        avatar_url = usuario.avatar.url if usuario.avatar else usuario.default_avatar.url
        embed = discord.Embed(color=COLOR_ATLAS)
        embed.set_image(url=avatar_url)
        display_name = usuario.display_name
        embed.set_author(name=display_name,
                        icon_url='https://onedrive.live.com/embed?resid=4304D643148B3DFB%214304&authkey=%21AET1i2KgxBylAUo&width=677&height=684')
        await ctx.send(embed=embed)

    # Gera um número aletório de 1 até o valor especificado pelo usuário
    @commands.hybrid_command(description='Deixe o bot gerar um valor aleatório de 1 até o número especificado.')
    async def roll(self, ctx, valor: int):

        if(valor < 0):
            await ctx.send(f'Digite um valor maior ou igual a 1', ephemeral=True)
            return
        numero = random.randint(1, valor)
        await ctx.send(f'O valor gerado é: {numero}.')

    # comando para ajudar a usar o comando de eventos
    @commands.hybrid_command(name='ajuda_evento', description='Ajuda para os comandos de evento.')
    @commands.guild_only()
    async def ajuda_evento(self, ctx):

        fuso_valor = '1 : America/Sao_Paulo\n2 : America/Noronha\n3 : America/Belem\n4 : America/Fortaleza\n5 : America/Recife\n6 : America/Araguaina\n7 : America/Maceio\n8 : America/Bahia\n9 : America/Campo_Grande\n10 : America/Cuiaba\n11 : America/Boa_Vista\n12 : America/Manaus\n13 : America/Eirunepe\n14 : America/Rio_Branco'
        embed = discord.Embed(title='Instruções para usar o comando de eventos',
                              color=COLOR_ATLAS)
        embed.add_field(name='fuso_horario',
                        value=f'{fuso_valor}',
                        inline=True)
        await ctx.send(embed=embed, ephemeral=True)

    async def get_image_bytes(self, url):

        response = requests.get(url)
        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            return response.content
        else:
            # Lida com o erro, por exemplo, levanta uma exceção
            raise Exception(f"Erro ao obter imagem da URL. Código de status: {response.status_code}")

async def setup(bot):
    await bot.add_cog(Interacao(bot))
