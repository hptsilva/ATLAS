import discord

COLOR_ATLAS = 0x1414b8

class Modal_Enquete_Editar(discord.ui.Modal, title = 'Editar Evento'):

    titulo = discord.ui.TextInput(label='Título', 
                                  placeholder='Título do Evento',
                                  required=False,
                                  max_length=256,
                                  style=discord.TextStyle.short)
    descricao = discord.ui.TextInput(label='Descrição (Opcional)', 
                                     placeholder='Descrição do Evento. Digite {apagar} para limpar o campo.',
                                     required=False, 
                                     style=discord.TextStyle.paragraph)
    url_imagem = discord.ui.TextInput(label='URL da imagem',
                                      placeholder='URL da imagem para o Evento',
                                      required=False,
                                      style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):

        message = interaction.message
        if self.titulo.value == '' and self.descricao.value == '' and self.url_imagem.value == '':
            await interaction.response.send_message('Nenhuma alteracao foi inserida.', ephemeral=True)
            return
        embed_antigo = message.embeds[0]
        campo_sim = embed_antigo.fields[2]
        value_sim = campo_sim.value
        campo_nao = embed_antigo.fields[3]
        value_nao = campo_nao.value
        campo_talvez = embed_antigo.fields[4]
        value_talvez = campo_talvez.value
        url_image = embed_antigo.image.url
        title = embed_antigo.title if self.titulo.value == '' else self.titulo
        description = embed_antigo.description if self.descricao.value == '' else self.descricao
        if self.descricao.value == '{apagar}':
            description = ''
        url_image = embed_antigo.image.url if self.url_imagem.value == '' else self.url_imagem
        if description is None:
            embed = discord.Embed(title=f'{title}',
                                  color=COLOR_ATLAS)
        else:
            embed = discord.Embed(title=f'{title}',
                                  description=f'{description}',
                                  color=COLOR_ATLAS)
        embed.add_field(name='Opções:', value='| ✅ - Sim | ⛔ - Não | ❔ - Talvez |', inline=False)
        embed.timestamp = embed_antigo.timestamp
        embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
        embed.add_field(name='✅ Nomes:', value=f'{value_sim}', inline=True)
        embed.add_field(name='⛔ Nomes:', value=f'{value_nao}', inline=True)
        embed.add_field(name='❔ Nomes:', value=f'{value_talvez}', inline=True)
        embed.set_image(url=f'{url_image}')
        footer = embed_antigo.footer.text
        embed.set_footer(text=f'{footer}')
        try:
            await interaction.response.edit_message(embed=embed)
        except:
            await interaction.response.send_message('Não foi possível alterar o evento.', ephemeral=True)
