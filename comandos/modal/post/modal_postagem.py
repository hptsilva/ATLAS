import discord
from decouple import config

COLOR = int(config('COLOR'))
ICON_URL = config('ICON_URL')

class Modal_Postagem(discord.ui.Modal, title='Criar Postagem'):

    titulo = discord.ui.TextInput(label='Título:',
                                  placeholder='Título da Postagem',
                                  required=True,
                                  min_length=1,
                                  max_length=256,
                                  style=discord.TextStyle.short)
    descricao = discord.ui.TextInput(label='Texto:',
                                     placeholder='Texto da Postagem',
                                     required=True,
                                     style=discord.TextStyle.paragraph)


    async def on_submit(self, interaction: discord.Interaction):

        titulo = self.titulo.value
        descricao = self.descricao.value
        embed = discord.Embed(title=f"{titulo}",
                              description=f'>>> {descricao}',
                              color=COLOR,
        )
        embed.set_footer(text=f'Post feito por {interaction.user.display_name}',
                         icon_url=ICON_URL,
        )
        client = interaction.client
        channel_id = interaction.channel_id
        message = client.get_channel(channel_id)
        await message.send(embed=embed)
        await interaction.response.send_message('Postagem enviada.', ephemeral=True)
