import discord
from datetime import timedelta, datetime, timezone
from discord import app_commands
from random import choice
from discord.ext import commands, tasks
from nebulafunctions.moderation.fmoderation import *
from nebulafunctions.storage.fstorage import *


@tasks.loop(seconds=1)
async def pollloop(bot):
    try:
        data = getdata_poll()
        for i in data.keys():
            try:
                et = data[i]['et']
                if et == None:
                    continue
                a = datetime.fromtimestamp(int(et), timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                if a <= datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'):
                    c = data[i]['ch']
                    c = await bot.fetch_channel(c)
                    m = await c.fetch_message(i)
                    a = 0
                    b = ''
                    ii = 0
                    num = data[i]['votes']
                    key = list(num.keys())
                    e = data[i]['votes']
                    for j in e:
                        ii += 1
                        if num[str(j)] != 0:
                            if num[str(j)] > a:
                                a = num[str(j)]
                                b = key[ii-1]
                            elif num[str(j)] == a:
                                a = str(a) + ', ' + str(num[str(j)])
                                b = str(b) + ', ' + str(key[ii-1])
                    user = data[i]['a']
                    guild = data[i]['guild']
                    guild = bot.get_guild(guild)
                    user = await guild.fetch_member(user)
                    question = data[i]['q']
                    if a == 0:
                        embed = discord.Embed(description=f'{question}\n\n**Result:** Nobody Voted\n\n🔒 Voting has been locked', color=discord.Color.red())
                        name = user.nick
                        if name == None:
                            name = user.name
                        embed.set_author(name=name, icon_url=user.avatar.url)
                        await m.edit(embed=embed)
                    else:
                        embed = discord.Embed(description=f'{question}\n\n**Result:** {str(b)} won with {str(a)} vote(s)\n\n🔒 Voting has been locked', color=discord.Color.green())
                        name = user.nick
                        if name == None:
                            name = user.name
                        embed.set_author(name=name, icon_url=user.avatar.url)
                        await m.edit(embed=embed)
                    setcomplete(m.id)
            except:
                pass
    except:
        pass
    
@tasks.loop(seconds=1)
async def giveawayloop(bot):
    with open('storage/giveaway.json') as file:
        data = json.load(file)
    for i in data.keys():
        try:
            a = datetime.fromtimestamp(int(getgtime(i))).strftime('%Y-%m-%d %H:%M:%S')
            if a <= datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'):
                mes = i
                prize = getgprize(i)
                guild = await bot.fetch_guild(getgguild(i))
                author = await guild.fetch_member(int(getgauthor(i)))
                channel = bot.get_channel(getgchannel(i))
                mes = await channel.fetch_message(mes)
                usersasync = mes.reactions[0].users()
                users = []
                async for j in usersasync:
                    users.append(j.id)
                # discord.Message.reactions[0].users()
                try:
                    users.pop(users.index(bot.user.id))
                except:
                    pass
                if len(users) != 0:
                    winner = choice(users)
                    winner = await bot.fetch_user(winner)
                else:
                    winner = 'NOBODY'
                t = f'<t:{int(getgtime(i))}:R>'
                if winner != 'NOBODY':    
                    embed2 = discord.Embed(title='Giveaway', description=f'**{prize}**\nWon by {winner.mention} (`{str(winner)}`) :popcorn: :tada:\n**Ended:** {t}\n\n**Cleared all reactions**', color = discord.Color.gold())
                else:
                    embed2 = discord.Embed(title='Giveaway', description=f'**{prize}**\nNobody Participated :frowning:\n**Ended:** {t}\n\n**Cleared all reactions**', color = discord.Color.gold())
                name = author.nick
                if name == None:
                    name = author.name
                embed2.set_author(name=name, icon_url=author.avatar.url)
                await mes.edit(embed=embed2)
                e = '🎉'
                await mes.clear_reaction(e)
                await author.send(embed=discord.Embed(title=f'**Giveaway for {prize} has been won**',description=f'**Hello,**\n\nYour giveaway for ****{prize}**** in **{guild.name}** has been won by `{winner}`', color = discord.Color.gold()))
                with open('storage/giveaway.json') as file:
                    data = json.load(file)
                data.pop(i)
                with open('storage/giveaway.json', 'w') as file:
                    json.dump(data, file)
        except Exception as e:
            print(e)
    
@tasks.loop(seconds=1)
async def tempbanloop(bot):
    with open('storage/tempban.json') as file:
        data = json.load(file)
    for i in data.keys():
        time = checktempban(i)
        now = datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
        if now <= datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'):
            guild = gettempbanguild(str(i))
            guild = await bot.fetch_guild(guild)
            user = await bot.fetch_user(int(i))
            await guild.unban(user)
            deletetempban(i)

class moderation(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        self.removed = []
        pollloop.start(bot)
        tempbanloop.start(bot)
        giveawayloop.start(bot)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        data = getdata_poll()
        member = payload.member
        mid = payload.message_id
        channel_id = payload.channel_id
        if data[str(mid)] == 'OVER':
            channel = self.bot.get_channel(channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, member)
            self.removed.append((member.id, payload.guild_id))
            return
        a = data[str(mid)]['voted']
        if a == 0:
            return
        if member.id in a:
            channel = self.bot.get_channel(channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, member)
            self.removed.append((member.id, payload.guild_id))
        else:
            a.append(member.id)
            votes = data[str(mid)]['votes']
            for i in votes.keys():
                if str(i) == str(payload.emoji):
                    votes[str(i)] += 1
            pollupdatevotedvotes(str(mid), a, votes)
            
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        data = getdata_poll()
        member = await self.bot.fetch_user(payload.user_id)
        mid = payload.message_id
        removedcheckii = 0
        for i in self.removed:
            if member.id == i[0] and payload.guild_id == i[1]:
                self.removed.pop(removedcheckii)
                return
            removedcheckii += 1
        # channel_id = payload.channel_id
        if data[str(mid)] == 'OVER':
            return
        a = data[str(mid)]['voted']
        if a == 0:
            return
        if member.id in a:
            a.pop(a.index(member.id))
            votes = data[str(mid)]['votes']
            for i in votes.keys():
                if str(i) == str(payload.emoji):
                    votes[str(i)] -= 1
            pollupdatevotedvotes(str(mid), a, votes)
        
    @app_commands.command(name='kick', description='Kick a user')
    async def kick(self, ctx, user: discord.Member, reason: str=None):
        if ctx.user.guild_permissions.kick_members != True:
            await ctx.response.send_message('You need the permission: **Kick Members** to use this command', ephemeral=True)
            return
        embed = discord.Embed(title='Kicked', description=f'**Server:** {ctx.guild}\n**Moderator:** `{ctx.user.name}`\n**Reason:** {reason}', color=discord.Color.red())
        await user.send(embed=embed)
        await user.kick(reason=reason)
        embed = discord.Embed(title='User Kicked', description=f'**User:** `{user.name}`\n**Moderator:** {ctx.user.mention}\n**Reason:** {reason}', color=discord.Color.red())
        await ctx.response.send_message(embed=embed)
    
    @app_commands.command(name='ban', description='Ban a user')
    @app_commands.choices(delete_messages=[
            app_commands.Choice(name="Dont Delete", value="0"),
            app_commands.Choice(name="Previous Hour", value="1"),
            app_commands.Choice(name="Previous 6 Hours", value="6"),
            app_commands.Choice(name="Previous 12 Hours", value="12"),
            app_commands.Choice(name="Previous 24 Hours", value="24"),
            app_commands.Choice(name="Previous 3 Days", value="3d"),
            app_commands.Choice(name="Previous 7 Days", value="7d")
        ])
    async def ban(self, ctx, user: discord.Member, delete_messages: app_commands.Choice[str], reason: str=None):
        if ctx.user.guild_permissions.ban_members != True:
            await ctx.response.send_message('You need the permission: **Ban Members** to use this command', ephemeral=True)
            return
        embed = discord.Embed(title='Banned', description=f'**Server:** {ctx.guild}\n**Moderator:** `{ctx.user.name}`\n**Reason:** {reason}', color=discord.Color.red())
        await user.send(embed=embed)
        if delete_messages.value != '0':
            if delete_messages.value == '3d':
                await user.ban(reason=reason, delete_message_days=3)
            elif delete_messages.value == '7d':
                await user.ban(reason=reason, delete_message_days=3)
            else:
                await user.ban(reason=reason, delete_message_seconds=int(delete_messages.value)*60*60)
        else:
            await user.ban(reason=reason)
        embed = discord.Embed(title='User Banned', description=f'**User:** `{user.name}`\n**Moderator:** {ctx.user.mention}\n**Reason:** {reason}', color=discord.Color.red())
        await ctx.response.send_message(embed=embed)
    
    @app_commands.command(name='slowmode', description='Set the slowmode')
    async def slowmode(self, ctx, seconds: int):
        if ctx.user.guild_permissions.manage_channels != True:
            await ctx.response.send_message('You need the permission: **Manage Channels** to use this command', ephemeral=True)
            return
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            embed = discord.Embed(title='Updated Slowmode', description=f'Set slowmode for {ctx.channel.mention} to `{seconds}` seconds', color=discord.Color.green())
            await ctx.response.send_message(embed=embed)
        except:
            await ctx.response.send_message(f'Cannot set slowmode to `{seconds}` seconds', ephemeral=True)    

    @app_commands.command(name='create', description='Create a channel')
    async def create(self, ctx, name: str, category: discord.CategoryChannel=None):
        if ctx.user.guild_permissions.manage_channels != True:
            await ctx.response.send_message('You need the permission: **Manage Channels** to use this command', ephemeral=True)
            return
        ch = await ctx.guild.create_text_channel(name=name, category=category)
        embed = discord.Embed(title='Channel Created', description=f'**Channel:** {ch.mention} [{ch.name}]\n**Moderator:** {ctx.user.mention}', color=discord.Color.green())
        await ctx.response.send_message(embed=embed)

    @app_commands.command(name='delete', description='Delete a channel')
    async def delete(self, ctx, channel: discord.TextChannel):
        if ctx.user.guild_permissions.manage_channels != True:
            await ctx.response.send_message('You need the permission: **Manage Channels** to use this command', ephemeral=True)
            return
        ch = channel.name
        await channel.delete()
        embed = discord.Embed(title='Channel Deleted', description=f'**Name:** {ch}\n**Moderator:** {ctx.user.mention}', color=discord.Color.red())
        await ctx.response.send_message(embed=embed)
    
    @app_commands.command(name='poll', description='Create a poll')
    @app_commands.describe(time = 's: seconds, m: minutes, h: hours, d: days. Example: 2h', question = '[nl] for newline')
    async def pollc(self, ctx, channel: discord.TextChannel, question: str, time: str, emojis: str):
        for i in list(channel.overwrites.keys()):
            if i in ctx.user.roles:
                if channel.overwrites[i].send_messages:
                    break
        else:
            if ctx.user.guild_permissions.manage_channels != True:
                await ctx.response.send_message(f'You need to be able to send messages in {channel.mention} to create a poll in that channel', ephemeral=True)
                return
        question = question.replace('[nl]', '\n')
        def convert_time(time):
            pos = ['s', 'm', 'h', 'd']
            time_dict = {'s':1, 'm':60, 'h':3600, 'd':3600*24}
            unit = time[-1]
            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2
            return val * time_dict[unit]
        
        time = convert_time(time)
        time2 = timedelta(0, time)
        time2 = datetime.now(timezone.utc) + time2
        day = time2.strftime('%d')
        year = time2.strftime('%Y')
        month = time2.strftime('%m')
        hour = time2.strftime('%H')
        minute = time2.strftime('%M')
        epoch_time = datetime(int(year), int(month), int(day), int(hour), int(minute), 0, 0, timezone.utc).timestamp() 

        epoch_time = round(epoch_time)
        th = f'<t:{epoch_time}:R>'
        embed = discord.Embed(description=f'{question}\n\nGets over {str(th)}', color=discord.Color.purple())
        name = ctx.user.nick
        if name == None:
            name = ctx.user.name
        embed.set_author(name=name, icon_url=ctx.user.avatar.url)
        m = await channel.send(embed=embed)
        embed = discord.Embed(description=f':white_check_mark: `Created a poll in` {channel.mention}', color=discord.Color.green())
        await ctx.response.send_message(embed=embed, ephemeral=True)
            
        num = {}
        ee = []
        for i in emojis:
            i = i.replace(' ', '')
            if i != None and i != '':
                try:
                    await m.add_reaction(i)
                    num[str(i)]=0
                    ee.append(i)
                except:
                    pass
        emojis = ee
        poll(m.id, time, [], num, epoch_time, ctx.user.id, question, channel.id, ctx.guild.id)
    
    @app_commands.command(name='announce', description='Create an announcement')
    @app_commands.describe(embedcolor = 'Hex Code', message = '[nl] for newline')
    async def announce(self, ctx, channel: discord.TextChannel, title: str, message: str, embedcolor: str=None):
        try:
            color = discord.Color.from_str(embedcolor)
        except:
            color = discord.Color.gold()
        for i in list(channel.overwrites.keys()):
            if i in ctx.user.roles:
                if channel.overwrites[i].send_messages:
                    break
        else:
            if ctx.user.guild_permissions.manage_channels != True:
                await ctx.response.send_message(f'You need to be able to send messages in {channel.mention} to announce in that channel', ephemeral=True)
                return
        message = message.replace('[nl]', '\n')
        embed = discord.Embed(title=title, description=message, color=color)
        name = ctx.user.nick
        if name == None:
            name = ctx.user.name
        embed.set_author(name=name, icon_url=ctx.user.avatar.url)
        await channel.send(embed=embed)
        embed = discord.Embed(description=f':white_check_mark: `Created a announcement in` {channel.mention}', color=discord.Color.green())
        await ctx.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name='lock', description='Lock a channel')
    async def lock(self, ctx, channel: discord.TextChannel, lock_for: discord.Role, reason: str=None):
        if ctx.user.guild_permissions.manage_channels != True:
            await ctx.response.send_message('You need the permission: **Manage Channels** to use this command', ephemeral=True)
            return
        embed = discord.Embed(title='Channel Locked', description=f'**Locked For:** {lock_for.mention}\n**Moderator:** {ctx.user.mention}\n**Reason:** {reason}', color=discord.Color.red())
        await channel.send(embed=embed)
        if lock_for not in channel.overwrites:
            overwrites = {
            lock_for: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
        elif channel.overwrites[lock_for].send_messages == True or channel.overwrites[lock_for].send_messages == None:
            overwrites = channel.overwrites[lock_for]
            overwrites.send_messages = False
            await channel.set_permissions(lock_for, overwrite=overwrites, reason=reason)
        embed = discord.Embed(description=f':white_check_mark: Locked {channel.mention}', color=discord.Color.green())
        await ctx.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name='unlock', description='Unlock a channel')
    async def unlock(self, ctx, channel: discord.TextChannel, unlock_for: discord.Role, reason: str=None):
        if ctx.user.guild_permissions.manage_channels != True:
            await ctx.response.send_message('You need the permission: **Manage Channels** to use this command', ephemeral=True)
            return
        embed = discord.Embed(title='Channel Unlocked', description=f'**Unlocked For:** {unlock_for.mention}\n**Moderator:** {ctx.user.mention}\n**Reason:** {reason}', color=discord.Color.green())
        await channel.send(embed=embed)
        if unlock_for not in channel.overwrites:
            overwrites = {
            unlock_for: discord.PermissionOverwrite(send_messages=True)
            }
            await channel.edit(overwrites=overwrites)
        elif channel.overwrites[unlock_for].send_messages == False or channel.overwrites[unlock_for].send_messages == None:
            overwrites = channel.overwrites[unlock_for]
            overwrites.send_messages = True
            await channel.set_permissions(unlock_for, overwrite=overwrites, reason=reason)
        embed = discord.Embed(description=f':white_check_mark: Unlocked {channel.mention}', color=discord.Color.green())
        await ctx.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name='tempban', description='Temporary ban a user')
    @app_commands.describe(time = 's: seconds, m: minutes, h: hours, d: days. Example: 2h')
    @app_commands.choices(delete_messages=[
            app_commands.Choice(name="Dont Delete", value="0"),
            app_commands.Choice(name="Previous Hour", value="1"),
            app_commands.Choice(name="Previous 6 Hours", value="6"),
            app_commands.Choice(name="Previous 12 Hours", value="12"),
            app_commands.Choice(name="Previous 24 Hours", value="24"),
            app_commands.Choice(name="Previous 3 Days", value="3d"),
            app_commands.Choice(name="Previous 7 Days", value="7d")
        ])
    async def tempban(self, ctx, user: discord.Member, delete_messages: app_commands.Choice[str], time: str, reason: str=None):
        if ctx.user.guild_permissions.ban_members != True:
            await ctx.response.send_message('You need the permission: **Ban Members** to use this command', ephemeral=True)
            return
        embed = discord.Embed(title='Temporary Banned', description=f'**Server:** {ctx.guild}\n**Moderator:** `{ctx.user.name}`\n**Time:** {time}\n**Reason:** {reason}', color=discord.Color.red())
        await user.send(embed=embed)
        if delete_messages.value != '0':
            if delete_messages.value == '3d':
                await user.ban(reason=reason, delete_message_days=3)
            elif delete_messages.value == '7d':
                await user.ban(reason=reason, delete_message_days=3)
            else:
                await user.ban(reason=reason, delete_message_seconds=int(delete_messages.value)*60*60)
        else:
            await user.ban(reason=reason)
        embed = discord.Embed(title='User Temporary Banned', description=f'**User:** `{user.name}`\n**Moderator:** {ctx.user.mention}\n**Time:** {time}\n**Reason:** {reason}', color=discord.Color.red())
        await ctx.response.send_message(embed=embed)
        addtempban(user.id, time, ctx.guild.id)
        
    @app_commands.command(name='unban', description='Unban a user')
    async def unban(self, ctx, userid: str, reason: str=None):
        userid = int(userid)
        if ctx.user.guild_permissions.ban_members != True:
            await ctx.response.send_message('You need the permission: **Ban Members** to use this command', ephemeral=True)
            return
        user = await self.bot.fetch_user(userid)
        await ctx.guild.unban(user, reason=reason)
        embed = discord.Embed(title='User Unbanned', description=f'**User:** `{user.name}`\n**Moderator:** {ctx.user.mention}\n**Reason:** {reason}', color=discord.Color.green())
        await ctx.response.send_message(embed=embed)
        
    @app_commands.command(name='giveaway', description='Start a giveaway')
    @app_commands.describe(time = 's: seconds, m: minutes, h: hours, d: days. Example: 2h')
    async def giveaway(self, ctx, channel: discord.TextChannel, prize: str, time: str):
        for i in list(channel.overwrites.keys()):
            if i in ctx.user.roles:
                if channel.overwrites[i].send_messages:
                    break
        else:
            if ctx.user.guild_permissions.manage_channels != True:
                await ctx.response.send_message(f'You need to be able to send messages in {channel.mention} to create a giveaway in that channel', ephemeral=True)
                return
        time = convert_time(time)
        time2 = timedelta(0, time)
        time2 = datetime.now(timezone.utc) + time2
        day = time2.strftime('%d')
        year = time2.strftime('%Y')
        month = time2.strftime('%m')
        hour = time2.strftime('%H')
        minute = time2.strftime('%M')
        epoch_time = datetime(int(year), int(month), int(day), int(hour), int(minute)).timestamp() 

        epoch_time = round(epoch_time)
        t = f'<t:{epoch_time}:R>'
        embed = discord.Embed(title='**Giveaway**', description=f'**{prize}**\n\n**Ends:** {t}\n\n**React with :tada: to participate**', color = discord.Color.gold())
        name = ctx.user.nick
        if name == None:
            name = ctx.user.name
        embed.set_author(name=name, icon_url=ctx.user.avatar.url)
        m = await channel.send(embed=embed)
        await m.add_reaction('🎉')
        embed = discord.Embed(description=f':white_check_mark: Created giveaway in {channel.mention}', color=discord.Color.green())
        await ctx.response.send_message(embed=embed, ephemeral=True)
        giveawayf(m.id, epoch_time, prize, ctx.user.id, channel.id, ctx.guild.id)
    
    @app_commands.command(name='warn', description='Warn a user')
    async def warn(self, ctx, user: discord.User, reason: str):
        if ctx.user.guild_permissions.manage_messages != True:
            await ctx.response.send_message('You need the permission: **Manage Messages** to use this command', ephemeral=True)
            return
        warnings, warnid = addwarn(user.id, reason, ctx.user.id, ctx.guild.id)
        embed = discord.Embed(description=f':white_check_mark: Warned {user.mention} (`{user.id}`) for **{reason}**', color=discord.Color.green())
        embed.set_footer(text=f'Warn ID: {warnid} || {user.name} now has {warnings} warnings')
        await ctx.response.send_message(embed=embed)
    
    @app_commands.command(name='warnings', description='View warnings for a user')
    async def warnings(self, ctx, user: discord.User=None):
        if user == None:
            user = ctx.user
        description = ''
        warns = getwarns(user.id, ctx.guild.id)
        if warns == None:
            embed = discord.Embed(title='Warnings', description='No warnings', color=discord.Color.purple())
            await ctx.response.send_message(embed=embed)
            return
        for i in warns:
            description = description + f'**{i["reason"]}**\n```{i["id"]}```\n'
        embed = discord.Embed(title='Warnings', description=description, color=discord.Color.purple())
        await ctx.response.send_message(embed=embed)
    
    @app_commands.command(name='delwarn', description='Delete a users warning')
    async def delwarn(self, ctx, warnid: str):
        if ctx.user.guild_permissions.manage_messages != True:
            await ctx.response.send_message('You need the permission: **Manage Messages** to use this command', ephemeral=True)
            return
        warnings, user = delwarn(warnid, ctx.guild.id)
        user = await self.bot.fetch_user(user)
        embed = discord.Embed(description=f':white_check_mark: Deleted warn (`{warnid}`) for {user.mention} (`{user.id}`)', color=discord.Color.green())
        embed.set_footer(text=f'{user.name} now has {warnings} warnings')
        await ctx.response.send_message(embed=embed)

        
async def setup(bot:commands.Bot) -> None:
        await bot.add_cog(moderation(bot), guilds = []) #leave empty for all servers
