import discord
import datetime
import random
from discord.ext import commands
from logComando import ComandoLog

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
        embed = discord.Embed(color=0x1948bf)
        embed.set_image(url=avatar_url)
        display_name = usuario.display_name
        embed.set_author(name=display_name,
                        icon_url="https://lh3.googleusercontent.com/drive-viewer/AK7aPaAorQOW2PpP7d8xyxCq3Z9OFRBJlj3R1sa6S9N3QiPTUJQQTMVwtUMdYFSrIXXN5FiufKDtJGNLNtPLfW5t6Mk-SA8B=s2560")
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

    # O bot irá enviar uma dm chamando os membros do servidor para uma raid
    @commands.hybrid_command(name='dm_jogar', description='O bot enviará um convite para o membro escolhido (2 min a cada uso).')
    @commands.cooldown(1, 120, commands.BucketType.member) # Limita o uso do comando para cada 2 min por servidor (120seg = 2min)
    async def dm_jogar(self, ctx, membro: discord.User, jogo: str):

        invite = await ctx.channel.create_invite(max_age=300, max_uses=1)
        author = ctx.author.display_name
        name_guild = ctx.guild
        embed = discord.Embed(title=f':rotating_light: Você recebeu um convite para jogar {jogo} :rotating_light:',
                            description=f'Convite  de {author} feito no servidor {name_guild}\nLink: {invite.url}',
                            color = 0x1948bf)
        member_id = membro.id
        guild_banner_url = ctx.guild.icon.url
        member_obj = self.bot.get_user(member_id)
        embed.set_thumbnail(url=guild_banner_url)
        embed.set_footer(text='Não é necessário responder a mensagem. Não irei enviar nenhuma confirmação.')
        await member_obj.send(embed=embed)
        await ctx.send('**Convite enviado**', ephemeral=True)
        comando_log = f"[{datetime.datetime.now()} -- {ctx.author} -- {ctx.guild} -- Canal de Texto: ({ctx.channel})]: $idm_jogar\n"
        instanceLog.salvar_log(comando_log)

async def setup(bot):
    await bot.add_cog(Interacao(bot))
