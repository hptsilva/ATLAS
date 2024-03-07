from decouple import config
from discord.ext import commands
from comandos.butoes.modal_enquete import Modal_Enquete

TOKEN = config('TOKEN')

bot = commands.Bot(command_prefix='$a', intents=discord.Intents.all())

async def load_extensions(self):

     await self.load_extension('comandos.interacao.interaction')
     await self.load_extension('comandos.moderacao.moderation')
     await self.load_extension('comandos.eventos.events')
     await self.load_extension('comandos.eventos.exception_events')
     await self.load_extension('comandos.exclusivo.comandos_exclusivos')

asyncio.run(load_extensions(bot))

@bot.tree.command(name='evento', description='Crie um evento no servidor.')
@commands.guild_only()
async def enquete(interaction: discord.Interaction):

     await interaction.response.send_modal(Modal_Enquete())

bot.run(TOKEN) # Executa uma instância do bot
