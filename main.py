# Documentação https://discordpy.readthedocs.io/en/stable/
# Repositório Discord.py https://github.com/Rapptz/discord.py/tree/v2.3.2

import discord
import asyncio
from decouple import config
from discord.ext import commands
from discord import app_commands
from comandos.modal.evento.modal_enquete import Modal_Enquete
from comandos.modal.post.modal_postagem import Modal_Postagem
from comandos.modal.aviso.modal_aviso import Modal_Aviso

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
@bot.tree.command(name='evento', description='Crie um evento no servidor.')
@commands.guild_only()
async def enquete(interaction: discord.Interaction):

     await interaction.response.send_modal(Modal_Enquete())

# Carrega o comando para criação de postagens. Apenas pode ser utilizado dentro de um servidor
@bot.tree.command(name='postar', description='Crie uma postagem.')
@commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def postagem(interaction: discord.Interaction):

    await interaction.response.send_modal(Modal_Postagem())

# Carrega o comando para criação de mensagens de aviso. Apenas pode ser utilizado dentro de um servidor
@bot.tree.command(name='avisar', description='Crie uma mensagem de aviso.')
@commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def aviso(interaction: discord.Interaction):

    await interaction.response.send_modal(Modal_Aviso())

# Executa uma instância do bot
bot.run(config('TOKEN'))
