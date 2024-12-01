import discord
import re
import timezone
from comandos.modal.evento.buttons import Menu_Enquete
from decouple import config

COLOR = int(config('COLOR'))

class Modal_Enquete(discord.ui.Modal, title='Criar Evento'):

    titulo = discord.ui.TextInput(label='Título:',
                                  placeholder='Título do Evento',
                                  required=True,
                                  min_length=1,
                                  max_length=256,
                                  style=discord.TextStyle.short)
    fuso_horario = discord.ui.TextInput(label='Zona de Tempo:',
                                  placeholder='Use o comando /timezone e veja as opções',
                                  required=True,
                                  min_length=1,
                                  max_length=1,
                                  style=discord.TextStyle.short)
    data_horario = discord.ui.TextInput(label='Horário e Data (HH:MM AAAA-MM-DD):',
                                  placeholder='Horário e Data do Evento',
                                  required=True,
                                  min_length=16,
                                  max_length=16,
                                  style=discord.TextStyle.short)
    descricao = discord.ui.TextInput(label='Descrição (Opcional):',
                                     placeholder='Descrição do Evento',
                                     required=False,
                                     style=discord.TextStyle.paragraph)
    url_imagem = discord.ui.TextInput(label='URL da imagem (Opcional):',
                                      placeholder='URL da imagem para o Evento',
                                      required=False,
                                      style=discord.TextStyle.short)

    async def on_submit(self, interaction: discord.Interaction):

        titulo = self.titulo.value
        data_horario = self.data_horario.value
        fuso_horario = self.fuso_horario.value
        url_da_imagem = self.url_imagem.value
        descricao = self.descricao.value
        padra_data = r'^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]) (202[0-9])-(0[0-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[0-1])$'
        corresponde_data = re.match(padra_data, data_horario)
        if corresponde_data:
            try:
                Fuso_Horario = timezone.Fuso_Horario()
                horario = data_horario[:5]
                data = data_horario[6:]
                start_time, end_time, now_time = await Fuso_Horario.fuso_horario(int(fuso_horario), data, horario)
                segundos_depois = start_time.timestamp()
                segundos_agora = now_time.timestamp()
                if (segundos_depois - segundos_agora) > 0:
                    pass
                else:
                    await interaction.response.send_message('Não é possível criar um evento com data e hora no passado.', ephemeral=True)
                    return
            except Exception:
                await interaction.response.send_message(f'Zona de tempo inválida.', ephemeral=True)
                return
            if descricao == '':
                embed = discord.Embed(title=f'{titulo}',
                                      color=COLOR)
            else:
                embed = discord.Embed(title=f'**{titulo}**',
                                      description=f'{descricao}',
                                      color=COLOR)
            embed.timestamp = start_time
            embed.add_field(name='Horário:', value=f':alarm_clock: <t:{int(start_time.timestamp())}:f>\n:hourglass: <t:{int(start_time.timestamp())}:R>', inline=False)
            embed.add_field(name='🟩 Sim:', value=f'', inline=True)
            embed.add_field(name='🟥 Não:', value=f'', inline=True)
            embed.add_field(name='🟦 Talvez:', value=f'', inline=True)
            if url_da_imagem != '':
                try:
                    image_url = url_da_imagem
                    embed.set_image(url=image_url)
                except:
                    await interaction.response.send_message('Não foi possível inserir a imagem. Tente novamente.', ephemeral=True)
                    return
            embed.set_footer(text=f'Evento criado por {interaction.user.display_name}',
                             icon_url='https://cdn.discordapp.com/attachments/1302022249389363210/1302022403605659720/warning.png?ex=6741a11b&is=67404f9b&hm=b938c823f51bb59036433b7549074f0d6667a5f580d28e9bae169707427f5d0e&',
            )
            view = Menu_Enquete()
            try:
                await interaction.response.send_message(content='@everyone',embed=embed, view=view, allowed_mentions = discord.AllowedMentions(everyone=True, users=True))
            except:
                await interaction.response.send_message('Não foi possível criar o evento.', ephemeral=True)
        else:
            await interaction.response.send_message('A data não está no formato correto (hh:mm aaaa-mm-dd) ou não é válida.', ephemeral=True)
