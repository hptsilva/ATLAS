from discord.ext import commands
from discord import RateLimited, NotFound
from discord.ext.commands.errors import MissingPermissions, CommandNotFound, MissingRequiredArgument, CommandOnCooldown, NotOwner, BotMissingPermissions, CheckAnyFailure, MissingPermissions, NoPrivateMessage, PrivateMessageOnly, CommandInvokeError, UserInputError, MaxConcurrencyReached

class Exception_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    error_messages_ext= {
        MissingPermissions: '**Você não possui permissão para utilizar esse comando.**',
        CommandNotFound: '**Este comando não existe.**',
        MissingRequiredArgument: '**Envie todos os argumentos necessários.**',
        CommandOnCooldown: '**O comando está em cooldown.**',
        NotOwner: '**Você não é dono da aplicação.**',
        BotMissingPermissions: '**O bot não tem permissão para executar esse comando.**',
        CheckAnyFailure: '**Você não possui permissão para utilizar esse comando.**',
        NotFound: '**Erro 404. Aguarde alguns segundos. Se o problema persistir informe o dono da aplicação.**',
        RateLimited: '**Aguarde alguns segundos para requisição.**',
        NoPrivateMessage: '**Comando usado apenas em mensagens privadas.**',
        PrivateMessageOnly: '**Comando usado apenas em mensagens privadas.**',
        CommandInvokeError: '**Erro interno**',
        UserInputError: '**Houve algum erro relacionado a entrada de dados**',
        MaxConcurrencyReached: '**Limite de invocações simultâneas atingida**'
    }

    # Evento ativado quando ocorre uma exceção.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        error_type = type(error)
        if error_type in self.error_messages_ext:
            await ctx.send(self.error_messages_ext[error_type], ephemeral=True)
        else:
            await ctx.send('**Erro interno.**', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Exception_events(bot))
