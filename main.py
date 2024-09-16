# Documentação https://discordpy.readthedocs.io/en/stable/
# Repositório Discord.py https://github.com/Rapptz/discord.py/tree/v2.3.2

import discord
import asyncio
from decouple import config
from discord.ext import commands
from comandos.modal.modal_enquete import Modal_Enquete

flags = discord.MemberCacheFlags.all()
bot = commands.AutoShardedBot(command_prefix='$i', intents=discord.Intents.all(), shard_count=1, member_cache_flags=flags)

# Carregar comandos
async def load_extensions(self):

     await self.load_extension('comandos.interacao.interaction')
     await self.load_extension('comandos.moderacao.moderation')
     await self.load_extension('comandos.eventos.events')
     await self.load_extension('comandos.eventos.exceptions')
     await self.load_extension('comandos.exclusivo.owner_commands')

asyncio.run(load_extensions(bot))

# Carrega o comando para criação de evento. Apenas pode ser utilizado dentro de um servidor.
@bot.tree.command(name='evento', description='Evento - Crie um evento no servidor.')
@commands.guild_only()
async def enquete(interaction: discord.Interaction):

     await interaction.response.send_modal(Modal_Enquete())

bot.run(config('TOKEN')) # Executa uma instância do bot
