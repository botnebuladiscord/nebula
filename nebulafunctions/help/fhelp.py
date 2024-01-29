from discord import Embed, Color
def returnembed(command):
          command = command.lower()
          command = command.replace(' ', '')
          if command == 'add':
              embed = Embed(title='Add', description='Adds numbers', color=Color.gold())
              embed.add_field(name='Usage', value='`/add [numbers separated by commas]`', inline=False)
              embed.add_field(name='Example', value='`/add [1,2,3]`', inline=False)
              return embed
          elif command == 'subtract':
              embed = Embed(title='Subtract', description='Subtracts numbers', color=Color.gold())
              embed.add_field(name='Usage', value='`/subtract [numbers separated by commas]`', inline=False)
              embed.add_field(name='Example', value='`/subtract [4,2,1]`', inline=False)
              return embed
          elif command == 'multiply':
              embed = Embed(title='Multiply', description='Multiply numbers', color=Color.gold())
              embed.add_field(name='Usage', value='`/multiply [numbers separated by commas]`', inline=False)
              embed.add_field(name='Example', value='`/multiply [1,2,3]`', inline=False)
              return embed
          elif command == 'divide':
              embed = Embed(title='Divide', description='Divide numbers', color=Color.gold())
              embed.add_field(name='Usage', value='`/divide [numbers separated by commas]`', inline=False)
              embed.add_field(name='Example', value='`/divide [4,2]`', inline=False)
              return embed
          elif command == 'squareroot':
              embed = Embed(title='Square Root', description='Find the square root of a number', color=Color.gold())
              embed.add_field(name='Usage', value='`/squareroot [number]`', inline=False)
              embed.add_field(name='Example', value='`/squareroot [4]`', inline=False)
              return embed
          elif command == 'cuberoot':
              embed = Embed(title='Cube Root', description='Find the cube root of a number', color=Color.gold())
              embed.add_field(name='Usage', value='`/cuberoot [number]`', inline=False)
              embed.add_field(name='Example', value='`/cuberoot [8]`', inline=False)
              return embed
          elif command == 'circumference':
              embed = Embed(title='Circumference', description='Find the circumference of a circle', color=Color.gold())
              embed.add_field(name='Usage', value='`/circumference [inputtype(Radius/Diameter)] [number]`', inline=False)
              embed.add_field(name='Example', value='`/circumference [Radius] [5]`', inline=False)
              return embed
          elif command == 'speed':
              embed = Embed(title='Speed', description='Find the speed of an object', color=Color.gold())
              embed.add_field(name='Usage', value='`/speed [distance] [time]`', inline=False)
              embed.add_field(name='Example', value='`/speed [10] [5]`', inline=False)
              return embed
          elif command == 'distance':
              embed = Embed(title='Distance', description='Find the distance an object traveled', color=Color.gold())
              embed.add_field(name='Usage', value='`/distance [speed] [time]`', inline=False)
              embed.add_field(name='Example', value='`/distance [2] [5]`', inline=False)
              return embed
          elif command == 'time':
              embed = Embed(title='Time', description='Find the time an object takes to cover a distance', color=Color.gold())
              embed.add_field(name='Usage', value='`/time [distance] [speed]`', inline=False)
              embed.add_field(name='Example', value='`/time [10] [2]`', inline=False)
              return embed
          elif command == 'tictactoe':
              embed = Embed(title='Tic Tac Toe', color=Color.gold())
              embed.add_field(name='Single Player', value='Play a game with the **bot**', inline=False)
              embed.add_field(name='Multiplayer', value='Play a game with **your friends**', inline=False)
              embed.add_field(name='Usage', value='`/tictactoe [type]`', inline=False)
              embed.add_field(name='Example', value='`/tictactoe [Single Player]`', inline=False)
              return embed
          elif command == 'wanted':
              embed = Embed(title='Wanted', description='Shows the users profile picture on a wanted poster', color=Color.gold())
              embed.add_field(name='Usage', value='`/wanted [user(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/wanted [@Nebula]`', inline=False)
              return embed
          elif command == 'prison':
              embed = Embed(title='Prison', description='Shows the users profile picture in a prison', color=Color.gold())
              embed.add_field(name='Usage', value='`/prison [user(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/prison [@Nebula]`', inline=False)
              return embed
          elif command == 'rockpaperscissors':
              embed = Embed(title='Rock Paper Scissors', description='Play a game of rock paper scissors', color=Color.gold())
              embed.add_field(name='Usage', value='`/rockpaperscissors`', inline=False)
              embed.add_field(name='Example', value='`/rockpaperscissors`', inline=False)
              return embed
          elif command == 'tweet':
              embed = Embed(title='Tweet', description='Make a custom twitter post', color=Color.gold())
              embed.add_field(name='Usage', value='`/tweet [body][user(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/tweet [Hello][@Nebula]`', inline=False)
              return embed
          elif command == 'diceroll':
              embed = Embed(title='Dice Roll', description='Roll a dice', color=Color.gold())
              embed.add_field(name='Usage', value='`/diceroll`', inline=False)
              embed.add_field(name='Example', value='`/diceroll`', inline=False)
              return embed
          elif command == 'quiz':
              embed = Embed(title='Quiz', description='Start a quiz', color=Color.gold())
              embed.add_field(name='Usage', value='`/quiz [channel(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/quiz [#general]`', inline=False)
              return embed
          elif command == 'quizstats':
              embed = Embed(title='Quiz Stats', description='View your quiz stats', color=Color.gold())
              embed.add_field(name='Usage', value='`/quizstats [user(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/quizstats [@Nebula]`', inline=False)
              return embed
          elif command == 'quizleaderboard':
              embed = Embed(title='Quiz Leaderboard', description='View the quiz leaderboard', color=Color.gold())
              embed.add_field(name='Usage', value='`/quizleaderboard`', inline=False)
              embed.add_field(name='Example', value='`/quizleaderboard`', inline=False)
              return embed
          elif command == 'connect4':
              embed = Embed(title='Connect4', color=Color.gold())
              embed.add_field(name='Single Player', value='Play a game with the **bot**', inline=False)
              embed.add_field(name='Multiplayer', value='Play a game with **your friends**', inline=False)
              embed.add_field(name='Usage', value='`/connect4 [type]`', inline=False)
              embed.add_field(name='Example', value='`/connect4 [Single Player]`', inline=False)
              return embed
          elif command == 'kick':
              embed = Embed(title='Kick', description='Kick a server member', color=Color.gold())
              embed.add_field(name='Usage', value='`/kick [user] [reason(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/kick [@Cosmos] [test]`', inline=False)
              embed.set_footer(text='Requires Kick Members permission')
              return embed
          elif command == 'ban':
              embed = Embed(title='Ban', description='Ban a server member', color=Color.gold())
              embed.add_field(name='Usage', value='`/ban [user] [delete_mesages] [reason(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/ban [@Cosmos] [Previous Hour] [test]`', inline=False)
              embed.set_footer(text='Requires Ban Members permission')
              return embed
          elif command == 'slowmode':
              embed = Embed(title='Slowmode', description='Set channel slowmode', color=Color.gold())
              embed.add_field(name='Usage', value='`/slowmode [seconds]`', inline=False)
              embed.add_field(name='Example', value='`/slowmode [5]`', inline=False)
              embed.set_footer(text='Requires Manage Channels permission')
              return embed
          elif command == 'create':
              embed = Embed(title='Create', description='Create a channel', color=Color.gold())
              embed.add_field(name='Usage', value='`/create [name] [category(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/create [nebula-updates] [nebula info]`', inline=False)
              embed.set_footer(text='Requires Manage Channels permission')
              return embed
          elif command == 'delete':
              embed = Embed(title='Delete', description='Delete a channel', color=Color.gold())
              embed.add_field(name='Usage', value='`/delete [channel]`', inline=False)
              embed.add_field(name='Example', value='`/delete [#chat]`', inline=False)
              embed.set_footer(text='Requires Manage Channels permission')
              return embed
          elif command == 'poll':
              embed = Embed(title='Poll', description='Create a poll', color=Color.gold())
              embed.add_field(name='Usage', value='`/poll [channel] [question] [time] [emojis]`', inline=False)
              embed.add_field(name='Example', value='`/poll [#chat] [Does pineapple belong on pizza?] [2h] [✅ ❌]`', inline=False)
              embed.add_field(name='Note: Time parameter', value='**Seconds:** `s` (`30s`)\n**Minutes:** `m` (`10m`)\n**Hours:** `h` (`1h`)\n**Days:** `d` (`1d`)', inline=False)
              embed.set_footer(text='Requires the user to be able to send messages in the specific channel')
              return embed
          elif command == 'announce':
              embed = Embed(title='Announce', description='Create an announcement', color=Color.gold())
              embed.add_field(name='Usage', value='`/announce [channel] [title] [message] [embedcolor(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/announce [#chat] [Slash Commands] [Nebula now has slash commands] [#FFFFFF]`', inline=False)
              embed.set_footer(text='Requires the user to be able to send messages in the specific channel')
              return embed
          elif command == 'lock':
              embed = Embed(title='Lock', description='Lock a channel', color=Color.gold())
              embed.add_field(name='Usage', value='`/lock [channel] [lock_for] [reason(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/lock [#chat] [@everyone] [Test]`', inline=False)
              embed.set_footer(text='Requires Manage Channels permission')
              return embed
          elif command == 'unlock':
              embed = Embed(title='Unlock', description='Unlock a channel', color=Color.gold())
              embed.add_field(name='Usage', value='`/unlock [channel] [unlock_for] [reason(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/unlock [#chat] [@everyone] [Test]`', inline=False)
              embed.set_footer(text='Requires Manage Channels permission')
              return embed
          elif command == 'unban':
              embed = Embed(title='Unban', description='Unban a server member', color=Color.gold())
              embed.add_field(name='Usage', value='`/unban [userid] [reason(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/unban [953533453100527626] [test]`', inline=False)
              embed.set_footer(text='Requires Ban Members permission')
              return embed
          elif command == 'giveaway':
              embed = Embed(title='Giveaway', description='Create a giveaway', color=Color.gold())
              embed.add_field(name='Usage', value='`/giveaway [channel] [prize] [time]`', inline=False)
              embed.add_field(name='Example', value='`/giveaway [#chat] [Nitro] [2h]`', inline=False)
              embed.add_field(name='Note: Time parameter', value='**Seconds:** `s` (`30s`)\n**Minutes:** `m` (`10m`)\n**Hours:** `h` (`1h`)\n**Days:** `d` (`1d`)', inline=False)
              embed.set_footer(text='Requires the user to be able to send messages in the specific channel')
              return embed
          elif command == 'tempban':
              embed = Embed(title='Temporary Ban', description='Temporary Ban a server member', color=Color.gold())
              embed.add_field(name='Usage', value='`/tempban [user] [delete_mesages] [time] [reason(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/tempban [@Cosmos] [Previous Hour] [2h] [test]`', inline=False)
              embed.add_field(name='Note: Time parameter', value='**Seconds:** `s` (`30s`)\n**Minutes:** `m` (`10m`)\n**Hours:** `h` (`1h`)\n**Days:** `d` (`1d`)', inline=False)
              embed.set_footer(text='Requires Ban Members permission')
              return embed
          elif command == 'warn':
              embed = Embed(title='Warn', description='Warn a user', color=Color.gold())
              embed.add_field(name='Usage', value='`/warn [user] [reason]`', inline=False)
              embed.add_field(name='Example', value='`/warn [@Cosmos] [test]`', inline=False)
              embed.set_footer(text='Requires Manage Messages permission')
              return embed
          elif command == 'warnings':
              embed = Embed(title='Warnings', description='View warnings for a user', color=Color.gold())
              embed.add_field(name='Usage', value='`/warnings [user(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/warnings [@Cosmos]`', inline=False)
              return embed
          elif command == 'delwarn':
              embed = Embed(title='Delete Warn', description='Delete a warning', color=Color.gold())
              embed.add_field(name='Usage', value='`/delwarn [warnid]`', inline=False)
              embed.add_field(name='Example', value='`/delwarn [b54ee6e9d06003cm8118935947167662101]`', inline=False)
              embed.set_footer(text='Requires Manage Messages permission')
              return embed
          elif command == 'userinfo':
              embed = Embed(title='User Info', description='View information on a user', color=Color.gold())
              embed.add_field(name='Usage', value='`/userinfo [user]`', inline=False)
              embed.add_field(name='Example', value='`/userinfo [@Cosmos]`', inline=False)
              return embed
          elif command == 'serverinfo':
              embed = Embed(title='Server Info', description='View information on a server', color=Color.gold())
              embed.add_field(name='Usage', value='`/serverinfo`', inline=False)
              embed.add_field(name='Example', value='`/serverinfo`', inline=False)
              return embed
          elif command == 'fact':
              embed = Embed(title='Fact', description='Get a random fact', color=Color.gold())
              embed.add_field(name='Usage', value='`/fact`', inline=False)
              embed.add_field(name='Example', value='`/fact`', inline=False)
              return embed
          elif command == 'question':
              embed = Embed(title='Question', description='Get a random question', color=Color.gold())
              embed.add_field(name='Usage', value='`/question`', inline=False)
              embed.add_field(name='Example', value='`/question`', inline=False)
              return embed
          elif command == 'changelog':
              embed = Embed(title='Question', description='View the changelog', color=Color.gold())
              embed.add_field(name='Usage', value='`/changelog`', inline=False)
              embed.add_field(name='Example', value='`/changelog`', inline=False)
              return embed
          elif command == 'invite':
              embed = Embed(title='Invite', description='Get invite information about nebula', color=Color.gold())
              embed.add_field(name='Usage', value='`/invite`', inline=False)
              embed.add_field(name='Example', value='`/invite`', inline=False)
              return embed
          elif command == 'suggest':
              embed = Embed(title='Suggest', description='Suggest Features', color=Color.gold())
              embed.add_field(name='Usage', value='`/suggest`', inline=False)
              embed.add_field(name='Example', value='`/suggest`', inline=False)
              return embed
          elif command == 'stats':
              embed = Embed(title='Stats', description='View Nebulas stats', color=Color.gold())
              embed.add_field(name='Usage', value='`/stats`', inline=False)
              embed.add_field(name='Example', value='`/stats`', inline=False)
              return embed
          elif command == 'start':
              embed = Embed(title='Start', description='Start your NebCoins account', color=Color.gold())
              embed.add_field(name='Usage', value='`/start`', inline=False)
              embed.add_field(name='Example', value='`/start`', inline=False)
              return embed
          elif command == 'balance':
              embed = Embed(title='Balance', description='View your NebCoins balance', color=Color.gold())
              embed.add_field(name='Usage', value='`/balance`', inline=False)
              embed.add_field(name='Example', value='`/balance`', inline=False)
              return embed
          elif command == 'farm':
              embed = Embed(title='Farm', description='View your NebCoins farm', color=Color.gold())
              embed.add_field(name='Usage', value='`/farm`', inline=False)
              embed.add_field(name='Example', value='`/farm`', inline=False)
              return embed
          elif command == 'plant':
              embed = Embed(title='Plant', description='Plant a crop', color=Color.gold())
              embed.add_field(name='Usage', value='`/plant [plant(OPTIONAL)]`', inline=False)
              embed.add_field(name='Example', value='`/plant [apple]`', inline=False)
              return embed
          elif command == 'inventory':
              embed = Embed(title='Inventory', description='View your NebCoins inventory', color=Color.gold())
              embed.add_field(name='Usage', value='`/inventory`', inline=False)
              embed.add_field(name='Example', value='`/inventory`', inline=False)
              return embed
          elif command == 'sell':
              embed = Embed(title='Inventory', description='Sell an inventory item', color=Color.gold())
              embed.add_field(name='Usage', value='`/sell [id] [quantity]`', inline=False)
              embed.add_field(name='Example', value='`/sell [1] [3]`', inline=False)
              return embed
          elif command == 'market':
              embed = Embed(title='Inventory', description='View todays market', color=Color.gold())
              embed.add_field(name='Usage', value='`/market`', inline=False)
              embed.add_field(name='Example', value='`/market`', inline=False)
              return embed
          elif command == 'work':
              embed = Embed(title='Work', description='Work for NebCoins', color=Color.gold())
              embed.add_field(name='Usage', value='`/work`', inline=False)
              embed.add_field(name='Example', value='`/work`', inline=False)
              return embed
          elif command == 'leaderboard':
              embed = Embed(title='Work', description='View the NebCoins leaderboard', color=Color.gold())
              embed.add_field(name='Usage', value='`/leaderboard`', inline=False)
              embed.add_field(name='Example', value='`/leaderboard`', inline=False)
              return embed
          elif command == 'level':
              embed = Embed(title='Level', description='View your NebCoins level', color=Color.gold())
              embed.add_field(name='Usage', value='`/level`', inline=False)
              embed.add_field(name='Example', value='`/level`', inline=False)
              return embed
          elif command == 'transfer':
              embed = Embed(title='Level', description='Transfer NebCoins to another player', color=Color.gold())
              embed.add_field(name='Usage', value='`/transfer [user] [amount]`', inline=False)
              embed.add_field(name='Example', value='`/transfer [@Nebula] [100]`', inline=False)
              return embed
          elif command == 'beg':
              embed = Embed(title='Level', description='Beg for NebCoins', color=Color.gold())
              embed.add_field(name='Usage', value='`/beg`', inline=False)
              embed.add_field(name='Example', value='`/beg`', inline=False)
              return embed
          elif command == 'journey':
              embed = Embed(title='Level', description='Go on a journey to find pets', color=Color.gold())
              embed.add_field(name='Usage', value='`/journey`', inline=False)
              embed.add_field(name='Example', value='`/journey`', inline=False)
              return embed
          elif command == 'mypets':
              embed = Embed(title='My Pets', description='View a list of your pets', color=Color.gold())
              embed.add_field(name='Usage', value='`/mypets`', inline=False)
              embed.add_field(name='Example', value='`/mypets`', inline=False)
              return embed
          elif command == 'pets':
              embed = Embed(title='Pets', description='View a list of available pets', color=Color.gold())
              embed.add_field(name='Usage', value='`/pets`', inline=False)
              embed.add_field(name='Example', value='`/pets`', inline=False)
              return embed
          else:
              embed = Embed(description=f':x: Command **{command}** not found', color=Color.red())
              return embed