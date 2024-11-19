import discord
from decouple import config

COLOR = int(config('COLOR'))
BOT_NAME = config('BOT_NAME')
ICON_URL = config('ICON_URL')

class Modal_Aviso(discord.ui.Modal, title='Criar Aviso'):

    titulo = discord.ui.TextInput(label='Título:',
                                  placeholder='Título do Aviso',
                                  required=True,
                                  min_length=1,
                                  max_length=256,
                                  style=discord.TextStyle.short)
    descricao = discord.ui.TextInput(label='Texto:',
                                     placeholder='Texto do Aviso',
                                     required=True,
                                     style=discord.TextStyle.paragraph)


    async def on_submit(self, interaction: discord.Interaction):

        titulo = self.titulo.value
        descricao = self.descricao.value
        embed = discord.Embed(title=f"{titulo}",
                              description=f'>>> {descricao}',
                              color=COLOR,
        )
        embed.set_footer(text=f"{BOT_NAME}",
                       icon_url=ICON_URL
        )
        client = interaction.client
        channel_id = interaction.channel_id
        message = client.get_channel(channel_id)
        await message.send(content='@everyone', embed=embed,  allowed_mentions = discord.AllowedMentions(everyone=True))
        await interaction.response.send_message('Aviso enviado.', ephemeral=True)
