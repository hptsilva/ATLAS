from decouple import config
from discord.ext import commands
from mysql_Connector import MySQLConnector

class Update_Server(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Envia uma dm para o dono do servidor quando um canal de texto ou voz é deletado.
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        MySQLConnector.greetings_channel_Search(MySQLConnector,)

async def setup(bot):
    await bot.add_cog(Update_Server(bot))
