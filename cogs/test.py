import discord
from discord import app_commands
from discord.ext import commands
import typing

global testvar
testvar = [app_commands.Choice(name="Option 1", value="1"),
        app_commands.Choice(name="Option 2", value="2")]


class test(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        
    @app_commands.command(name='test', description='test')
    @app_commands.choices(option=testvar)
    async def test(self, ctx, option: typing.Optional[app_commands.Choice[str]]):
        await ctx.response.send_message('Worked')
        
async def setup(bot:commands.Bot) -> None:
        await bot.add_cog(test(bot), guilds = [discord.Object(id = 879950029564031006)]) #leave empty for all servers