import discord
from decouple import config
from discord.ext import commands

COLOR = int(config('COLOR'))
BOT_NAME = config('BOT_NAME')

class Exclusivo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Alterar atividade do bot. Apenas o dono do bot consegue utilizar o comando.
    @commands.hybrid_command(name = 'status', description='Comando restrito.')
    @commands.is_owner()
    async def status(self, ctx, op: int, *, status):

        match op:
            case 1:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=status))
                await ctx.send('Status alterado.', ephemeral=True)
            case 2:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
                await ctx.send('Status alterado.', ephemeral=True)
            case 3:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
                await ctx.send('Status alterado.', ephemeral=True)
            case _:
                await ctx.send(f'Digite uma opção válida:\n1 - Jogando\n2 - Ouvindo\n3 - Assistindo', ephemeral=True)

    # Limpar presença do bot.
    @commands.hybrid_command(name = 'limpar_status', description='Comando restrito.')
    @commands.is_owner()
    async def limparStatus(self, ctx):

        await self.bot.change_presence(activity=None)
        await ctx.send('Status alterado.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Exclusivo(bot))
