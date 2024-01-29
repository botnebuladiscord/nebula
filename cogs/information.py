import discord
from discord import app_commands
from discord.ext import commands
from better_profanity import profanity
from datetime import datetime
from random import shuffle
from discord.ui import View, Button
import asyncio
from nebulafunctions.information.finformation import *

class information(commands.Cog):
	def __init__(self, bot: commands.bot) -> None:
		self.bot = bot

	@app_commands.command(name='wikipedia', description='Search wikipedia')
	async def wikipedia(self, ctx, query: str):
		query = query.lower()
		if profanity.contains_profanity(query):
			await ctx.response.send_message('This query contains profanity', ephemeral=True)
			return
		title, description = fwikipedia(query)
		if description == None:
			await ctx.response.send_message(f'Could not find any result for **{query}**', ephemeral=True)
			return
		embed = discord.Embed(title=title, description=description, color=discord.Color.orange())
		await ctx.response.send_message(embed=embed)

	@app_commands.command(name='weather', description='Find the weather of a location')
	async def weather(self, ctx, query: str):
		await ctx.response.defer()
		a = fweather(query)
		if a != 404:
			embed = discord.Embed(title=query.capitalize(), color=discord.Color.purple())
			file = discord.File('assets/weather/weather.png', filename='weather.png')
			weather = 'attachment://weather.png'
			embed.set_image(url=weather)
			await ctx.followup.send(embed=embed, file=file)
		else:
			await ctx.followup.send(f'Could not find weather for **{query}**')

	@app_commands.command(name='serverinfo', description='Find information on the server')
	async def serverinfo(self, ctx):
		sn = ctx.guild.name
		asset = ctx.guild.icon
		id = str(ctx.guild.id)
		memberCount = str(ctx.guild.member_count)
		day = ctx.guild.created_at.strftime('%d')
		year = ctx.guild.created_at.strftime('%Y')
		month = ctx.guild.created_at.strftime('%m')
		hour = ctx.guild.created_at.strftime('%H')
		minute = ctx.guild.created_at.strftime('%M')
		created = datetime(int(year), int(month), int(day), int(hour), int(minute)).timestamp() 
		created = round(created)
		created = f'<t:{created}:R>'
		level = str(ctx.guild.verification_level).upper()
		if level == 'LOW':
			level = ':red_circle: '+level
		elif level == 'MEDIUM':
			level = ':orange_circle: '+level
		elif level == 'HIGH':
			level = ':yellow_circle: '+level
		elif level == 'HIGHEST':
			level = ':green_circle: '+level
		text_channels = str(len(ctx.guild.text_channels))
		voice_channels = str(len(ctx.guild.voice_channels))
		stage_channels = str(len(ctx.guild.stage_channels))
		forums = str(len(ctx.guild.forums))
		categories = str(len(ctx.guild.categories))
		nr = str(len(ctx.guild.roles))
		hr = ctx.guild.roles[len(ctx.guild.roles) - 1]
		a = f':id:**:** `{id}`\n\n:bust_in_silhouette: **Member Count:** `{memberCount}`\n\n:calendar_spiral: **Created:** {created}\n\n:white_check_mark: **Verification Level:** {level}\n\n:1234: **Role Count:** `{nr}`\n\n:arrow_double_up: **Highest Role:** {hr.mention}'
		embed = discord.Embed(title=sn, description=a, color=discord.Color.green())
		embed.add_field(name='Channels', value=f':file_folder: **Categories:** `{categories}`\n:hash: **Text Channels:** `{text_channels}`\n:sound: **Voice Channels:** `{voice_channels}`\n:microphone2: **Stage Channels:** `{stage_channels}`\n:speech_balloon: **Forum Channels:** `{forums}`')
		embed.set_thumbnail(url=asset)
		await ctx.response.send_message(embed=embed)

	@app_commands.command(name='userinfo', description='Find information on a user')
	async def userinfo(self, ctx, user: discord.Member=None):
		if user == None:
			user = ctx.user
		un = user.name
		asset = user.avatar
		id = str(user.id)
		created = datetime(int(user.created_at.strftime('%Y')), int(user.created_at.strftime('%m')), int(user.created_at.strftime('%d')), int(user.created_at.strftime('%H')), int(user.created_at.strftime('%M'))).timestamp() 
		created = round(created)
		created = f'<t:{created}:R>'
		joined = datetime(int(user.joined_at.strftime('%Y')), int(user.joined_at.strftime('%m')), int(user.joined_at.strftime('%d')), int(user.joined_at.strftime('%H')), int(user.joined_at.strftime('%M'))).timestamp() 
		joined = round(joined)
		joined = f'<t:{joined}:R>'
		roles = [role for role in user.roles]
		roles.pop(0)
		nr = len(roles)
		if user.bot == False:
			bot = 'No'
		else:
			bot = 'Yes'
		a = f':id:**:** `{id}`\n\n:robot: **Bot:** {bot}\n\n:calendar_spiral: **Created:** {created}\n\n:inbox_tray: **Joined:** {joined}\n\n:1234: **Role Count:** `{nr}`\n\n:arrow_double_up: **Highest Role:** {user.top_role.mention}\n\n:bust_in_silhouette: **Roles:** {" ".join([role.mention for role in roles])}'
		embed = discord.Embed(title=un, description=a, color=discord.Color.green())
		embed.set_thumbnail(url=asset)
		await ctx.response.send_message(embed=embed)

	@app_commands.command(name='fact', description='Get a random fact')
	async def fact(self, ctx):
		fact = get_fact()
		fact = fact.replace('`', "'")
		embed = discord.Embed(title='Did You Know?', description=fact, color=discord.Color.purple())
		await ctx.response.send_message(embed=embed)

	@app_commands.command(name='question', description='Get a random question')
	async def question(self, ctx):
		q, i, c, d = question()
		embed = discord.Embed(title='Question', description=q, color=discord.Color.purple())
		view = View()
		options = []
		ii = 0
		for j in i:
			ii += 1
			button = Button(label=j, style=discord.ButtonStyle.blurple, custom_id=f'questionincorrect{ii}')
			options.append(button)
		button = Button(label=c, style=discord.ButtonStyle.blurple, custom_id='questioncorrect')
		options.append(button)
		shuffle(options)
		for h in options:
			view.add_item(h)
		await ctx.response.send_message(embed=embed, view=view)
		for h in options:
			h.disabled = True
			if h.custom_id == 'questioncorrect':
				h.style = discord.ButtonStyle.green
			else:
				h.style = discord.ButtonStyle.red
		try:
			def check(payload):
				return payload.user.id == ctx.user.id
			interaction = await self.bot.wait_for('interaction', check=check, timeout=30)
			if interaction.data['custom_id'] == 'questioncorrect':
				embed.title = '[Correct] '+embed.title
				embed.color = discord.Color.green()
			else:
				embed.title = '[Incorrect] '+embed.title
				embed.color = discord.Color.red()
			await ctx.edit_original_response(embed=embed, view=view)
			await interaction.response.defer()
		except asyncio.TimeoutError:
			embed.color = discord.Color.blue()
			embed.title = '[Time Out] '+embed.title
			await ctx.edit_original_response(embed=embed, view=view)

	@app_commands.command(name='invite', description='Get invite information about nebula')
	async def invite(self, ctx):
		embed = discord.Embed(title='Invite', description=f'[Invite Nebula](https://discord.com/api/oauth2/authorize?client_id=953533453100527626&permissions=1247621410038&scope=bot)\n[Join the support server](https://discord.gg/CxtY6rTnr4)', color=discord.Color.purple())
		await ctx.response.send_message(embed=embed)

	@app_commands.command(name='suggest', description='Suggest Features')
	async def suggest(self, ctx):
		embed = discord.Embed(title='Suggest', description=f'[Suggest](https://hi7rxb1s0wz.typeform.com/to/ftHD17Mz)', color=discord.Color.purple())
		await ctx.response.send_message(embed=embed)

	@app_commands.command(name='stats', description='View Nebulas stats')
	async def suggest(self, ctx):
		servercount = len(self.bot.guilds)
		membercount = sum(guild.member_count for guild in self.bot.guilds)
		avg = round(membercount/servercount)
		embed = discord.Embed(title='Stats', color=discord.Color.purple())
		embed.add_field(name='Servers', value=f'`{servercount}`', inline=False)
		embed.add_field(name='Members', value=f'`{membercount}`', inline=False)
		embed.add_field(name='Average members per server', value=f'`{avg}`', inline=False)
		embed.add_field(name='Library', value='`discord.py`', inline=False)
		me = await self.bot.fetch_user(811893594716766210)
		embed.add_field(name='Creator', value=f'`{me.name}`', inline=False)
		embed.add_field(name='Invite', value='[:link: Invite](https://discord.com/api/oauth2/authorize?client_id=953533453100527626&permissions=1247621410038&scope=bot)\n[:link: Support](https://discord.gg/CxtY6rTnr4)', inline=False)
		await ctx.response.send_message(embed=embed)

	@app_commands.command(name='changelog', description='View the changelog')
	async def changelog(self, ctx):
		newcommands = '''
		`/start`
		`/balance`
		`/farm`
		`/plant`
		`/inventory`
		`/sell`
		`/market`
		`/work`
		`/leaderboard`
		`/level`
		`/transfer`
		`/beg`
		`/journey`
		`/mypets`
		`/pets`'''

		bugfixes = '''
		Fixed stats update on top.gg and discordbotlist.com'''

		extraadds = '''
		Added a bug report system'''

		embed = discord.Embed(title='Changelog', description='**Version:** `4.2`', color=discord.Color.purple())
		embed.add_field(name='New Commands', value=newcommands, inline=False)
		embed.add_field(name='Extra Adds', value=extraadds, inline=False)
		embed.add_field(name='Bug Fixes', value=bugfixes, inline=False)
		await ctx.response.send_message(embed=embed)

async def setup(bot:commands.Bot) -> None:
		await bot.add_cog(information(bot), guilds = []) #leave empty for all servers