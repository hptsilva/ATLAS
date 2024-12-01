import discord
from decouple import config

COLOR = int(config('COLOR'))

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
                         icon_url='https://cdn.discordapp.com/attachments/1302022249389363210/1302022403605659720/warning.png?ex=6741a11b&is=67404f9b&hm=b938c823f51bb59036433b7549074f0d6667a5f580d28e9bae169707427f5d0e&',
        )
        client = interaction.client
        channel_id = interaction.channel_id
        message = client.get_channel(channel_id)
        await message.send(embed=embed)
        await interaction.response.send_message('Postagem enviada.', ephemeral=True)
