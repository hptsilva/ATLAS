from datetime import datetime
import mysql_connection
from discord.ext import commands
from discord import RateLimited, NotFound
from discord.errors import NotFound
from discord.ext.commands.errors import MissingPermissions, CommandNotFound, MissingRequiredArgument, CommandOnCooldown, NotOwner, BotMissingPermissions, CheckAnyFailure, MissingPermissions, NoPrivateMessage, PrivateMessageOnly

class Exception_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    error_messages_ext= {
        MissingPermissions: '**Você não possui permissão para utilizar esse comando.**',
        CommandNotFound: '**Este comando não existe.**',
        MissingRequiredArgument: '**Envie todos os argumentos necessários.**',
        CommandOnCooldown: '**O comando está em modo de espera.**',
        NotOwner: '**Interação restrita.**',
        BotMissingPermissions: '**O bot não tem as permissões necessárias para executar o comando.**',
        CheckAnyFailure: '**Você não possui permissão para utilizar esse comando.**',
        RateLimited: '**O comando está em modo de espera.**',
        NoPrivateMessage: '**Comando usado apenas em mensagens privadas.**',
        PrivateMessageOnly: '**Comando usado apenas em mensagens privadas.**',
        NotFound: "**Erro. Tente novamente...**",
    }

    # Evento ativado quando ocorre uma exceção.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        error_type = type(error)
        if error_type in self.error_messages_ext:
            await ctx.send(self.error_messages_ext[error_type], ephemeral=True)
        else:
            await ctx.send('**Erro.**', ephemeral=True)
        guild = ctx.guild
        command = ctx.command
        author = ctx.author
        guild_id = guild.id if command else None
        command_name = command.name if command else None
        author_id = author.id if author else None
        MySQLConnector = mysql_connection.MySQLConnector()
        cnx_admin, cursor_admin = await MySQLConnector.conectar_admin()
        inserir = 'INSERT INTO exceptions VALUES(%s, %s, %s, %s, %s)'
        cursor_admin.execute(inserir, (str(error), str(guild_id), str(author_id), str(command), datetime.now(), ))
        cnx_admin.commit()
        await MySQLConnector.desconectar_admin(cnx_admin)

async def setup(bot):
    await bot.add_cog(Exception_events(bot))
