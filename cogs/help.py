import discord
from discord.ui import Select, View
from discord import app_commands
from discord.ext import commands
from discord import SelectOption
import typing
# from nebulafunctions.help.helpoptions import helpoptions
from nebulafunctions.help.fhelp import *

global timeoutcheck
timeoutcheck = {}

class helpSelect(Select):
    def __init__(self) -> None:
        super().__init__(
                placeholder="Choose a category", disabled=False, options=[
                SelectOption(
                    label='Math',
                    value='Math',
                    description='Math Commands',
                    emoji="📏"
                    ),
                SelectOption(
                    label='Fun', 
                    value='Fun',
                    description='Fun Commands',
                    emoji="🎢"
                    ),
                SelectOption(
                    label='Information', 
                    value='Information',
                    description='Information Commands',
                    emoji="ℹ️"
                    ),
                SelectOption(
                    label='Moderation', 
                    value='Moderation',
                    description='Moderation Commands',
                    emoji="⚖"
                    ),
                # SelectOption(
                #     label='Music', 
                #     value='Music',
                #     description='Music Commands',
                #     emoji="🎵"
                #   ),
                SelectOption(
                    label='NebCoins', 
                    value='Nebcoins',
                    description='The Game',
                    emoji="🌱"
                    )
                # SelectOption(
                #     label='Setup', 
                #     value='Setup',
                #     description='Setup Commands',
                #     emoji="⚙️"
                #     )
            ]
        )

    async def callback(self, ctx):
        self._view.stop()
        category = self.values[0]
        command = '`/add`\n`/subtract`\n`/multiply`\n`/divide`\n`/squareroot`\n`/cuberoot`\n`/speed`\n`/distance`\n`/time`\n`/circumference`'
        math = discord.Embed(title='**Math Commands**',description=str(command),colour = ctx.user.color)
        command = '`/tictactoe`\n`/diceroll`\n`/tweet`\n`/wanted`\n`/rockpaperscissors`\n`/prison`\n`/quiz`\n`/quizstats`\n`/quizleaderboard`\n`/connect4`'
        fun = discord.Embed(title='**Fun Commands**',description=str(command),colour = ctx.user.color)
        command = '`/wikipedia`\n`/weather`\n`/serverinfo`\n`/userinfo`\n`/suggest`\n`/invite`\n`/changelog`\n`/fact`\n`/question`\n`/stats`'
        information = discord.Embed(title='**Information Commands**',description=str(command),colour = ctx.user.color)
        command = '`/kick`\n`/ban`\n`/unban`\n`/poll`\n`/announce`\n`/warn`\n`/warnings`\n`/delwarn`\n`/giveaway`\n`/lock`\n`/unlock`\n`/slowmode`\n`/tempban`\n`/create`\n`/delete`'
        moderation = discord.Embed(title='**Moderation Commands**',description=str(command),colour = ctx.user.color)
        # command = '**Join:**\nAliases: j\nDescription: Joins the Voice Channel\nUsage: `.join`\n\n**Disconnect:**\nAliases: l\nDescription: Leaves the Voice Channel\nUsage: `.disconnect`\n\n**Play:**\nAliases: pl\nDescription: plays the song\nUsage: `.play song name`\n\n**Pause:**\nAliases: None\nDescription: Pauses the song\nUsage: `.pause`\n\n**Resume:**\nAliases: None\nDescription: Resumes the song\nUsage: `.resume`\n\n**Stop:**\nAliases: None\nDescription: Stops the song\nUsage: `.stop`\n\n**NowPlaying:**\nAliases: np\nDescription: Shows the song now playing\nUsage: `.nowplaying`\n\n**Remove:**\nAliases: None\nDescription: Removes the song from queue\nUsage: `.remove 1`\n\n**Loop:**\nAliases: None\nDescription: Loops the song\nUsage: `.loop`\n\n**Queue:**\nAliases: None\nDescription: Shows the queue\nUsage: `.queue`\n\n**Skip:**\nAliases: None\nDescription: Skips the Song\nUsage: `.skip`\n\n**Playlist Add:**\nAliases: pla\nDescription: adds the song to your playlist\nUsage: `.playlistadd song name`\n\n**Playlist Remove:**\nAliases: plr\nDescription: removes the song from your playlist\nUsage: `.playlistremove song name`\n\n**My Playlist:**\nAliases: mp\nDescription: shows your playlist\nUsage: `.myplaylist`\n\n**Playlist:**\nAliases: None\nDescription: Plays your playlist, use .join before this\nUsage: `.playlist`'
        # music = discord.Embed(title='**Music Commands**',description=str(command),colour = ctx.author.color)
        command = '`/start`\n`/farm`\n`/balance`\n`/plant`\n`/inventory`\n`/sell`\n`/market`\n`/work`\n`/leaderboard`\n`/beg`\n`/journey`\n`/pets`\n`/mypets`'
        nebcoins = discord.Embed(title='**NebCoins**',description=str(command),colour = ctx.user.color)
        command = '`/setmemberrole`\n`/removememberrole`\n`/setupdatechannel`'
        setup = discord.Embed(title='**Setup Commands**',description=str(command),colour = ctx.user.color)
        if category == 'Math':
            await ctx.message.edit(embed=math, view=None)
        elif category == 'Fun':
            await ctx.message.edit(embed=fun, view=None)
        elif category == 'Information':
            await ctx.message.edit(embed=information, view=None)
        elif category == 'Moderation':
            await ctx.message.edit(embed=moderation, view=None)
        # elif category == 'Music':
        #     await ctx.message.edit(embed=music)
        elif category == 'Nebcoins':
            await ctx.message.edit(embed=nebcoins, view=None)
        elif category == 'Setup':
            await ctx.message.edit(embed=setup, view=None)

