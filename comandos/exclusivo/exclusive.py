import discord
import asyncio
from discord.ext import commands
from mysql_Connector import MySQLConnector

class Exclusivo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # O bot irá sair do servidor. Apenas o dono do bot consegue utilizar
    @commands.command(name='leaveserver')
    @commands.is_owner()
    async def leaveServer(self, idserver: discord.Guild):

        id_server = idserver.id
        guild = discord.utils.get(self.bot.guilds, id=id_server)
        await guild.leave()

    # Alterar atividade do bot. Apenas o dono do bot consegue utilizar o comando
    @commands.hybrid_command(name = 'alterar_presença', description='Apenas o dono da aplicação consegue usar o comando.')
    @commands.is_owner()
    async def alterarPresenca(self, ctx, op: int, *, frase):

        match op:
            case 1:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=frase))
                await ctx.send('Presença alterada', ephemeral=True)
            case 2:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=frase))
                await ctx.send('Presença alterada', ephemeral=True)
            case 3:
                await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=frase))
                await ctx.send('Presença alterada', ephemeral=True)
            case _:
                await ctx.send(f'Digite uma opção válida:\n1 - Jogando\n2 - Ouvindo\n3 - Assistindo', ephemeral=True)

    @commands.hybrid_command(name='banir_servidor', description='Apenas o dono da aplicação consegue usar o comando.')
    @commands.is_owner()
    async def banir_servidor(self, ctx, servidor: discord.Guild):
        
        MySQLConnector.banir_servidor(MySQLConnector, servidor.id, servidor.name)
        await ctx.send('Servidor banido.', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Exclusivo(bot))