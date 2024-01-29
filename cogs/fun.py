import discord
import asyncio
import random
from random import shuffle
import matplotlib.pyplot as plt
from discord import app_commands, SelectOption
from discord.ext import commands
from nebulafunctions.fun.ffun import *
from discord.ui import Button, View, Select
from datetime import datetime, timedelta


class fun(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.tictactoevar = {}
        self.singletictactoevar = {}
        self.connect4 = {}
        self.connect4mem = {}
        self.sconnect4 = {}
        self.sconnect4mem = {}
        
    @app_commands.command(name='tictactoe', description='Play a game of Tic Tac Toe')
    @app_commands.choices(gametype=[
            app_commands.Choice(name="Single Player", value="1"),
            app_commands.Choice(name="Multiplayer", value="2")
        ])
    async def tictactoe(self, ctx, gametype: app_commands.Choice[str]):
        if gametype.value == '1':
            embed = discord.Embed(title='Level', description='Please choose a difficulty level', color=discord.Color.gold())
            view = View()
            
            async def easy(interaction):
                global level
                level = 'easy'
            async def difficult(interaction):
                global level
                level = 'difficult'
            
            easybutton = Button(label='Easy', style=discord.ButtonStyle.green)
            difficultbutton = Button(label='Difficult', style=discord.ButtonStyle.red)
            
            easybutton.callback = easy
            difficultbutton.callback = difficult
            
            view.add_item(easybutton)
            view.add_item(difficultbutton)
            await ctx.response.send_message(embed=embed, view=view)
            
            def levelcheck(event):
                if event.type == discord.InteractionType.component:
                    return True

            try:
                event = await self.bot.wait_for('interaction', check=levelcheck, timeout=20)
                await event.response.defer()
                embed = discord.Embed(title='Level', description=f'Difficulty level has been set to **{level.capitalize()}**', color=discord.Color.gold())
                view = View()
                easybutton = Button(label='Easy', style=discord.ButtonStyle.green, disabled=True)
                difficultbutton = Button(label='Difficult', style=discord.ButtonStyle.red, disabled=True)
                view.add_item(easybutton)
                view.add_item(difficultbutton)
                await ctx.edit_original_response(embed=embed, view=view)
            except asyncio.TimeoutError:
                embed = discord.Embed(title='Level', description=':frowning: You did not respond', color=discord.Color.blue())
                view = View()
                easybutton = Button(label='Easy', style=discord.ButtonStyle.green, disabled=True)
                difficultbutton = Button(label='Difficult', style=discord.ButtonStyle.red, disabled=True)
                view.add_item(easybutton)
                view.add_item(difficultbutton)
                await ctx.edit_original_response(embed=embed, view=view)
                return     
            
            player1icon = random.choice(['x', 'o'])
            player1 = ctx.user
            player2 = self.bot.user
            if player1icon == 'x':
                player2icon = 'o'
                currentplayer = player1
            else:
                player2icon = 'x'
                currentplayer = player2
                        
            self.singletictactoevar[ctx.guild.id] = {'player1':[ctx.user.id, player1icon], 'player2':[player2.id, player2icon], 'current':currentplayer, 'board':{"pos1":"n", "pos2":"n", "pos3":"n", "pos4":"n", "pos5":"n", "pos6":"n", "pos7":"n", "pos8":"n", "pos9":"n"}}
                    
            embed = discord.Embed(title='Tic Tac Toe', description=f'A game is starting!\n\n', color=discord.Color.purple())
            embed.add_field(name=f':{player1icon}:', value=player1.mention)
            embed.add_field(name=f':{player2icon}:', value=player2.mention)
            await ctx.channel.send(embed=embed)
            
            def checkresponse(message):
                playerc = self.singletictactoevar[ctx.guild.id]["current"]
                if message.author.id == playerc.id and message.channel.id == ctx.channel.id:
                    return True
            
            i = 0
            while True:
                i += 1
                # embed = discord.Embed(title=f'Turn {i}', description=f'{self.singletictactoevar[ctx.guild.id]["current"].mention}, Your turn please write a box no in chat', color=discord.Color.purple())
                # embed.set_image(url='https://i.imgur.com/nJPPRNa.gif')
                # prevmessage = await ctx.channel.send(embed=embed)
                result = genboard(ctx.guild.id, self.singletictactoevar)
                # gameboard = uploadimgur('assets/tictactoe/currentboard.png', f'{ctx.guild.id}{player1.id}{player2.id}')
                file = discord.File('assets/tictactoe/currentboard.png', filename='currentboard.png')
                gameboard = 'attachment://currentboard.png'
                if result != None:
                    if result == 'yes':
                        if self.singletictactoevar[ctx.guild.id]["current"].id == player1.id:
                            embed = discord.Embed(title='Game Over', description=f':tada: {player2.mention} :{self.singletictactoevar[ctx.guild.id]["player2"][1]}: Won!', color = discord.Color.gold())
                            embed.set_image(url=gameboard)
                            await ctx.channel.send(file=file, embed=embed)
                            return
                        elif self.singletictactoevar[ctx.guild.id]["current"].id == player2.id:
                            embed = discord.Embed(title='Game Over', description=f':tada: {player1.mention} :{self.singletictactoevar[ctx.guild.id]["player1"][1]}: Won!', color = discord.Color.gold())
                            embed.set_image(url=gameboard)
                            await ctx.channel.send(file=file, embed=embed)
                            return
                    elif result == 'draw':
                        embed = discord.Embed(title='Game Over', description='It was a draw. :x::o:', color=discord.Color.blue())
                        embed.set_image(url=gameboard)
                        await ctx.channel.send(file=file, embed=embed)
                    self.singletictactoevar.pop(ctx.guild.id)
                    return

                embed = discord.Embed(title=f'Turn {i}', description=f'{self.singletictactoevar[ctx.guild.id]["current"].mention}, Your turn please write a box no in chat', color=discord.Color.purple())
                embed.set_image(url=gameboard)
                await ctx.channel.send(file=file, embed=embed)
                
                if self.singletictactoevar[ctx.guild.id]["current"].id == ctx.user.id:
                    try:
                        gridno = await self.bot.wait_for('message', check=checkresponse, timeout=30)
                        if str(gridno.content).isdigit():
                            if int(gridno.content) <= 9:
                                use = convert(int(gridno.content))
                                if self.singletictactoevar[ctx.guild.id]["board"][use] == 'n':
                                    if self.singletictactoevar[ctx.guild.id]["current"].id == player1.id:
                                        cplayer = 'player1'
                                    else:
                                        cplayer = 'player2'
                                        
                                    self.singletictactoevar[ctx.guild.id]["board"][use] = self.singletictactoevar[ctx.guild.id][cplayer][1]

                                    if self.singletictactoevar[ctx.guild.id]["current"].id == player1.id:
                                        nextplayer = player2
                                    elif self.singletictactoevar[ctx.guild.id]["current"].id == player2.id:
                                        nextplayer = player1
                                        
                                    self.singletictactoevar[ctx.guild.id]["current"] = nextplayer
                                else:
                                    await ctx.channel.send(f'{self.singletictactoevar[ctx.guild.id]["current"].mention} Position `{gridno.content}` is already taken')
                            else:
                                await ctx.channel.send(f'{self.singletictactoevar[ctx.guild.id]["current"].mention} You need to respond with a number from **1-9**')
                        else:
                            await ctx.channel.send(f'{self.singletictactoevar[ctx.guild.id]["current"].mention} You need to respond with a number from **1-9**')
                    except asyncio.TimeoutError:
                        embed = discord.Embed(title='Timeout', description=f'⌛ {self.singletictactoevar[ctx.guild.id]["current"].mention} did not respond\n\n**Game Aborted**', color = discord.Color.blue())
                        self.singletictactoevar.pop(ctx.guild.id)
                        await ctx.channel.send(embed=embed)
                        return
                else:
                    if level == 'easy':
                        while True:
                            chose = random.choice(list(range(1,10,1)))
                            use = convert(int(chose))
                            if self.singletictactoevar[ctx.guild.id]["board"][use] == 'n':
                                await asyncio.sleep(1)
                                await ctx.channel.send(f'Nebula chose {chose}')
                                if self.singletictactoevar[ctx.guild.id]["current"].id == player1.id:
                                    cplayer = 'player1'
                                else:
                                    cplayer = 'player2'
                                self.singletictactoevar[ctx.guild.id]["board"][use] = self.singletictactoevar[ctx.guild.id][cplayer][1]
                                if self.singletictactoevar[ctx.guild.id]["current"].id == player1.id:
                                    nextplayer = player2
                                elif self.singletictactoevar[ctx.guild.id]["current"].id == player2.id:
                                    nextplayer = player1 
                                self.singletictactoevar[ctx.guild.id]["current"] = nextplayer
                                break
                    elif level == 'difficult':
                        chose = getanum(ctx.guild.id, self.singletictactoevar)
                        use = convert(int(chose))
                        await asyncio.sleep(1)
                        await ctx.channel.send(f'Nebula chose {chose}')
                        if self.singletictactoevar[ctx.guild.id]["current"].id == player1.id:
                            cplayer = 'player1'
                        else:
                            cplayer = 'player2'
                        self.singletictactoevar[ctx.guild.id]["board"][use] = self.singletictactoevar[ctx.guild.id][cplayer][1]
                        if self.singletictactoevar[ctx.guild.id]["current"].id == player1.id:
                            nextplayer = player2
                        elif self.singletictactoevar[ctx.guild.id]["current"].id == player2.id:
                            nextplayer = player1 
                        self.singletictactoevar[ctx.guild.id]["current"] = nextplayer
                        
        elif gametype.value == '2':
            embed = discord.Embed(title='Player Selection', description='Please mention somebody to play tic tac toe with', color=discord.Color.gold())
            await ctx.response.send_message(embed=embed)
            
            def tictactoeplayercheck(message):
                if message.author.id == ctx.user.id and '<@' in message.content:
                    return True
            def tictactoereactioncheck(reaction, member):
                if member.id == player.id and reaction.message.id == acceptdecline.id:
                    if reaction.emoji == '✅' or reaction.emoji == '🚫':
                        return True
            
            try:
                playermessage = await self.bot.wait_for('message', check=tictactoeplayercheck, timeout=30)
                player = extractid(playermessage.content)
                player = await self.bot.fetch_user(player)
                embed = discord.Embed(title='TicTacToe Invite', description=f'{playermessage.author.mention} has invited {player.mention} for a game of TicTacToe\n\n{player.mention} do you accept?', color=discord.Color.blue())
                acceptdecline = await playermessage.reply(player.mention, embed=embed, allowed_mentions=discord.AllowedMentions(replied_user=True))
                await acceptdecline.add_reaction('✅')
                await acceptdecline.add_reaction('🚫')
                try:
                    playerchoice = await self.bot.wait_for('reaction_add', check=tictactoereactioncheck, timeout=60)
                    if str(playerchoice[0].emoji) == '🚫':
                        await acceptdecline.clear_reactions()
                        embed = discord.Embed(title='Declined', description=f'🚫 {player.mention} declined', color=discord.Color.red())
                        await acceptdecline.edit(content=None, embed=embed)
                        return
                    elif str(playerchoice[0].emoji) == '✅':
                        await acceptdecline.clear_reactions()
                        embed = discord.Embed(title='Accepted', description=f'✅ {player.mention} accepted', color=discord.Color.green())
                        await acceptdecline.edit(content=None, embed=embed)
                        
                    player1icon = random.choice(['x', 'o'])
                    player1 = ctx.user
                    player2 = player
                    if player1icon == 'x':
                        player2icon = 'o'
                        currentplayer = player1
                    else:
                        player2icon = 'x'
                        currentplayer = player2
                        
                    self.tictactoevar[ctx.guild.id] = {'player1':[ctx.user.id, player1icon], 'player2':[player.id, player2icon], 'current':currentplayer, 'board':{"pos1":"n", "pos2":"n", "pos3":"n", "pos4":"n", "pos5":"n", "pos6":"n", "pos7":"n", "pos8":"n", "pos9":"n"}}

                    
                    embed = discord.Embed(title='Tic Tac Toe', description=f'A game is starting!\n\n', color=discord.Color.purple())
                    embed.add_field(name=f':{player1icon}:', value=player1.mention)
                    embed.add_field(name=f':{player2icon}:', value=player2.mention)
                    await ctx.channel.send(embed=embed)
                    
                    def checkresponse(message):
                        playerc = self.tictactoevar[ctx.guild.id]["current"]
                        if message.author.id == playerc.id and message.channel.id == ctx.channel.id:
                            return True
                    
                    i = 0
                    while True:
                        i += 1
                        # embed = discord.Embed(title=f'Turn {i}', description=f'{self.singletictactoevar[ctx.guild.id]["current"].mention}, Your turn please write a box no in chat', color=discord.Color.purple())
                        # embed.set_image(url='https://i.imgur.com/nJPPRNa.gif')
                        # prevmessage = await ctx.channel.send(embed=embed)
                        result = genboard(ctx.guild.id, self.tictactoevar)
                        # gameboard = uploadimgur('assets/tictactoe/currentboard.png', f'{ctx.guild.id}{player1.id}{player2.id}')
                        file = discord.File('assets/tictactoe/currentboard.png', filename='currentboard.png')
                        gameboard = 'attachment://currentboard.png'
                        if result != None:
                            if result == 'yes':
                                if self.tictactoevar[ctx.guild.id]["current"].id == player1.id:
                                    embed = discord.Embed(title='Game Over', description=f':tada: {player2.mention} :{self.tictactoevar[ctx.guild.id]["player2"][1]}: Won!', color = discord.Color.gold())
                                    embed.set_image(url=gameboard)
                                    await ctx.channel.send(file=file, embed=embed)
                                elif self.tictactoevar[ctx.guild.id]["current"].id == player2.id:
                                    embed = discord.Embed(title='Game Over', description=f':tada: {player1.mention} :{self.tictactoevar[ctx.guild.id]["player1"][1]}: Won!', color = discord.Color.gold())
                                    embed.set_image(url=gameboard)
                                    await ctx.channel.send(file=file, embed=embed)
                            elif result == 'draw':
                                embed = discord.Embed(title='Game Over', description='It was a draw. :x::o:', color=discord.Color.blue())
                                embed.set_image(url=gameboard)
                                await ctx.channel.send(file=file, embed=embed)
                            self.tictactoevar.pop(ctx.guild.id)
                            return

                        embed = discord.Embed(title=f'Turn {i}', description=f'{self.tictactoevar[ctx.guild.id]["current"].mention}, Your turn please write a box no in chat', color=discord.Color.purple())
                        embed.set_image(url=gameboard)
                        await ctx.channel.send(file=file, embed=embed)
                        try:
                            gridno = await self.bot.wait_for('message', check=checkresponse, timeout=30)
                            if str(gridno.content).isdigit():
                                if int(gridno.content) <= 9:
                                    use = convert(int(gridno.content))
                                    if self.tictactoevar[ctx.guild.id]["board"][use] == 'n':
                                        if self.tictactoevar[ctx.guild.id]["current"].id == player1.id:
                                            cplayer = 'player1'
                                        else:
                                            cplayer = 'player2'
                                            
                                        self.tictactoevar[ctx.guild.id]["board"][use] = self.tictactoevar[ctx.guild.id][cplayer][1]

                                        if self.tictactoevar[ctx.guild.id]["current"].id == player1.id:
                                            nextplayer = player2
                                        elif self.tictactoevar[ctx.guild.id]["current"].id == player2.id:
                                            nextplayer = player1
                                            
                                        self.tictactoevar[ctx.guild.id]["current"] = nextplayer
                                    else:
                                        await ctx.channel.send(f'{self.tictactoevar[ctx.guild.id]["current"].mention} Position `{gridno.content}` is already taken')
                                else:
                                    await ctx.channel.send(f'{self.tictactoevar[ctx.guild.id]["current"].mention} You need to respond with a number from **1-9**')
                            else:
                                await ctx.channel.send(f'{self.tictactoevar[ctx.guild.id]["current"].mention} You need to respond with a number from **1-9**')
                        except asyncio.TimeoutError:
                            embed = discord.Embed(title='Timeout', description=f'⌛ {self.tictactoevar[ctx.guild.id]["current"].mention} did not respond\n\n**Game Aborted**', color = discord.Color.blue())
                            self.tictactoevar.pop(ctx.guild.id)
                            await ctx.channel.send(embed=embed)
                            return
                except asyncio.TimeoutError:
                    await acceptdecline.clear_reactions()
                    embed = discord.Embed(title='Declined', description=f'⌛ {player.mention} did not respond', color=discord.Color.red())
                    await acceptdecline.edit(content=None, embed=embed)
                    return
            except asyncio.TimeoutError:
                embed = discord.Embed(title='Timeout', description=f':frowning: You did not respond', color=discord.Color.red())
                await ctx.edit_original_response(embed=embed)
                return
    
    @app_commands.command(name='wanted', description='Shows the users profile picture on a wanted poster')
    async def wanted(self, ctx, user: discord.User=None):
        if user == None:
            user = ctx.user
        avatar = user.avatar
        await ctx.response.defer()
        await fwanted(avatar)
        await ctx.followup.send(file=discord.File('assets/wanted/wanted.png'))
    
    @app_commands.command(name='prison', description='Shows the users profile picture in a prison')
    async def prison(self, ctx, user: discord.User=None):
        if user == None:
            user = ctx.user
        avatar = user.avatar
        await ctx.response.defer()
        await fprison(avatar)
        await ctx.followup.send(file=discord.File('assets/prison/prison.png'))
    
    @app_commands.command(name='tweet', description='Shows a custom twitter post')
    async def tweet(self, ctx, body: str, user: discord.User=None):
        if user == None:
            user = ctx.user
        avatar = user.avatar
        await ctx.response.defer()
        await ftweet(avatar, user.name, user.discriminator, body)
        await ctx.followup.send(file=discord.File('assets/twitter/tweet.png'))
    
    @app_commands.command(name='rockpaperscissors', description='Play a game of rock paper scissors')
    async def rockpaperscissors(self, ctx):
        view = View(timeout=15)
        rock = Button(label='Rock', emoji='🪨', style=discord.ButtonStyle.red)
        paper = Button(label='Paper', emoji='📜', style=discord.ButtonStyle.green)
        scissors = Button(label='Scissors', emoji='✂️', style=discord.ButtonStyle.blurple)
        
        async def rockcallback(interaction):
            global chosen
            chosen = '🪨 Rock'
        async def papercallback(interaction):
            global chosen
            chosen = '📜 Paper'
        async def scissorscallback(interaction):
            global chosen
            chosen = '✂️ Scissors'
            
        
        rock.callback = rockcallback
        paper.callback = papercallback
        scissors.callback = scissorscallback
        
        view.add_item(rock)
        view.add_item(paper)
        view.add_item(scissors)
        
        disabledview = View()
        rock = Button(label='Rock', emoji='🪨', style=discord.ButtonStyle.red, disabled=True)
        paper = Button(label='Paper', emoji='📜', style=discord.ButtonStyle.green, disabled=True)
        scissors = Button(label='Scissors', emoji='✂️', style=discord.ButtonStyle.blurple, disabled=True)
        disabledview.add_item(rock)
        disabledview.add_item(paper)
        disabledview.add_item(scissors)
        
        start = discord.Embed(title='Rock Paper Scissors', description=':rock: :scroll: :scissors:', color=discord.Color.from_str('#36393F'))
        await ctx.response.send_message(embed=start, view=view)

        timeout = discord.Embed(title='Rock Paper Scissors', description=':timer: Timeout! You did not respond within 15 seconds', color=discord.Color.blue())
        
        def rpscheck(event):
                if event.type == discord.InteractionType.component:
                    return True
        
        try:
            event = await self.bot.wait_for('interaction', check=rpscheck, timeout=15)
            await event.response.defer()
        except asyncio.TimeoutError:
            await ctx.edit_original_response(embed=timeout, view=disabledview)
            
        computer = ['📜 Paper', '🪨 Rock', '✂️ Scissors']
        computer = random.choice(computer)

        
        won = discord.Embed(description=':tada: You Won!', color=discord.Color.green())
        won.set_author(name=f'Winner - {str(ctx.user)}', icon_url=ctx.user.avatar)
        won.set_footer(text=f'Nebula chose {computer}')
        lost = discord.Embed(description=':frowning: You lost', color=discord.Color.red())
        lost.set_author(name=f'Winner - {str(self.bot.user)}', icon_url=self.bot.user.avatar)
        lost.set_footer(text=f'Nebula chose {computer}')
        tie = discord.Embed(description=':expressionless: It was a Tie!', color=discord.Color.purple())
        tie.set_author(name=f'Player - {str(ctx.user)}', icon_url=ctx.user.avatar)
        tie.set_footer(text=f'Nebula chose {computer}')
        
        
        if chosen == "🪨 Rock" and computer == "📜 Paper" or chosen == "📜 Paper" and computer == "✂️ Scissors" or chosen == "✂️ Scissors" and computer == "🪨 Rock":
            await ctx.edit_original_response(embed=lost, view=disabledview)
        elif chosen == computer:
            await ctx.edit_original_response(embed=tie, view=disabledview)
        else:
            await ctx.edit_original_response(embed=won, view=disabledview)
            
    @app_commands.command(name='diceroll', description='Roll a dice')
    async def diceroll(self, ctx):
        chosen = random.choice([('one', '<:nebula_one:1101819804677062690>'), ('two', '<:nebula_two:1101819814458179604>'), ('three', '<:nebula_three:1101819812067422218>'), ('four', '<:nebula_four:1101819802760261643>'), ('five', '<:nebula_five:1101819797500596264>'), ('six', '<:nebula_six:1101819808703578183>')])
        await ctx.response.send_message(f'{chosen[1]} :{chosen[0]}:')
        
    @app_commands.command(name='quiz', description='Start a quiz')
    async def quiz(self, ctx, channel: discord.TextChannel=None):
        if channel == None:
            channel = ctx.channel
        view = View()
        options = []
        for i in range(1, 16, 1):
            options.append(SelectOption(label=i, value=i))
        select = Select(placeholder='Select',options=options)
        view.add_item(select)
        await ctx.response.send_message(embed=discord.Embed(title='Questions', description='How many questions do you want?', color=discord.Color.gold()), ephemeral=True, view=view)
        disabledview = View()
        select.disabled = True
        disabledview.add_item(select)
        embed2 = discord.Embed(title='Times Up!', description='You ran out of time.', color=discord.Color.blue())
        def check(res):
            return ctx.user.id == res.user.id and res.channel == ctx.channel
        try:
            res = await self.bot.wait_for('interaction', check=check, timeout=30)
            await res.response.defer()
            num = int(res.data['values'][0])
        except asyncio.TimeoutError:
            await ctx.edit_original_response(embed=embed2, view=disabledview)
            return
        view = View()
        select = Select(placeholder='Select',options=[
                                            SelectOption(
                                                label='All',
                                                value='0',
                                                emoji="ℹ️"
                                            ),
                                            SelectOption(
                                                label='General Knowledge', 
                                                value='1',
                                                emoji="❓"
                                            ),
                                            SelectOption(
                                                label='Books', 
                                                value='2',
                                                emoji="📖"
                                            ),
                                            SelectOption(
                                                label='Film', 
                                                value='3',
                                                emoji="🎬"
                                            ),
                                            SelectOption(
                                                label='Music', 
                                                value='4',
                                                emoji="🎵"
                                            ),
                                            SelectOption(
                                                label='Theatre', 
                                                value='5',
                                                emoji="🎭"
                                            ),
                                            SelectOption(
                                                label='Telivision', 
                                                value='6',
                                                emoji="📺"
                                            ),
                                            SelectOption(
                                                label='Video Games', 
                                                value='7',
                                                emoji="🎮"
                                            ),
                                            SelectOption(
                                                label='Board Games', 
                                                value='8',
                                                emoji="🎲"
                                            ),
                                            SelectOption(
                                                label='Science', 
                                                value='9',
                                                emoji="🧪"
                                            ),
                                            SelectOption(
                                                label='Computer Science', 
                                                value='10',
                                                emoji="🖥️"
                                            ),
                                            SelectOption(
                                                label='Math', 
                                                value='11',
                                                emoji="🔢"
                                            ),
                                            SelectOption(
                                                label='Mythology', 
                                                value='12',
                                                emoji="🗿"
                                            ),
                                            SelectOption(
                                                label='Sports', 
                                                value='13',
                                                emoji="⚽"
                                            ),
                                            SelectOption(
                                                label='Geography', 
                                                value='14',
                                                emoji="🗺️"
                                            ),
                                            SelectOption(
                                                label='History', 
                                                value='15',
                                                emoji="👑"
                                            ),
                                            SelectOption(
                                                label='Politics', 
                                                value='16',
                                                emoji="🏛️"
                                            ),
                                            SelectOption(
                                                label='Art', 
                                                value='17',
                                                emoji="🎨"
                                            ),
                                            SelectOption(
                                                label='Celebrities', 
                                                value='18',
                                                emoji="🤩"
                                            ),
                                            SelectOption(
                                                label='Animals', 
                                                value='19',
                                                emoji="🦓"
                                            ),
                                            SelectOption(
                                                label='Vehicles', 
                                                value='20',
                                                emoji="🚚"
                                            ),
                                            SelectOption(
                                                label='Comics', 
                                                value='21',
                                                emoji="🗨️"
                                            ),
                                            SelectOption(
                                                label='Gadgets', 
                                                value='22',
                                                emoji="📱"
                                            ),
                                            SelectOption(
                                                label='Anime and Manga', 
                                                value='23',
                                                emoji="🍡"
                                            ),
                                            SelectOption(
                                                label='Cartoon', 
                                                value='24',
                                                emoji="🔍"
                                            ),
        ])
        view.add_item(select)
        embed = discord.Embed(title='Please choose a topic', description = 'You have 1 minute', color=discord.Color.gold())
        await ctx.edit_original_response(embed=embed, view=view)
        embed2 = discord.Embed(title='Times Up!', description='You ran out of time.', color=discord.Color.blue())
        disabledview = View()
        select.disabled = True
        disabledview.add_item(select)
        def check(res):
            return ctx.user.id == res.user.id and res.channel == ctx.channel
        try:
            res = await self.bot.wait_for('interaction', check=check, timeout=60)
            await res.response.defer()
            category = res.data['values'][0]
            category = int(category) + 8
            topic = select.options[int(category)-8].label
        except asyncio.TimeoutError:
            await ctx.edit_original_response(embed=embed2, view=disabledview)
            return
        view = View()
        select = Select(placeholder='Select',options=[
                                            SelectOption(
                                                label='Easy',
                                                value='easy',
                                                emoji="🙄"
                                            ),
                                            SelectOption(
                                                label='Medium', 
                                                value='medium',
                                                emoji="😉"
                                            ),
                                            SelectOption(
                                                label='Hard', 
                                                value='hard',
                                                emoji="😰"
                                            ),    
                                            SelectOption(
                                                label='All', 
                                                value='all',
                                                emoji="ℹ️"
                                            ),                      
        ])
        view.add_item(select)
        embed = discord.Embed(title='Please choose a difficulty level', description = 'You have 30 seconds', color=discord.Color.gold())
        await ctx.edit_original_response(embed=embed, view=view)
        embed2 = discord.Embed(title='Times Up!', description='You ran out of time.', color=discord.Color.blue())
        disabledview = View()
        select.disabled = True
        disabledview.add_item(select)
        def check(res):
            return ctx.user.id == res.user.id and res.channel == ctx.channel
        try:
            res = await self.bot.wait_for('interaction', check=check, timeout=30)
            await res.response.defer()
            hme = res.data['values'][0]
            ii = 0
            for i in select.options:
                if i.value == hme:
                    break
                ii += 1
            dif = select.options[ii].label
            if hme == 'all':
                hme = None
            embed = discord.Embed(title='Setup Complete', description=f'**Topic:** {topic}\n**Difficulty:** {dif}', color=discord.Color.green())
            await ctx.edit_original_response(embed=embed, view=disabledview)
        except asyncio.TimeoutError:
            await ctx.edit_original_response(embed=embed2, view=disabledview)
            return
        score = {}
        if category == 8:
            category = None
        embedstart = discord.Embed(title='Starting Quiz...', description=f'Please check {channel.mention}', color=discord.Color.green())
        await ctx.channel.send(embed=embedstart)
        embedstarta = discord.Embed(title='Quiz is starting!', description=f'A quiz created by **{ctx.user.name}**\n**Topic:** `{topic}`\n**Level:** `{dif}`\n**Question Count: **`{num}`\n**Estimated Time: **`{convertquiz(num*22)}`', color=discord.Color.orange())
        await channel.send(embed=embedstarta)
        await asyncio.sleep(3)
        for number in range(1,num+1,1):
            responded = []
            correct = []
            wrong = []
            response = {}
            q,i,c,d = question(category,hme)
            for j in i:
                response[j] = 0
            response[c] = 0
            ques = q
            points = 0
            if str(d) == 'easy':
                points = 10
            elif str(d) == 'medium':
                points = 20
            elif str(d) == 'hard':
                points = 30
            embed = discord.Embed(title=f'Question {number}/{num} ({points} points)', description=q, color=discord.Color.gold())
            embed.set_footer(text='You have 15 seconds')
            inc = []
            for inco in i:
                incoo = Button(style=discord.ButtonStyle.blurple, label=inco, custom_id=inco)
                inc.append(incoo)  
            c2 = Button(style=discord.ButtonStyle.blurple, label=c, custom_id=c)
            inc.append(c2)
            shuffle(inc)
            view = View()
            for ii in inc:
                view.add_item(ii)
                
            inc = []
            for inco in i:
                incoo = Button(style=discord.ButtonStyle.blurple, label=inco, custom_id=inco, disabled=True)
                inc.append(incoo)  
            c2 = Button(style=discord.ButtonStyle.blurple, label=c, custom_id=c, disabled=True)
            inc.append(c2)
            shuffle(inc)
            disabledview = View()
            for i in inc:
                disabledview.add_item(i)
            
            mes = await channel.send(embed=embed, view=view)
            def check(res):
                return res.channel == channel
            endTime = datetime.now() + timedelta(seconds=15)
            while True:
                if datetime.now() >= endTime:
                    embed.add_field(name='Results', value=f':white_check_mark: `{len(correct)}` **user(s) anwsered correctly**\n:no_entry_sign: `{len(wrong)}` **user(s) anwsered incorrectly**')
                    embed.set_footer(text='')
                    courses = list(response.keys())
                    values = list(response.values())
                    color = []
                    plt.figure(facecolor='#202225')
                    ax = plt.axes()
                    ax.set_facecolor("#202225")
                    for i in courses:
                        if i == c:
                            color.append('green')
                        else:
                            color.append('red')
                    
                    # creating the bar plot
                    plt.bar(courses, values, color = color,
                            width = 0.4)
                    plt.xticks(rotation=45)
                    plt.xlabel("Options")
                    plt.ylabel("No. of votes")
                    ax.xaxis.label.set_color('white')
                    ax.yaxis.label.set_color('white') 
                    ax.tick_params(axis='x', colors='white')
                    ax.tick_params(axis='y', colors='white')
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['bottom'].set_color("white")
                    ax.spines['left'].set_color("white")
                    plt.title(f"Question Results", color="white")
                    plt.tight_layout()
                    plt.savefig('storage/question.png')
                    plt.close()
                    
                    file = discord.File('storage/question.png', filename='question.png')
                    embed.set_image(url='attachment://question.png')
                    score2 = score.copy()
                    first = -1
                    first_user = ''
                    if len(score.keys()) >= 1:
                        for i in score2.keys():
                            if score2[i] > first:
                                first = score2[i]
                                first_user = self.bot.get_user(i).name
                                fuserid = i
                        score2.pop(fuserid)
                    else:
                        first_user = None
                    second = -1
                    second_user = ''
                    if len(score.keys()) >= 2:
                        for i in score2.keys():
                            if score2[i] > second:
                                second = score2[i]
                                second_user = self.bot.get_user(i).name
                                fuserid = i
                        score2.pop(fuserid)
                    else:
                        second_user = None
                    third = -1
                    third_user = ''
                    if len(score.keys()) >= 3:
                        for i in score2.keys():
                            if score2[i] > third:
                                third = score2[i]
                                third_user = self.bot.get_user(i).name
                                fuserid = i
                        score2.pop(fuserid)
                    else:
                        third_user = None
                    embed.add_field(name='Correct Answer', value=f':white_check_mark: {c}')
                    if first_user != None and second_user != None and third_user != None:
                        embed.add_field(name='Leaderboard', value=f':first_place: **{first_user}** - `{first}`\n:second_place: **{second_user}** - `{second}`\n:third_place: **{third_user}** - `{third}`', inline=False)
                    elif first_user != None and second_user != None:
                        embed.add_field(name='Leaderboard', value=f':first_place: **{first_user}** - `{first}`\n:second_place: **{second_user}** - `{second}`', inline=False)
                    elif first_user != None:
                        if number == 1:
                            embed = discord.Embed(title='No one joined!', description='You need atleast 2 people to join the quiz', color=discord.Color.red())
                            await channel.send(embed=embed)
                            embedend = discord.Embed(title='Quiz Ended', description=f'Your quiz has ended in {channel.mention}', color=discord.Color.red())
                            await ctx.channel.send(embed=embedend)
                            embed = discord.Embed(title=f'Question {number}/{num}', description=q, color=discord.Color.gold())
                            await mes.edit(embed=embed, view=disabledview)
                            return
                    else:
                        if number == 1:
                            embed = discord.Embed(title='No one joined!', description='You need atleast 2 people to join the quiz', color=discord.Color.red())
                            await channel.send(embed=embed)
                            embedend = discord.Embed(title='Quiz Ended', description=f'Your quiz has ended in {channel.mention}', color=discord.Color.red())
                            await ctx.channel.send(embed=embedend)
                            embed = discord.Embed(title=f'Question {number}/{num}', description=q, color=discord.Color.gold())
                            await mes.edit(embed=embed, view=disabledview)
                            return
                        embed.add_field(name='Leaderboard', value=f':first_place: **{first_user}** - `{first}`', inline=False)
                    await mes.edit(attachments=[file], embed=embed, view=disabledview)
                    break
                try:
                    res = await self.bot.wait_for('interaction', check=check, timeout=5)
                    chose = res.data['custom_id']
                    # q = str(q) + f'\n\n :white_check_mark: Correct Answer - {c}\n :orange_square: Your Answer - {chose}'
                    # embed3 = discord.Embed(title=f'Question {number} - Correct', description=q, color=discord.Color.green())
                    # embed4 = discord.Embed(title=f'Question {number} - Incorrect', description=q, color=discord.Color.red())
                    embed3 = discord.Embed(title=f'Question {number} - Submitted', description=str(q) + f'\n\n:orange_square: Your Answer - {chose}', color=discord.Color.orange())
                    embed5 = discord.Embed(description='You have already responded', color=discord.Color.orange())
                    try:
                        pscore = score[res.user.id]
                    except:
                        pscore = 0
                    if res.user.id not in responded:
                        if str(chose) == str(c):
                            score[res.user.id] = pscore + points
                            await res.response.send_message(embed=embed3, ephemeral=True)
                            responded.append(res.user.id)
                            correct.append(res.user.id)
                            response[chose] = response[chose] + 1
                        else:
                            score[res.user.id] = pscore
                            await res.response.send_message(embed=embed3, ephemeral=True)
                            responded.append(res.user.id)
                            wrong.append(res.user.id)
                            response[chose] = response[chose] + 1
                        q = ques
                    else:
                        score[res.user.id] = pscore
                        await res.response.send_message(embed=embed5, ephemeral=True)
                except:
                    pass
        score2 = score.copy()
        first = -1
        first_user = ''
        if len(score.keys()) >= 1:
            for i in score2.keys():
                if score2[i] > first:
                    first = score2[i]
                    first_user = self.bot.get_user(i).name
                    fuserid = i
                    fid = i
            score2.pop(fuserid)
        else:
            first_user = None
        second = -1
        second_user = ''
        if len(score.keys()) >= 2:
            for i in score2.keys():
                if score2[i] > second:
                    second = score2[i]
                    second_user = self.bot.get_user(i).name
                    fuserid = i
                    sid = i
            score2.pop(fuserid)
        else:
            second_user = None
        third = -1
        third_user = ''
        if len(score.keys()) >= 3:
            for i in score2.keys():
                if score2[i] > third:
                    third = score2[i]
                    third_user = self.bot.get_user(i).name
                    fuserid = i
                    tid = i
            score2.pop(fuserid)
        else:
            third_user = None
        if first_user != None:
            embed = discord.Embed(title='Quiz', description=f':tada: **{first_user}** won with `{first}` points!', color=discord.Color.gold())
        else:
            embed = discord.Embed(title='Quiz', description='😦 **No one participated**', color=discord.Color.red())
        if first_user != None and second_user != None and third_user != None:
            embed.add_field(name='Leaderboard', value=f':first_place: **{first_user}** - `{first}`\n:second_place: **{second_user}** - `{second}`\n:third_place: **{third_user}** - `{third}`', inline=False)
        elif first_user != None and second_user != None:
            embed.add_field(name='Leaderboard', value=f':first_place: **{first_user}** - `{first}`\n:second_place: **{second_user}** - `{second}`', inline=False)
        elif first_user != None:
            embed.add_field(name='Leaderboard', value=f':first_place: **{first_user}** - `{first}`', inline=False)
        await channel.send(embed=embed)
        if first_user != None:
            updatepoints(fid, getpoints(fid) + score[fid], getwins(fid) + 1, getgameslost(fid))
            score.pop(fid)
        if second_user != None:
            updatepoints(sid, getpoints(sid) + score[sid], getwins(sid), getgameslost(sid))
            score.pop(sid)
        if third_user != None:
            updatepoints(tid, getpoints(tid) + score[tid], getwins(tid), getgameslost(tid))
            score.pop(tid)
        for i in score.keys():
            updatepoints(i, getpoints(i) + score[i], getwins(i), getgameslost(i) + 1)
        embedend = discord.Embed(title='Quiz Ended', description=f'Your quiz has ended in {channel.mention}', color=discord.Color.green())
        await ctx.channel.send(embed=embedend)
    
    @app_commands.command(name='quizstats', description='View your quiz stats')
    async def qstats(self, ctx, user: discord.Member=None):
        if user == None:
            user = ctx.user
        embed = discord.Embed(title='Quiz Stats', description=f'Stats for {user.mention}', color=discord.Color.orange())
        embed.add_field(name='Total Score', value=f'💯 **`{getpoints(user.id)}`**', inline=False)
        total = getwins(user.id) + getgameslost(user.id)
        embed.add_field(name='Games Won', value=f'🏆 **`{getwins(user.id)}`/`{total}`**', inline=True)
        embed.add_field(name='Games Lost', value=f'😢 **`{getgameslost(user.id)}`/`{total}`**', inline=True)
        await ctx.response.send_message(embed=embed)
    
    @app_commands.command(name='quizleaderboard', description='View the quiz leaderboard')
    async def qlb(self, ctx):
        with open('storage/quiz.json') as file:
            data = json.load(file)
        gold = ''
        goldv = 0
        silver = ''
        silverv = 0
        bronz = ''
        bronzv = 0
        l = list(data.keys())
        for i in l:
            if int(data[i]["points"]) >= int(goldv):
                gold = i
                goldv = data[i]["points"]
        try:
            l.pop(l.index(gold))
        except:
            pass
        for i in l:
            if int(data[i]["points"]) >= int(silverv):
                silver = i
                silverv = data[i]["points"]
        try:
            l.pop(l.index(silver))
        except:
            pass
        for i in l:
            if int(data[i]["points"]) >= int(bronzv):
                bronz = i
                bronzv = data[i]["points"]
        try:
            l.pop(l.index(bronz))
        except:
            pass
        try:
            gold = await self.bot.fetch_user(gold)
        except:
            gold = None
            goldv = 0
        try:
            silver = await self.bot.fetch_user(silver)
        except:
            silver = None
            silverv = 0
        try:
            bronz = await self.bot.fetch_user(bronz)
        except:
            bronz = None
            bronzv = 0
        embed = discord.Embed(title='Quiz Leaderboard', color=discord.Color.gold())
        if gold != None:
            embed.add_field(name=f':first_place: - {str(goldv)} Points', value=f'`{gold}`', inline=False)
        if silver != None:
            embed.add_field(name=f':second_place: - {str(silverv)} Points', value=f'`{silver}`', inline=False)
        if bronz != None:
            embed.add_field(name=f':third_place: - {str(bronzv)} Points', value=f'`{bronz}`', inline=False)
        await ctx.response.send_message(embed=embed)
        
    @app_commands.command(name='connect4', description='Play a game of connect4')
    @app_commands.choices(gametype=[
            app_commands.Choice(name="Single Player", value="1"),
            app_commands.Choice(name="Multiplayer", value="2")
        ])
    async def connect4c(self, ctx, gametype: app_commands.Choice[str]):
        if gametype.value == '1':
            embed = discord.Embed(title='Level', description='Please choose a difficulty level', color=discord.Color.gold())
            view = View()
            
            async def easy(interaction):
                global level
                level = 'easy'
            async def difficult(interaction):
                global level
                level = 'difficult'
            
            easybutton = Button(label='Easy', style=discord.ButtonStyle.green)
            difficultbutton = Button(label='Difficult', style=discord.ButtonStyle.red)
            
            easybutton.callback = easy
            difficultbutton.callback = difficult
            
            view.add_item(easybutton)
            view.add_item(difficultbutton)
            await ctx.response.send_message(embed=embed, view=view)
            
            def levelcheck(event):
                if event.type == discord.InteractionType.component:
                    return True

            try:
                event = await self.bot.wait_for('interaction', check=levelcheck, timeout=20)
                await event.response.defer()
                embed = discord.Embed(title='Level', description=f'Difficulty level has been set to **{level.capitalize()}**', color=discord.Color.gold())
                view = View()
                easybutton = Button(label='Easy', style=discord.ButtonStyle.green, disabled=True)
                difficultbutton = Button(label='Difficult', style=discord.ButtonStyle.red, disabled=True)
                view.add_item(easybutton)
                view.add_item(difficultbutton)
                await ctx.edit_original_response(embed=embed, view=view)
                player1 = ctx.user
                player2 = self.bot.user
                p1 = ctx.user.id
                p2 = self.bot.user.id
                icons = ['red_circle', 'yellow_circle']
                player1icon = random.choice(icons)
                icons.pop(icons.index(player1icon))
                player2icon = icons[0]
                if player1icon == 'red_circle':
                    player1color = 'red'
                    player2color = 'yellow'
                else:
                    player1color = 'yellow'
                    player2color = 'red'
                id = ctx.guild.id
                self.sconnect4[id] = [['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n']]
                self.sconnect4mem[id] = {"player1":p1, "player2":p2}
                embed = discord.Embed(title='Connect4', description=f'A game is starting!\n\n', color=discord.Color.purple())
                embed.add_field(name=f':{player1icon}:', value=player1.mention)
                embed.add_field(name=f':{player2icon}:', value=player2.mention)
                await ctx.channel.send(embed=embed)
                turn = player1
                ii = 0
                while True:
                    ii += 1
                    # embed = discord.Embed(title=f'Turn {ii}', description=f'{turn.mention}, Your turn please write a box no in chat', color=discord.Color.purple())
                    # embed.set_image(url='https://i.imgur.com/nJPPRNa.gif')
                    # prevmessage = await ctx.channel.send(embed=embed)
                    checkvar = checkconnect4(id, self.sconnect4)
                    draw = None
                    for i in self.sconnect4[id]:
                        if draw == False:
                            break
                        for j in i:
                            if j == 'n':
                                draw = False
                                break
                        else:
                            draw = True
                    if checkvar == '1':
                        embed = discord.Embed(title=f'Game Over', description=f':{player1icon}: {player1.mention} Won', color=discord.Color.gold())
                        genconnect4(id, self.sconnect4)
                        # gameboard = uploadimgur('assets/connect4/currentboard.png', f'{ctx.guild.id}{player1.id}{player2.id}')
                        file = discord.File('assets/connect4/currentboard.png', filename='currentboard.png')
                        gameboard = 'attachment://currentboard.png'
                        embed.set_image(url=gameboard)
                        await ctx.channel.send(file=file, embed=embed)
                        self.sconnect4.pop(ctx.guild.id)
                        self.sconnect4mem.pop(ctx.guild.id)
                        return
                    elif checkvar == '2':
                        embed = discord.Embed(title=f'Game Over', description=f':{player2icon}: {player2.mention} Won', color=discord.Color.gold())
                        genconnect4(id, self.sconnect4)
                        # gameboard = uploadimgur('assets/connect4/currentboard.png', f'{ctx.guild.id}{player1.id}{player2.id}')
                        file = discord.File('assets/connect4/currentboard.png', filename='currentboard.png')
                        gameboard = 'attachment://currentboard.png'
                        embed.set_image(url=gameboard)
                        await ctx.channel.send(file=file, embed=embed)
                        self.sconnect4.pop(ctx.guild.id)
                        self.sconnect4mem.pop(ctx.guild.id)
                        return
                    elif draw == True:
                        embed = discord.Embed(title=f'Game Over', description='Game Draw', color=discord.Color.gold())
                        genconnect4(id, self.sconnect4)
                        # gameboard = uploadimgur('assets/connect4/currentboard.png', f'{ctx.guild.id}{player1.id}{player2.id}')
                        file = discord.File('assets/connect4/currentboard.png', filename='currentboard.png')
                        gameboard = 'attachment://currentboard.png'
                        embed.set_image(url=gameboard)
                        await ctx.channel.send(file=file, embed=embed)
                        self.sconnect4.pop(ctx.guild.id)
                        self.sconnect4mem.pop(ctx.guild.id)
                        return
                                # else:
                                #     await ctx.channel.send(f'{turn.mention} your turn, mention a column number to move.')
                    genconnect4(id, self.sconnect4)
                    # gameboard = uploadimgur('assets/connect4/currentboard.png', f'{ctx.guild.id}{player1.id}{player2.id}')
                    file = discord.File('assets/connect4/currentboard.png', filename='currentboard.png')
                    gameboard = 'attachment://currentboard.png'
                    embed = discord.Embed(title=f'Turn {ii}', description=f'{turn.mention}, Your turn please write a box no in chat', color=discord.Color.purple())
                    embed.set_image(url=gameboard)
                    await ctx.channel.send(file=file, embed=embed)
                    if checkvar == '1' or checkvar == '2' or draw == True:
                        if id in self.sconnect4.keys():
                            self.sconnect4.pop(id)
                        break
                    def check(res):
                        return res.author.id == turn and res.channel.id == ctx.channel.id
                    try:
                        if turn == self.bot.user:
                            if id in self.sconnect4.keys():
                                if level == 'easy':
                                    if turn.id == p1:
                                        color = player1color
                                    elif turn.id == p2:
                                        color = player2color
                                    while True:
                                        chose = random.choice(list(range(1,8,1)))
                                        if connect4move(id,int(chose), color, self.sconnect4) != False:
                                            break
                                    await ctx.channel.send(f'Nebula chose {chose}')
                                    if turn.id == p1:
                                        turn = player2
                                    elif turn.id == p2:
                                        turn = player1
                                elif level == 'difficult':
                                    if turn.id == p1:
                                        color = player1color
                                    elif turn.id == p2:
                                        color = player2color
                                    while True:
                                        column = connect3(id, self.sconnect4)
                                        print(column)
                                        if column == 'random':
                                            while True:
                                                chose = random.choice(list(range(1,8,1)))
                                                if connect4move(id,int(chose), color, self.sconnect4) != False:
                                                    break
                                            await ctx.channel.send(f'Nebula chose {chose}')
                                            break
                                        if connect4move(id,int(column), color, self.sconnect4) != False:
                                            await ctx.channel.send(f'Nebula chose {column}')
                                            break
                                    if turn.id == p1:
                                        turn = player2
                                    elif turn.id == p2:
                                        turn = player1
                            else:
                                return
                        else:
                            def check(res):
                                    return res.author.id == turn.id and res.channel.id == ctx.channel.id
                            destroy = False
                            while True:
                                try:
                                    mes = await self.bot.wait_for('message', check=check, timeout=30)
                                    if id in self.sconnect4.keys():
                                        mes = mes.content
                                        if mes.isdigit():
                                            if int(mes) <= 7:
                                                if turn.id == p1:
                                                    color = player1color
                                                elif turn.id == p2:
                                                    color = player2color
                                                moved = connect4move(id,int(mes), color, self.sconnect4)
                                                if moved != False:
                                                    if turn.id == p1:
                                                        turn = player2
                                                    elif turn.id == p2:
                                                        turn = player1
                                                    break
                                                else:
                                                    await ctx.channel.send(f'{turn.mention} the colum is already full')       
                                            else:
                                                await ctx.channel.send(f'{turn.mention} choose a number between 1-7')
                                        else:
                                            await ctx.channel.send(f'{turn.mention} choose a number between 1-7')
                                    else:
                                        pass
                                except asyncio.TimeoutError:
                                    if id in self.sconnect4.keys():
                                        self.sconnect4.pop(id)
                                        await ctx.channel.send(embed=discord.Embed(title='Timeout', description=f'{turn.mention} did not respond within 30 seconds', color=discord.Color.red()))
                                    destroy = True
                            if destroy == True:
                                break
                            # mes = await self.bot.wait_for('message', check=check, timeout=30)
                            # if id in self.sconnect4.keys():
                            #     mes = mes.content
                            #     if mes.isdigit():
                            #         if int(mes) <= 7:
                            #             if turn == p1:
                            #                 color = "yellow"
                            #             elif turn == p2:
                            #                 color = "red"
                            #             moved = connect4move(id,int(mes), color, self.connect4)
                            #             if moved != False:
                            #                 if turn.id == p1:
                            #                     turn = player2
                            #                 elif turn.id == p2:
                            #                     turn = player1
                            #             else:
                            #                 await ctx.channel.send(f'{turn.mention} the colum is already full')       
                            #         else:
                            #             await ctx.channel.send(f'{turn.mention} choose a number between 1-7')
                            #     else:
                            #         await ctx.channel.send(f'{turn.mention} choose a number between 1-7')
                            # else:
                            #     return
                    except asyncio.TimeoutError:
                        if id in self.sconnect4.keys():
                            self.sconnect4.pop(id)
                            await ctx.channel.send(embed=discord.Embed(title='Timeout', description=f'{turn.mention} did not respond within 30 seconds', color=discord.Color.red()))
                        break
            except asyncio.TimeoutError:
                embed = discord.Embed(title='Level', description=':frowning: You did not respond', color=discord.Color.blue())
                view = View()
                easybutton = Button(label='Easy', style=discord.ButtonStyle.green, disabled=True)
                difficultbutton = Button(label='Difficult', style=discord.ButtonStyle.red, disabled=True)
                view.add_item(easybutton)
                view.add_item(difficultbutton)
                await ctx.edit_original_response(embed=embed, view=view)
                return
            
            
            
        elif gametype.value == '2':
            embed = discord.Embed(title='Player Selection', description='Please mention somebody to play connect4 with', color=discord.Color.gold())
            await ctx.response.send_message(embed=embed)
            
            def tictactoeplayercheck(message):
                if message.author.id == ctx.user.id and '<@' in message.content:
                    return True
            def tictactoereactioncheck(reaction, member):
                if member.id == player.id and reaction.message.id == acceptdecline.id:
                    if reaction.emoji == '✅' or reaction.emoji == '🚫':
                        return True
            
            try:
                playermessage = await self.bot.wait_for('message', check=tictactoeplayercheck, timeout=30)
                player = extractid(playermessage.content)
                player = await self.bot.fetch_user(player)
                embed = discord.Embed(title='Connect4 Invite', description=f'{playermessage.author.mention} has invited {player.mention} for a game of TicTacToe\n\n{player.mention} do you accept?', color=discord.Color.blue())
                acceptdecline = await playermessage.reply(player.mention, embed=embed, allowed_mentions=discord.AllowedMentions(replied_user=True))
                await acceptdecline.add_reaction('✅')
                await acceptdecline.add_reaction('🚫')
                try:
                    playerchoice = await self.bot.wait_for('reaction_add', check=tictactoereactioncheck, timeout=60)
                    if str(playerchoice[0].emoji) == '🚫':
                        await acceptdecline.clear_reactions()
                        embed = discord.Embed(title='Declined', description=f'🚫 {player.mention} declined', color=discord.Color.red())
                        await acceptdecline.edit(content=None, embed=embed)
                        return
                    elif str(playerchoice[0].emoji) == '✅':
                        await acceptdecline.clear_reactions()
                        embed = discord.Embed(title='Accepted', description=f'✅ {player.mention} accepted', color=discord.Color.green())
                        await acceptdecline.edit(content=None, embed=embed)
            
                    if ctx.guild.id not in self.connect4.keys():
                        if ctx.user.id != player.id:
                            player1 = ctx.user
                            player2 = player
                            p1 = ctx.user.id
                            p2 = player.id
                            id = ctx.guild.id
                            icons = ['red_circle', 'yellow_circle']
                            player1icon = random.choice(icons)
                            icons.pop(icons.index(player1icon))
                            player2icon = icons[0]
                            if player1icon == 'red_circle':
                                player1color = 'red'
                                player2color = 'yellow'
                            else:
                                player1color = 'yellow'
                                player2color = 'red'
                            self.connect4[id] = [['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n'], ['n','n','n','n','n','n','n']]
                            self.connect4mem[id] = {"player1":p1, "player2":p2}
                            embed = discord.Embed(title='Connect4', description=f'A game is starting!\n\n', color=discord.Color.purple())
                            embed.add_field(name=f':{player1icon}:', value=player1.mention)
                            embed.add_field(name=f':{player2icon}:', value=player2.mention)
                            await ctx.channel.send(embed=embed)
                            turn = player1
                            ii = 0
                            while True:
                                ii += 1
                                # embed = discord.Embed(title=f'Turn {ii}', description=f'{turn.mention}, Your turn please write a box no in chat', color=discord.Color.purple())
                                # embed.set_image(url='https://i.imgur.com/nJPPRNa.gif')
                                # prevmessage = await ctx.channel.send(embed=embed)
                                checkvar = checkconnect4(id, self.connect4)
                                draw = None
                                for i in self.connect4[id]:
                                    if draw == False:
                                        break
                                    for j in i:
                                        if j == 'n':
                                            draw = False
                                            break
                                    else:
                                        draw = True
                                if checkvar == '1':
                                    embed = discord.Embed(title=f'Game Over', description=f':{player1icon}: {player1.mention} Won', color=discord.Color.gold())
                                    genconnect4(id, self.connect4)
                                    # gameboard = uploadimgur('assets/connect4/currentboard.png', f'{ctx.guild.id}{player1.id}{player2.id}')
                                    file = discord.File('assets/connect4/currentboard.png', filename='currentboard.png')
                                    gameboard = 'attachment://currentboard.png'
                                    embed.set_image(url=gameboard)
                                    await ctx.channel.send(file=file, embed=embed)
                                    self.connect4.pop(ctx.guild.id)
                                    self.connect4mem.pop(ctx.guild.id)
                                    return
                                elif checkvar == '2':
                                    embed = discord.Embed(title=f'Game Over', description=f':{player2icon}: {player2.mention} Won', color=discord.Color.gold())
                                    genconnect4(id, self.connect4)
                                    # gameboard = uploadimgur('assets/connect4/currentboard.png', f'{ctx.guild.id}{player1.id}{player2.id}')
                                    file = discord.File('assets/connect4/currentboard.png', filename='currentboard.png')
                                    gameboard = 'attachment://currentboard.png'
                                    embed.set_image(url=gameboard)
                                    await ctx.channel.send(file=file, embed=embed)
                                    self.connect4.pop(ctx.guild.id)
                                    self.connect4mem.pop(ctx.guild.id)
                                    return
                                elif draw == True:
                                    embed = discord.Embed(title=f'Game Over', description='Game Draw', color=discord.Color.gold())
                                    genconnect4(id, self.connect4)
                                    # gameboard = uploadimgur('assets/connect4/currentboard.png', f'{ctx.guild.id}{player1.id}{player2.id}')
                                    file = discord.File('assets/connect4/currentboard.png', filename='currentboard.png')
                                    gameboard = 'attachment://currentboard.png'
                                    embed.set_image(url=gameboard)
                                    await ctx.channel.send(file=file, embed=embed)
                                    self.connect4.pop(ctx.guild.id)
                                    self.connect4mem.pop(ctx.guild.id)
                                    return
                                # else:
                                #     await ctx.channel.send(f'{turn.mention} your turn, mention a column number to move.')
                                genconnect4(id, self.connect4)
                                # gameboard = uploadimgur('assets/connect4/currentboard.png', f'{ctx.guild.id}{player1.id}{player2.id}')
                                file = discord.File('assets/connect4/currentboard.png', filename='currentboard.png')
                                gameboard = 'attachment://currentboard.png'
                                embed = discord.Embed(title=f'Turn {ii}', description=f'{turn.mention}, Your turn please write a box no in chat', color=discord.Color.purple())
                                embed.set_image(url=gameboard)
                                await ctx.channel.send(file=file, embed=embed)
                                if checkvar == '1' or checkvar == '2' or draw == True:
                                    if id in self.connect4.keys():
                                        self.connect4.pop(id)
                                    break
                                def check(res):
                                    return res.author.id == turn.id and res.channel.id == ctx.channel.id
                                destroy = False
                                while True:
                                    try:
                                        mes = await self.bot.wait_for('message', check=check, timeout=30)
                                        if id in self.connect4.keys():
                                            mes = mes.content
                                            if mes.isdigit():
                                                if int(mes) <= 7:
                                                    if turn.id == p1:
                                                        color = player1color
                                                    elif turn.id == p2:
                                                        color = player2color
                                                    moved = connect4move(id,int(mes), color, self.connect4)
                                                    if moved != False:
                                                        if turn.id == p1:
                                                            turn = player2
                                                        elif turn.id == p2:
                                                            turn = player1
                                                        break
                                                    else:
                                                        await ctx.channel.send(f'{turn.mention} the colum is already full')       
                                                else:
                                                    await ctx.channel.send(f'{turn.mention} choose a number between 1-7')
                                            else:
                                                await ctx.channel.send(f'{turn.mention} choose a number between 1-7')
                                        else:
                                            pass
                                    except asyncio.TimeoutError:
                                        if id in self.connect4.keys():
                                            self.connect4.pop(id)
                                            await ctx.channel.send(embed=discord.Embed(title='Timeout', description=f'{turn.mention} did not respond within 30 seconds', color=discord.Color.red()))
                                        destroy = True
                                if destroy == True:
                                    break
                        else:
                            await ctx.channel.send(embed=discord.Embed(title='Error', description=f':x: You cannot play with yourself', color=discord.Color.red()))
                    else:
                        await ctx.channel.send(embed=discord.Embed(title='Error', description=f'A game in **{ctx.guild.name}** is in progress', color=discord.Color.red()))
                except asyncio.TimeoutError:
                        await acceptdecline.clear_reactions()
                        embed = discord.Embed(title='Declined', description=f'⌛ {player.mention} did not respond', color=discord.Color.red())
                        await acceptdecline.edit(content=None, embed=embed)
                        return
            except asyncio.TimeoutError:
                embed = discord.Embed(title='Timeout', description=f':frowning: You did not respond', color=discord.Color.red())
                await ctx.edit_original_response(embed=embed)
                return
    # @app_commands.command(name='test', description='test')
    # async def test(self, ctx):
    #     embed = discord.Embed(title='test')
    #     file = discord.File('assets/connect4/currentboard.png', filename='currentboard.png')
    #     embed.set_image(url='attachment://currentboard.png')
    #     await ctx.response.send_message(file=file, embed=embed)


async def setup(bot:commands.Bot) -> None:
        await bot.add_cog(fun(bot), guilds = []) #leave empty for all servers