class helpView(View):
    def __init__(self, timeout=60):
        super().__init__(timeout=timeout)
        self.add_item(helpSelect())


    async def on_timeout(self):
        await endf(self.id)

class help(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @app_commands.command(name='help', description="View all of Nebula's features")
    async def help(self, ctx, command: str=None):
        if command != None:
            embed = returnembed(command)
            await ctx.response.send_message(embed=embed)
            return

        startv = helpView()

        start = discord.Embed(title='Help', description='Choose a category\n\n**Quick Links**\n**[Invite](https://discord.com/api/oauth2/authorize?client_id=953533453100527626&permissions=1247621410038&scope=bot) . [Support](https://discord.gg/CxtY6rTnr4) . [top.gg](https://top.gg/bot/953533453100527626) . [Website](https://bot-nebula.web.app/)\n[YouTube](https://www.youtube.com/channel/UC3mXj3Vr3p0l7ARHADtSvVQ) . [Changelog](http://bot-nebula.web.app/changelog/pg1) . [Suggest](https://hi7rxb1s0wz.typeform.com/to/ftHD17Mz)**', color=discord.Color.gold())
        start.set_footer(text='Use /help [COMMAND NAME] to get more information on a command')
        await ctx.response.send_message(embed=start, view=startv)
        timeoutcheck[startv.id] = ctx
        global endf
        async def endf(id):
            select = Select(placeholder="No category chosen", disabled=True, options=[
                SelectOption(
                    label='Math',
                    value='Math',
                    description='Math Commands',
                    emoji="📏"
                    ),
                SelectOption(
                    label='Fun', 
                    value='Fun',
                    description='Fun Commands',
                    emoji="🎢"
                    ),
                SelectOption(
                    label='Information', 
                    value='Information',
                    description='Information Commands',
                    emoji="ℹ️"
                    ),
                SelectOption(
                    label='Moderation', 
                    value='Moderation',
                    description='Moderation Commands',
                    emoji="⚖"
                    ),
                # SelectOption(
                #     label='Music', 
                #     value='Music',
                #     description='Music Commands',
                #     emoji="🎵"
                #   ),
                SelectOption(
                    label='NebCoins', 
                    value='Nebcoins',
                    description='The Game',
                    emoji="🌱"
                    ),
                SelectOption(
                    label='Setup', 
                    value='Setup',
                    description='Setup Commands',
                    emoji="⚙️"
                    )
            ])
            endv = View()
            endv.add_item(select)

            end = discord.Embed(title='Help', description='No category chosen\n\n**Quick Links**\n**[Invite](https://discord.com/api/oauth2/authorize?client_id=953533453100527626&permissions=1247621410038&scope=bot) . [Support](https://discord.gg/JqaJauWB9f) . [top.gg](https://top.gg/bot/953533453100527626) . [DiscordBotList](https://discordbotlist.com/bots/nebula-3788) . [Discord Bots](https://discord.bots.gg/bots/953533453100527626) . [Website](https://bot-nebula.web.app/)\n[YouTube](https://www.youtube.com/channel/UC3mXj3Vr3p0l7ARHADtSvVQ) . [Changelog](http://bot-nebula.web.app/changelog/pg1) . [Suggest](https://forms.gle/GSC7VNnGRyCikw8b6)**', color=discord.Color.gold())
            end.set_footer(text='Use /help [COMMAND NAME] to get more information on a command')
            await timeoutcheck[id].edit_original_response(embed=end, view=endv)
            timeoutcheck.pop(id)

async def setup(bot:commands.Bot) -> None:
        await bot.add_cog(help(bot), guilds = []) #leave empty for all servers