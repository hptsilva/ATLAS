import discord
from decouple import config
from discord.ext import commands

COLOR = int(config('COLOR'))
BOT_NAME = config('BOT_NAME')

class Exclusivo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Alterar atividade do bot. Apenas o dono do bot consegue utilizar o comando.
    @commands.hybrid_command(name = 'alterar_presença', description='Apenas o dono da aplicação consegue usar o comando.')
    @commands.is_owner()
    async def alterarPresenca(self, ctx, op: int, *, frase):

        match op:
            case 1:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=frase))
                await ctx.send('Presença alterada.', ephemeral=True)
            case 2:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=frase))
                await ctx.send('Presença alterada.', ephemeral=True)
            case 3:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=frase))
                await ctx.send('Presença alterada.', ephemeral=True)
            case _:
                await ctx.send(f'Digite uma opção válida:\n1 - Jogando\n2 - Ouvindo\n3 - Assistindo', ephemeral=True)

    # Limpar presença do bot.
    @commands.hybrid_command(name = 'limpar_presença', description='Apenas o dono da aplicação consegue usar o comando.')
    @commands.is_owner()
    async def limparPresenca(self, ctx):

        await self.bot.change_presence(activity=None)
        await ctx.send('Presença alterada.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Exclusivo(bot))
