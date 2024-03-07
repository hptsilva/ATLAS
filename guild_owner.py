from discord.ext import commands

class GuildOwner:

     def is_guild_owner():
          def predicate(ctx):
               return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
          return commands.check(predicate) 

