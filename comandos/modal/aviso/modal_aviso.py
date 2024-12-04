import discord
from decouple import config

COLOR = int(config('COLOR'))
BOT_NAME = config('BOT_NAME')

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
    url_imagem = discord.ui.TextInput(label='URL da imagem (Opcional):',
                                      placeholder='Exemplo: https://subdominio.dominio/uri',
                                      required=False,
                                      style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):

        if self.titulo.value == '' or self.descricao.value == '':
            await interaction.response.send_message('**Preencha todos os campos obrigatórios.**', ephemeral=True)
            return
        titulo = self.titulo.value
        descricao = self.descricao.value
        url_da_imagem = self.url_imagem.value
        embed = discord.Embed(title=f"{titulo}",
                              description=f'>>> {descricao}',
                              color=COLOR,
        )
        if url_da_imagem != '':
            embed.set_image(url=url_da_imagem)
        embed.set_footer(text=f"{BOT_NAME}",
                       icon_url="https://cdn.discordapp.com/attachments/1302022249389363210/1302022403605659720/warning.png?ex=6741a11b&is=67404f9b&hm=b938c823f51bb59036433b7549074f0d6667a5f580d28e9bae169707427f5d0e&"
        )
        client = interaction.client
        channel_id = interaction.channel_id
        message = client.get_channel(channel_id)
        try:
            await message.send(content='@everyone', embed=embed,  allowed_mentions = discord.AllowedMentions(everyone=True))
        except:
            await interaction.response.send_message('**Não foi possível criar o aviso**.', ephemeral=True)
            return
        await interaction.response.send_message('Aviso enviado.', ephemeral=True)
