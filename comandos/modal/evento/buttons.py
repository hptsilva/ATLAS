import discord
import comandos.modal.evento.reacoes as reacoes
from comandos.modal.evento.modal_enquete_editar import Modal_Enquete_Editar
from datetime import datetime
import mysql_connection

class Menu_Enquete(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.timeout = None

    @discord.ui.button(label='', style=discord.ButtonStyle.green, emoji='▫️', row=2)
    async def confirmacao1(self, interaction: discord.Interaction, button: discord.ui.Button):

        Reacoes_Enquete = reacoes.Reacoes_Enquete()
        message = interaction.message
        user = interaction.user
        embed = await Reacoes_Enquete.reacoes(message, user, 1)
        await interaction.response.edit_message(content='@everyone', embed=embed, allowed_mentions = discord.AllowedMentions(everyone=True, users=True))

    @discord.ui.button(label='', style=discord.ButtonStyle.red, emoji='▫️', row=2)
    async def confirmacao2(self, interaction: discord.Interaction, button: discord.ui.Button):

        Reacoes_Enquete = reacoes.Reacoes_Enquete()
        message = interaction.message
        user = interaction.user
        embed = await Reacoes_Enquete.reacoes(message, user, 2)
        await interaction.response.edit_message(content='@everyone', embed=embed, allowed_mentions = discord.AllowedMentions(everyone=True, users=True))

    @discord.ui.button(label='', style=discord.ButtonStyle.blurple, emoji='▫️', row=2)
    async def confirmacao3(self, interaction: discord.Interaction, button: discord.ui.Button):

        Reacoes_Enquete = reacoes.Reacoes_Enquete()
        message = interaction.message
        user = interaction.user
        embed = await Reacoes_Enquete.reacoes(message, user, 3)
        await interaction.response.edit_message(content='@everyone', embed=embed, allowed_mentions = discord.AllowedMentions(everyone=True, users=True))

    @discord.ui.button(label='EDITAR', style=discord.ButtonStyle.gray, row=1)
    async def editar(self, interaction: discord.Interaction, button: discord.ui.Button):

        message = interaction.message
        author = message.interaction_metadata.user
        if interaction.user == author:
            await interaction.response.send_modal(Modal_Enquete_Editar())
        else:
            await interaction.response.send_message('Interação não permitida.', ephemeral=True)

    @discord.ui.button(label='CANCELAR', style=discord.ButtonStyle.gray, row=1)
    async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):

        message = interaction.message
        author = message.interaction_metadata.user
        if interaction.user == author:
            Reacoes_Enquete = reacoes.Reacoes_Enquete()
            message = interaction.message
            embed = await Reacoes_Enquete.reacoes(message, author, 4)
            message = interaction.message
            id_message = message.id
            MySQLConnector = mysql_connection.MySQLConnector()
            await MySQLConnector.excluir_evento(id_message)
            await MySQLConnector.excluir_view(id_message)
            await interaction.response.edit_message(content='@everyone', embed=embed, view=None, allowed_mentions = discord.AllowedMentions(everyone=True, users=True),  delete_after=60)
            self.stop()
        else:
            await interaction.response.send_message('Interação não permitida.', ephemeral=True)

    @discord.ui.button(label='CONCLUIR', style=discord.ButtonStyle.gray, row=1)
    async def concluir(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        author = message.interaction_metadata.user
        if interaction.user == author:
            Reacoes_Enquete = reacoes.Reacoes_Enquete()
            message = interaction.message
            embed = await Reacoes_Enquete.reacoes(message, author, 5)
            message = interaction.message
            id_message = message.id
            MySQLConnector = mysql_connection.MySQLConnector()
            await MySQLConnector.excluir_evento(id_message)
            await MySQLConnector.excluir_view(id_message)
            await interaction.response.edit_message(content='@everyone', embed=embed, view=None, allowed_mentions = discord.AllowedMentions(everyone=True, users=True), delete_after=600)
            self.stop()
        else:
            await interaction.response.send_message('Interação não permitida.', ephemeral=True)

    @discord.ui.button(label='NOTIFICAR', style=discord.ButtonStyle.red, row=1)
    async def notificar(self, interaction: discord.Interaction, button: discord.ui.Button):
        message = interaction.message
        author = message.interaction_metadata.user
        if interaction.user == author:
            message = interaction.message
            textChannel = message.channel
            guild = message.guild
            id_message = message.id
            id_textChannel = textChannel.id
            id_guild = guild.id
            MySQLConnector = mysql_connection.MySQLConnector()
            resultado = await MySQLConnector.pesquisar_evento(id_message)
            if resultado:
                if resultado[3] == 'NÃO':
                    await MySQLConnector.excluir_evento(id_message)
                    button.style = discord.ButtonStyle.red
                    await interaction.response.edit_message(view=self)
                else:
                    await interaction.response.send_message('Os membros já foram notificados.', ephemeral=True)
            else:
                embed = message.embeds[0]
                tempo_evento = embed.timestamp
                now_time = datetime.now()
                if (tempo_evento.timestamp()  - now_time.timestamp()) < 0:
                    await interaction.response.send_message('Interação não permitida.', ephemeral=True)
                    return
                await MySQLConnector.inserir_evento(id_message, id_guild, id_textChannel)
                button.style = discord.ButtonStyle.green
                await interaction.response.edit_message(view=self)
        else:
            await interaction.response.send_message('Interação não permitida.', ephemeral=True)
