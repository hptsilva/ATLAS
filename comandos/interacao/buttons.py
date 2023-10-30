import discord
from discord.ext import commands

class Buttons(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='button', description='Um botão')
    async def button(self, ctx):
        teste = discord.ui.Select(placeholder='Oi', 
                                  min_values=1, 
                                  max_values=2,
                                  )
        await ctx.send()

async def setup(bot):
    await bot.add_cog(Buttons(bot))