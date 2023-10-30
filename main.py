# Documentação https://discordpy.readthedocs.io/en/stable/
# Repositório Discord.py https://github.com/Rapptz/discord.py/tree/v2.3.2

import discord
import asyncio
from decouple import config
from discord.ext import commands

TOKEN = config('TOKEN')

bot = commands.Bot(command_prefix='$i', intents=discord.Intents.all())

# Carregar comandos
async def load_extensions(self):

     await self.load_extension('comandos.interacao.interaction')
     await self.load_extension('comandos.moderacao.moderation')
     await self.load_extension('comandos.eventos.events')
     await self.load_extension('comandos.eventos.exception_events')
     await self.load_extension('comandos.exclusivo.exclusive')

asyncio.run(load_extensions(bot))

bot.run(TOKEN) # Executa uma instância do bot
