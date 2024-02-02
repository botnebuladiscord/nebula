import discord
import os
import time
import topgg
import requests
import asyncio
from keepalive import keep_alive
from threading import Thread
from random import choice
from discord.ext import commands, tasks
from nebulafunctions.main.fmain import *
from discord import app_commands
from discord.ui import Button, View

class Nebula(commands.Bot):
        def __init__(self):
            intents = discord.Intents.default()
            intents.message_content = True
            intents.members = False
            intents.guild_reactions = True
            super().__init__(intents=intents, command_prefix=None)
            self.synced = False

        async def setup_hook(self):
          await self.load_extension('cogs.help')
          await self.load_extension('cogs.math')
          await self.load_extension('cogs.fun')
          await self.load_extension('cogs.moderation')
          await self.load_extension('cogs.information')
          await self.load_extension('cogs.nebcoins')
          # await self.load_extension('cogs.test')
          await client.tree.sync() #leave empty for all servers

        async def on_ready(self):
	        self.synced = True
	        global topggv
	        dbl_token = os.getenv('TOPGG')
	        topggv = topgg.DBLClient(client, dbl_token)
	        change_status.start()
	        update_stats.start()
	        print('Ready')
        
client = Nebula()

status = ['the server', '/help']
@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=choice(status)))

@tasks.loop(minutes=30)
async def update_stats():
    try:
        await topggv.post_guild_count()
        print(f"Posted server count ({topggv.guild_count}) [top.gg]")
    except:
        print(f"Fail [top.gg]")

    try:
      url = 'https://discordbots.gg/api/servers'

      data = {'count':len(client.guilds), 'client_id':'953533453100527626'}
      headers={'authorization':f'Bearer {os.getenv("DBOTS")}'}

      print(f'{requests.post(url, data, headers=headers).json()} [discordbots.gg]')
    except:
      print('Fail [discordbots.gg]')

    try:
      url = 'https://discordbotlist.com/api/v1/bots/953533453100527626/stats'

      data = {'guilds':len(client.guilds), 'users':sum(guild.member_count for guild in client.guilds)}
      headers={'Authorization':str(os.getenv("DBOTLIST"))}

      print(f'{requests.post(url, data=data, headers=headers).text} [discordbotlist.com (stats)]')
    except:
      print('Fail [discordbotlist.com (stats)]')

    try:
      cmds = await client.tree.fetch_commands()
      cmdlist = []
      for i in cmds:
        if i.options != []:
          options = []
          for j in i.options:
            if j.description != '…':
              options.append({"name":j.name, "description":j.description, "type":j.type.value, "required":j.required})
            else:
              options.append({"name":j.name, "type":j.type.value, "required":j.required})
          cmdlist.append({"name":i.name, "description":i.description, "type":i.type.value, "options":options})
        else:  
          cmdlist.append({"name":i.name, "description":i.description, "type":i.type.value})
  
      url = 'https://discordbotlist.com/api/v1/bots/953533453100527626/commands'
      headers={'Authorization':str(os.getenv("DBOTLIST"))}
  
      print(f'{requests.post(url, json=cmdlist, headers=headers).text} [discordbotlist.com (commands)]')
    except Exception as e:
      print(e)
      print('Fail [discordbotlist.com (commands)]')

@client.event
async def on_interaction(ctx):
  if ctx.type == discord.InteractionType.application_command:
    if isblacklist(ctx.user.id) != None:
      embed = discord.Embed(title='Fail', description=f'You were blacklisted for reason: **{isblacklist(ctx.user.id)}**', color=discord.Color.red())
      await ctx.response.send_message(embed=embed)

async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
	embed = discord.Embed(title='An error occurred', description='Do you want to report this error?', color=discord.Color.red())
	view = View()
	yes = Button(label='Report Error', style=discord.ButtonStyle.red, custom_id='errorreportyes')
	no = Button(label='Ignore', style=discord.ButtonStyle.blurple, custom_id='errorreportno')
	view.add_item(yes)
	view.add_item(no)
	await interaction.response.send_message(embed=embed, view=view)
	try:
		def check(payload):
			return payload.user.id == interaction.user.id
		interact = await client.wait_for('interaction', check=check, timeout=60)
		await interact.response.defer()
		yes.disabled = True
		no.disabled = True

		if interact.data['custom_id'] == 'errorreportyes':
			embed = discord.Embed(title='Error', description='```Reported```', color=discord.Color.purple())
			await interaction.edit_original_response(embed=embed, view=view)
			channel = client.get_channel(956417591176495164)
			embed = discord.Embed(title='Error Report', color=discord.Color.red())
			embed.add_field(name='Command', value=f'```{error.command.name} {error.command.parameters}```', inline=False)
			embed.add_field(name='Error', value=f'```{str(error.original)}```', inline=False)
			embed.add_field(name='Args', value=f'```{str(error.args)}```', inline=False)
			await channel.send(embed=embed)
		else:
			embed = discord.Embed(title='Error', description='```Ignored```', color=discord.Color.purple())
			await interaction.edit_original_response(embed=embed, view=view)

	except asyncio.TimeoutError:
	  yes.disabled = True
	  no.disabled = True
	  embed = discord.Embed(title='Error', description='```Ignored```', color=discord.Color.red())
	  await interaction.edit_original_response(embed=embed, view=view)



client.tree.on_error = on_tree_error

@client.event
async def on_error(error, message):
  if str(error) == 'on_message':
    pass

t = os.environ.get('TOKEN')
keep_alive()
while True:
	try:
		client.run(t)
		time.sleep(5)
		break
	except:
		print('Fail, Trying again in 5 minute')
		time.sleep(60*5)
# while True:
#   print('TRYING...')
#   try:
#     if client.is_ws_ratelimited():
#       pass
#     else:
#       client.run(t)
#       print('SUCCESS!')
#     break
#   except Exception as e:
#     print(e)
#     print('FAIL, Trying again in 5 minutes')
#     time.sleep(60*5)
