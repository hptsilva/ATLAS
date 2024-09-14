import discord
import re
import timezone
from decouple import config

COLOR = int(config('COLOR'))

class Modal_Enquete_Editar(discord.ui.Modal, title = 'Editar Evento'):

    titulo = discord.ui.TextInput(label='Título',
                                  placeholder='Título do Evento',
                                  required=False,
                                  max_length=256,
                                  style=discord.TextStyle.short)
    fuso_horario = discord.ui.TextInput(label='Zona de Tempo',
                                  placeholder='Use o comando /timezone para ver as opções',
                                  required=False,
                                  min_length=1,
                                  max_length=1,
                                  style=discord.TextStyle.short)
    data_horario = discord.ui.TextInput(label='Horário e Data (HH:MM AAAA-MM-DD)',
                                  placeholder='Horário e Data do Evento',
                                  required=False,
                                  min_length=16,
                                  max_length=16,
                                  style=discord.TextStyle.short)
    descricao = discord.ui.TextInput(label='Descrição',
                                     placeholder='Descrição do Evento. Digite {apagar} para limpar o campo.',
                                     required=False, style=discord.TextStyle.paragraph)
    url_imagem = discord.ui.TextInput(label='URL da imagem',
                                      placeholder='URL da imagem do Evento.',
                                      required=False, style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):

        message = interaction.message
        if self.titulo.value == '' and self.descricao.value == '' and self.url_imagem.value == '' and self.fuso_horario.value == '' and self.data_horario.value == '':
            await interaction.response.send_message('Nenhum dado foi inserido no formulário.', ephemeral=True)
            return
        embed_antigo = message.embeds[0]
        campo_sim = embed_antigo.fields[1]
        value_sim = campo_sim.value
        campo_nao = embed_antigo.fields[2]
        value_nao = campo_nao.value
        campo_talvez = embed_antigo.fields[3]
        value_talvez = campo_talvez.value
        url_image = embed_antigo.image.url
        title = embed_antigo.title if self.titulo.value == '' else self.titulo
        description = embed_antigo.description if self.descricao.value == '' else self.descricao
        if self.descricao.value == '{apagar}':
            description = ''
        url_image = embed_antigo.image.url if self.url_imagem.value == '' else self.url_imagem
        if description is None:
            embed = discord.Embed(title=f'{title}',
                                  color=COLOR)
        else:
            embed = discord.Embed(title=f'{title}',
                                  description=f'{description}',
                                  color=COLOR)
        if (self.fuso_horario.value != '' and self.data_horario.value != ''):
            padra_data = r'^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]) (202[0-9])-(0[0-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$'
            corresponde_data = re.match(padra_data, self.data_horario.value)
            if corresponde_data:
                Fuso_Horario = timezone.Fuso_Horario()
                horario = self.data_horario.value[:5]
                data = self.data_horario.value[6:]
                try:
                    start_time, end_time, now_time = await Fuso_Horario.fuso_horario(int(self.fuso_horario.value), data, horario)
                except Exception:
                    await interaction.response.send_message(f'Zona de tempo inválida.', ephemeral=True)
                    return
                segundos_depois = start_time.timestamp()
                segundos_agora = now_time.timestamp()
                if (segundos_depois - segundos_agora) < 0:
                    await interaction.response.send_message('Não é possível criar um evento com data e hora no passado.', ephemeral=True)
                    return
                embed.timestamp = start_time    
            else:
                await interaction.response.send_message('A data não está no formato correto (hh:mm aaaa-mm-dd) ou não é válida.', ephemeral=True)
                return
        elif (self.fuso_horario.value != '' and self.data_horario.value == ''):
            await interaction.response.send_message('Preencha também o campo Horário e Data.', ephemeral=True)
            return
        elif (self.fuso_horario.value == '' and self.data_horario.value != ''):
            await interaction.response.send_message('Preencha também o campo Zona de Tempo.', ephemeral=True)
            return
        else:
            embed.timestamp = embed_antigo.timestamp
        embed.add_field(name='Horário:', value=f'<t:{int(embed.timestamp.timestamp())}:f>', inline=False)
        embed.add_field(name='✅ Sim:', value=f'{value_sim}', inline=True)
        embed.add_field(name='⛔ Não:', value=f'{value_nao}', inline=True)
        embed.add_field(name='❔ Talvez:', value=f'{value_talvez}', inline=True)
        if url_image != '' and url_image != None and self.url_imagem.value != '{apagar}':
            embed.set_image(url=f'{url_image}')
        footer = embed_antigo.footer.text
        embed.set_footer(text=f'{footer}')
        await interaction.response.edit_message(embed=embed)
