import discord
from discord import app_commands
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from asyncio import sleep, TimeoutError
from discord.ui import View, Button
from random import choice
from nebulafunctions.nebcoins.fnebcoins import *
from nebulafunctions.cooldowns.fcooldowns import *
from nebulafunctions.storage.fstorage import *

@tasks.loop(seconds=86400)
async def mktprice():
    global mkt
    mkt = []
    for i in plants:
        cost = price[plants.index(i)]
        cost = cost + 1
        endcost = cost + cost
        finalcost = choice(list(range(cost, endcost, 1)))
        mkt.append(finalcost)

class nebcoins(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        mktprice.start()

    global plants, price, pets, pprice, petlevels, pgrowth, lvl
    plants = ['apple', 'banana', 'lemon', 'grapes', 'pineapple', 'watermelon', 'pear', 'mango', 'strawberry', 'melon', 'cherries', 'blueberries', 'kiwi', 'tomato', 'coconut', 'corn', 'onion', 'garlic', 'mushroom', 'potato', 'carrot', 'eggplant', 'cucumber', 'bell_pepper', 'broccoli', 'avocado']
    price = [100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1100,1200,1300,1400,1500,1600,1700]
    pgrowth = [60*5, 600, 60*15, 60*20, 60*25, 60*30, 60*35, 60*40, 60*45, 60*50, 60*60, 60*65, 60*70, 60*75, 60*80, 60*90, 60*95, 6000, 60*105, 60*110, 60*115, 60*120, 60*125, 60*130, 60*135, 60*140]
    pets = ['butterfly', 'ladybug', 'dog', 'cat', 'pig', 'chipmunk', 'hamster', 'swan', 'rabbit', 'peacock', 'frog', 'dolphin', 'horse', 'octopus', 'monkey', 'hedgehog', 'beaver', 'elephant', 'giraffe', 'rhino', 'panda', 'flamingo', 'llama', 'badger', 'sloth', 'raccoon', 'zebra', 'polar bear', 'penguin', 'orangutan']
    pprice = [50, 75, 100, 150, 175, 175, 200, 250, 300, 350, 400, 450, 500, 500, 550, 600, 600, 650, 675, 700, 750, 800, 850, 900, 950, 950, 975, 1000, 1000, 1000]
    petlevels = [9, 15]
    lvl = [12,25]

    @app_commands.command(name='start', description='Start a NebCoins account')
    async def start(self, ctx):
        a = getmoney(int(ctx.user.id))
        if a == None:
            startf(int(ctx.user.id))
            embed = discord.Embed(title='**Account Created**', description=f'Welcome {ctx.user.mention}!\n\nYour account has been created!\n\nYou now have 100 <:nebcoin:936570857684336640>', color = discord.Color.green())
            await ctx.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title='You already have a NebCoins account!', description='Do `/balance` to find your balance', color = discord.Color.red())
            await ctx.response.send_message(embed=embed)

    @app_commands.command(name='balance', description='View your NebCoins balance')
    async def balance(self, ctx):
        balance = getmoney(str(ctx.user.id))
        if balance != None:
            embed = discord.Embed(title='Balance', description=f'You have {balance} <:nebcoin:936570857684336640>', color = discord.Color.gold())
            await ctx.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title='You do not have a NebCoins account', description='Use `/start` to create one!', color = discord.Color.gold())
            await ctx.response.send_message(embed=embed)  

    @app_commands.command(name='farm', description='View your farm')
    async def farm(self, ctx):
        await ctx.response.send_message(':tractor: Checking for harvests...')
        money, time, farm, inv = getfarmdata(str(ctx.user.id))
        if money != None:
            # time = gettime(ctx.user.id)
            gtime = time
            # farm = getfarm(ctx.user.id)
            # inv = getinv(ctx.user.id)
            now = datetime.now()
            now = datetime.strptime(str(now).replace(' ', ''), '%Y-%m-%d%H:%M:%S.%f')
            embeds = discord.Embed(title='Your Farm', color = discord.Color.gold())
            emoji = ':brown_square::brown_square::brown_square::brown_square:'
            updatedata = False
            jj = -1
            for i in farm:
                jj += 1
                try:
                    t = datetime.strptime(time[jj], '%Y-%m-%d %H:%M:%S.%f')
                    if now > t:
                        if i == ':brown_square::brown_square::brown_square::brown_square:':
                            continue
                        land = farm.index(i)
                        embeds.add_field(name = f'**Land {land+1}**', value=f'{i} Harvested and placed in inventory!', inline = False)
                        p = str(farm[jj]).split(':')[1]
                        if inv == None:
                            inv = []
                        if inv == [" "]:
                            inv = []
                        inv.append(f':{p}:')
                        ufarm = []
                        pl = False
                        for j in farm:
                            if i == j and pl == False:
                                pos = farm.index(j)
                                ufarm.append(emoji)
                                pl = True
                            else:
                                ufarm.append(j)
                        farm = ufarm
                        stime = []
                        for i in range(len(time)):
                            if pos == i:
                                stime.append(None)
                            else:
                                stime.append(time[i])
                        time = stime
                        updatedata = True
                        # Thread(target=updateinv, args=(ctx.author.id, inv)).start()
                        # Thread(target=updatefarm, args=(ctx.author.id, farm)).start()
                        # Thread(target=updatetime, args=(ctx.author.id, pos, None)).start()
                except:
                    pass
            ii = 0
            for i in farm:
                ii+=1
                embeds.add_field(name = f'**Land {ii}**', value= farm[ii-1], inline = True)   
            embeds.add_field(name='How do I plant?', value=':seedling: Use `/plant` to get a list of plants', inline=False)
            await ctx.edit_original_response(embed=embeds)
            if updatedata == True:
                # updateinv(ctx.user.id, inv)
                # updatetime(ctx.user.id, pos, None)
                # updatefarm(ctx.user.id, farm)
                updatefarmdata(ctx.user.id, inv, time, farm)
        else:
            embed = discord.Embed(title='You do not have a NebCoins account', description='Use `/start` to create one!', color = discord.Color.gold())
            await ctx.edit_original_response(embed=embed)

    @app_commands.command(name='plant', description='Plant a crop')
    async def plant(self, ctx, plant: str=None):
        await ctx.response.defer()
        bal, level, farm = getplanteddata(ctx.user.id)
        # bal = getmoney(ctx.user.id)
        if bal == None:
            embed = discord.Embed(title='You do not have a NebCoins account', description='Use `/start` to create one!', color = discord.Color.gold())
            await ctx.edit_original_response(embed=embed)
            return
        templevel = level-1
        lvlid = lvl[templevel]+1
        plantslvl = []
        ii = 0
        query = plant
        for i in plants:
            ii+=1
            plantslvl.append(i)
            if ii == lvlid:
                break
        if query != None:
            query = plant.lower()
            if query not in plantslvl:
                await ctx.followup.send(":no_entry_sign: Plant not found")
                return
            if bal != None:
                planted = False
                land = ''
                query = str(query).lower()
                # farm = getfarm(ctx.user.id)
                for i in plantslvl:
                    if planted == True:
                        break
                    if str(query) == i:
                        cost = price[plantslvl.index(str(i))]
                        if int(bal) - cost >= 0:
                            query = str(query).lower()
                            emoji = f':{query}:'
                            emoji = f'{emoji}{emoji}{emoji}{emoji}'
                            emoji = str(emoji)
                            for i in farm:
                                if i == ':brown_square::brown_square::brown_square::brown_square:':
                                    ufarm = []
                                    l = farm.index(i)
                                    pl = False
                                    for j in farm:
                                        if i == j and pl == False:
                                            ufarm.append(emoji)
                                            pl = True
                                        else:
                                            ufarm.append(j)
                                    # updatefarm(ctx.user.id, ufarm)
                                    await ctx.followup.send(f':white_check_mark: Planted {query} on Land {l+1}')
                                    # updatemoney(ctx.user.id, bal-cost)
                                    land = l
                                    planted = True
                                    break
                            else:
                                await ctx.followup.send(':warning: Your Farm is full!')
                                planted = True
                                break
                            if planted == True:
                                now = datetime.now()
                                plantgrowth = {}
                                for i in plantslvl:
                                    plantgrowth[i] = pgrowth[plantslvl.index(i)]
                                new_datetime = now + timedelta(0, plantgrowth[query])
                                # updatetime(ctx.user.id, land, str(new_datetime))
                                updateplanted(ctx.user.id, ufarm, bal-cost, land, str(new_datetime))
                                if query.lower() == 'kiwi':
                                    nlevel = getquests(ctx.user.id)
                                    if "white_check_mark" not in nlevel[0]:
                                        mlevel = nlevel.pop(0)
                                        templevel = nlevel.pop(0)
                                        mlevel = f":white_check_mark: {mlevel}"
                                        nlevel.append(mlevel)
                                        nlevel.append(templevel)
                                        await sleep(5)
                                        updatequests(ctx.user.id, nlevel)
                        else:
                            await ctx.followup.send(':negative_squared_cross_mark: You dont have enough money')
                            planted = True
                            break
        else:
            view1 = View()
            button = Button(label="⬅️", style=discord.ButtonStyle.blurple, custom_id='n')
            view1.add_item(button)
            button2 = Button(label="🔒", style=discord.ButtonStyle.red, custom_id='l')
            view1.add_item(button2)
            embed = discord.Embed(title='**Plants**', color = discord.Color.orange())
            view = View()
            button = Button(label="➡️", style=discord.ButtonStyle.blurple, custom_id='n')
            view.add_item(button)
            button2 = Button(label="🔒", style=discord.ButtonStyle.red, custom_id='l')
            view.add_item(button2)
            ii = 0
            for i in plantslvl:
                ii += 1
                if ii == 14:
                    break
                time = f'`{convert(int(pgrowth[plantslvl.index(i)]))}`'
                embed.add_field(name=f':{i}: {i.capitalize()} - {price[plantslvl.index(str(i))]} <:nebcoin:936570857684336640>', value=f'{time}')
            embed.add_field(name='How do I plant?', value=':seedling: Use `/plant` and a plant name to fill up your farm!', inline=False)
            if lvlid == 13:
                await ctx.followup.send(embed=embed)
                return
            elif lvlid == 26:
                await ctx.followup.send(embed=embed, view=view)
                lno = 1
            while True:
                try:
                    def check(res):
                        return ctx.user == res.user and res.channel == ctx.channel
                    clicked2 = await self.bot.wait_for('interaction', check=check, timeout=30)
                    clicked = clicked2.data['custom_id']
                    if clicked == 'l':
                        button.disabled = True
                        button2.disabled = True
                        await ctx.edit_original_response(view=view)
                        await clicked2.response.defer()
                        break
                    elif clicked == 'n':
                        if lno == 1:
                            embed = discord.Embed(title='**Plants**', color = discord.Color.orange())
                            ii = 0
                            for i in plantslvl:
                                ii += 1
                                if ii == lvlid+1:
                                    break
                                if lno == 1:
                                    if ii <=  13:
                                        continue
                                time = f'`{convert(int(pgrowth[plantslvl.index(i)]))}`'
                                embed.add_field(name=f':{i}: {i.capitalize()} - {price[plantslvl.index(str(i))]} <:nebcoin:936570857684336640>', value=f'{time}')
                            embed.add_field(name='How do I plant?', value=':seedling: Use `/plant` and a plant name to fill up your farm!', inline=False)
                            await ctx.edit_original_response(embed=embed, view=view1)   
                            await clicked2.response.defer()
                            lno = 2 
                        elif lno == 2:
                            embed = discord.Embed(title='**Plants**', color = discord.Color.orange())
                            ii = 0
                            for i in plantslvl:
                                ii += 1
                                if ii == 14:
                                    break
                                time = f'`{convert(int(pgrowth[plantslvl.index(i)]))}`'
                                embed.add_field(name=f':{i}: {i.capitalize()} - {price[plantslvl.index(str(i))]} <:nebcoin:936570857684336640>', value=f'{time}')
                            embed.add_field(name='How do I plant?', value=':seedling: Use `/plant` and a plant name to fill up your farm!', inline=False)
                            await ctx.edit_original_response(embed=embed, view=view)   
                            await clicked2.response.defer()
                            lno = 1
                except TimeoutError:
                    button.disabled = True
                    button2.disabled = True
                    await ctx.edit_original_response(view=view)
                    await clicked2.response.defer()
                    break

    @app_commands.command(name='inventory', description='View your NebCoins inventory')
    async def inventory(self, ctx):
        money, inv = getinventorydata(ctx.user.id)
        if money != None:
            # inv = getinv(ctx.author.id)
            ii = 0
            invedit = []
            for i in inv:
                invedit1 = []
                for j in invedit:
                    invedit1.append(j.replace('**', '').split('x')[0])
                if i in invedit1:
                    item = invedit[invedit1.index(i)]
                    item = item.replace('**', '')
                    item = item.split('x')
                    item = str(item[0]) + '**x' + str(int(item[1])+1) + '**'
                    invedit[invedit1.index(i)] = item
                else:
                    invedit.append(i+'**x1**')
            a = ''
            for i in invedit:
                ii += 1
                a = str(a) + f'\n**{ii}.** {i}'
            if a == '':
                a = 'Your Inventory is Empty'
            embed = discord.Embed(title='Inventory', description='**[ID]**'+a + '\n\nUse `/sell [id]` to sell an item', color=discord.Color.orange())
            await ctx.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title='You do not have a NebCoins account', description='Use `/start` to create one!', color = discord.Color.gold())
            await ctx.response.send_message(embed=embed) 

    @app_commands.command(name='sell', description='Sell an inventory item')
    async def sell(self, ctx, id: int, quantity: int):
        await ctx.response.defer()
        bal, inv = getinventorydata(ctx.user.id)
        if bal != None:
            id = int(id)
            money = 0
            # inv = getinv(ctx.author.id)
            invedit = []
            for i in inv:
                invedit1 = []
                for j in invedit:
                    invedit1.append(j.replace('**', '').split('x')[0])
                if i in invedit1:
                    item = invedit[invedit1.index(i)]
                    item = item.replace('**', '')
                    item = item.split('x')
                    item = str(item[0]) + '**x' + str(int(item[1])+1) + '**'
                    invedit[invedit1.index(i)] = item
                else:
                    invedit.append(i+'**x1**')
            inv2 = []
            for j in invedit:
                j = j.replace('**', '').split('x')[0]
                inv2.append(j)
            try:
                ide = inv2[id-1]
            except:
                await ctx.followup.send(f'You do not this item in your inventory')
                return
            money = str(ide).replace(':','')
            money = mkt[plants.index(money)]
            nos = 0
            for i in inv2:
                if i == inv2[id-1]:
                    nos += 1
            if quantity > nos:
                await ctx.followup.send(f'You do not have these many items in your inventory')
                return
            for i in range(quantity):
                inv.pop(inv.index(inv2[id-1]))
            # Thread(target=updateinv, args=(ctx.author.id, inv)).start()
            # Thread(target=updatemoney, args=(ctx.author.id, bal + money)).start()
            embed = discord.Embed(title='Market', color=discord.Color.gold())
            embed.add_field(name='Type', value='Sell', inline=False)
            embed.add_field(name='Item', value=f'{ide}**x{quantity}**')
            embed.add_field(name='Price', value=f'{money} x {quantity} = {money*quantity} <:nebcoin:936570857684336640>')
            await ctx.followup.send(embed=embed)
            updatesell(ctx.user.id, inv, bal + money*quantity)
        else:
            embed = discord.Embed(title='You do not have a NebCoins account', description='Use `/start` to create one!', color = discord.Color.gold())
            await ctx.response.send_message(embed=embed)

    @app_commands.command(name='market', description='View todays market')
    async def market(self, ctx, page: app_commands.Range[int, 1, 2]):
        if getmoney(str(ctx.user.id)) != None:
            embed = discord.Embed(title="Today's Market!", color = discord.Color.dark_gold())
            ii = -1
            for i in mkt:
                ii += 1
                if page == 1 and ii == 13:
                    break
                elif page == 2 and ii < 13:
                    continue
                pl = plants[ii]
                if pl == 'cherry':
                    pl = 'cherries'
                embed.add_field(name=f':{pl}: - {pl.replace("_", " ").capitalize()}', value=f'{i} <:nebcoin:936570857684336640>')
            embed.set_footer(text='Market is ONLY for selling, you CANNOT buy from the market', icon_url='https://hotemoji.com/images/dl/o/seedling-emoji-by-twitter.png')
            await ctx.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title='You do not have a NebCoins account', description='Use `/start` to create one!', color = discord.Color.gold())
            await ctx.response.send_message(embed=embed)

    @app_commands.command(name='work', description='Work for NebCoins')
    async def work(self, ctx):
        cooldown = check_cooldown('work', ctx.user.id)
        if cooldown != None:
            await ctx.response.send_message(f'You can work <t:{cooldown}:R>', ephemeral=True)
            return
        money, p = getworkdata(ctx.user.id)
        if money != None:
            wlist = [':chart_with_downwards_trend: Buisness did not go well, You got', ':chart_with_upwards_trend: Buisness went well, You got', ':bar_chart: Buisness was stable, You got']        
            coins = choice(list(range(300, 700)))
            if p != None:
                for i in p:
                    try:
                        pp = pprice[pets.index(i)]
                        coins = coins + pp
                    except:
                        pass
            if coins < 400:
                message = f'{wlist[0]} {coins} <:nebcoin:936570857684336640>'
                col = discord.Color.red()
            elif coins > 400 and coins < 500:
                message = f'{wlist[2]} {coins} <:nebcoin:936570857684336640>'
                col = discord.Color.gold()
            elif coins > 500:
                message = f'{wlist[1]} {coins} <:nebcoin:936570857684336640>'
                col = discord.Color.green()
            embed = discord.Embed(title='**Work**', description=message, color=col)    
            await ctx.response.send_message(embed=embed)
            add_cooldown('work', ctx.user.id, 10800)
            updatemoney(ctx.user.id, money+coins)
        else:
            delete_cooldown('work', ctx.user.id)
            embed = discord.Embed(title='You do not have a NebCoins account', description='Use `/start` to create one!', color = discord.Color.gold())
            await ctx.response.send_message(embed=embed)

    @app_commands.command(name='leaderboard', description='View the NebCoins leaderboard')
    async def leaderboard(self, ctx):
          await ctx.response.defer()
          embed = discord.Embed(title='Leaderboard', color=discord.Color.green())
          gold = ''
          goldv = 0
          silver = ''
          silverv = 0
          bronz = ''
          bronzv = 0
          data = getdata()
          keys = data.keys()
          id = ''
          keys2 = []
          for i in keys:
              keys2.append(i)
          keys = keys2
          for key in keys:
              if key != "811893594716766210":
                  money = data[key]['bal']
                  if money > goldv:
                      goldv = money
                      gold = str(await self.bot.fetch_user(key))
                      id = key
          keys.pop(keys.index(id))
          for key in keys:
              if key != "811893594716766210":
                  money = data[key]['bal']
                  if money > silverv:
                      silverv = money
                      silver = str(await self.bot.fetch_user(key))
                      id = key
          keys.pop(keys.index(id))
          for key in keys:
              if key != "811893594716766210":
                  money = data[key]['bal']   
                  if money > bronzv:
                      bronzv = money
                      bronz = str(await self.bot.fetch_user(key))
                      id = key
          embed.add_field(name=f':first_place: - {str(goldv)} <:nebcoin:936570857684336640>', value=f'`{gold}`', inline=False)
          embed.add_field(name=f':second_place: - {str(silverv)} <:nebcoin:936570857684336640>', value=f'`{silver}`', inline=False)
          embed.add_field(name=f':third_place: - {str(bronzv)} <:nebcoin:936570857684336640>', value=f'`{bronz}`', inline=False)
          await ctx.followup.send(embed=embed)

    @app_commands.command(name='level', description='View your NebCoins level')
    async def level(self, ctx):
        await ctx.response.defer()
        level, nlevel, money, farm, time = getleveldata(ctx.user.id)
        content = None
        if level == 1:
            if money >= 2000 and ":white_check_mark:" not in nlevel[1]:
                templevel = nlevel.pop(0)
                mlevel = nlevel.pop(0)
                mlevel = f":white_check_mark: {mlevel}"
                nlevel.append(templevel)
                nlevel.append(mlevel)
                updatequests(ctx.user.id, nlevel)
            if ":white_check_mark:" in nlevel[0] and ":white_check_mark:" in nlevel[1]:
                content = ':tada: You just leveled up!'
                # farm = getfarm(ctx.user.id)
                farm.append(':brown_square::brown_square::brown_square::brown_square:')
                # updatefarm(ctx.user.id, farm)
                time.append(None)
                # updatelevel(ctx.user.id, 2)
                updateleveldata(ctx.user.id, farm, 2, time)
                level = 2
            else:
                content = None
        embed = discord.Embed(title='Level Information', color=discord.Color.gold())
        embed.add_field(name='Current level', value=f'**`{level}`**', inline=False)
        nlevel = "\n".join(nlevel)
        if level == 1:
            embed.add_field(name='Next level After', value=nlevel, inline=False)
        else:
            embed.add_field(name='Next level After', value="You are at the **MAX LEVEL**", inline=False)
        if level == 1:
            embed.add_field(name='Next level benifits', value=":gem: `+1 Land`\n:gem: `+13 crops`", inline=False)
        else:
            embed.add_field(name='Next level benifits', value="You are at the **MAX LEVEL**", inline=False)
        await ctx.followup.send(content=content, embed=embed)

    @app_commands.command(name='transfer', description='Transfer NebCoins')
    async def transfer(self, ctx, user: discord.User, amount: int):
        await ctx.response.defer()
        if int(amount) > 0:
            money1, money2 = gettransferdata(ctx.user.id, user.id)
            if money2 == None:
                await ctx.followup.send(f'{user.mention} does not have a NebCoins account')
                return
            if money1 - int(amount) >= 0:
                updatemoney(ctx.user.id, money1 - int(amount))
                updatemoney(user.id, money2 + int(amount))
                await ctx.followup.send(f'**Transfered {amount} <:nebcoin:936570857684336640> From {ctx.user.mention} to {user.mention}**')
            else:
                await ctx.followup.send(':warning: You Do Not Have Enough Money To Give Away')

    @app_commands.command(name='getmoney', description='Only for the creator')
    async def getmoney(self, ctx, amount: int):
        await ctx.response.defer()
        if ctx.user.id == 811893594716766210:
            updatemoney(ctx.user.id, getmoney(ctx.user.id) + int(amount))
            await ctx.followup.send(f':sunglasses: **Cool You Just Got {amount} <:nebcoin:936570857684336640>**')
        else:
            await ctx.followup.send('No.')

    @app_commands.command(name='beg', description='Beg for NebCoins')
    async def beg(self, ctx):
        cooldown = check_cooldown('beg', ctx.user.id)
        if cooldown != None:
            await ctx.response.send_message(f'You can beg <t:{cooldown}:R>', ephemeral=True)
            return
        await ctx.response.defer()
        num = choice(list(range(1,101,1)))
        add_cooldown('beg', ctx.user.id, 60)
        updatemoney(ctx.user.id, getmoney(ctx.user.id) + num)
        await ctx.followup.send(embed=discord.Embed(title='Beg', description=f'You got {num} <:nebcoin:936570857684336640>', color=discord.Color.gold()))

    @app_commands.command(name='journey', description='Go on a journey to find pets')
    async def journey(self, ctx):
        cooldown = check_cooldown('journey', ctx.user.id)
        if cooldown != None:
            await ctx.response.send_message(f'You can go on a journey <t:{cooldown}:R>', ephemeral=True)
            return
        await ctx.response.defer()
        money, userpets = getjourneydata(ctx.user.id)
        if money - 400 < 0:
            await ctx.followup.send(':x: You do not have enough money')
            return
        embed = discord.Embed(title='Confirmation', description='Going on a journey costs 500 <:nebcoin:936570857684336640>\n\nDo you want to continue?', color=discord.Color.orange())
        view = View()
        yes = Button(emoji='✅', style=discord.ButtonStyle.green, custom_id='journeyyes')
        no = Button(emoji='⛔', style=discord.ButtonStyle.red, custom_id='journeyno')
        view.add_item(yes)
        view.add_item(no)
        await ctx.followup.send(embed=embed, view=view)
        def check(res):
            return ctx.user.id == res.user.id and res.channel == ctx.channel
        try:
            res = await self.bot.wait_for('interaction', check=check, timeout=30)
            await res.response.defer()
            status = res.data['custom_id']
        except TimeoutError:
            embed.add_field(name='Status', value='Timed Out')
            yes.disabled = True
            no.disabled = True
            await ctx.edit_original_response(embed=embed, view=view)
            delete_cooldown('journey', ctx.user.id)
            return

        status = str(status).replace('journey', '')
        status = status.capitalize()
        embed.add_field(name='Status', value=f'Chose **{status}**')
        yes.disabled = True
        no.disabled = True
        await ctx.edit_original_response(embed=embed, view=view)

        if status == 'No':
            delete_cooldown('journey', ctx.user.id)
            return
        add_cooldown('journey', ctx.user.id, 86400)

        embed = discord.Embed(title='Choose a path', description='Click a button', color=discord.Color.orange())
        view = View()
        total = []
        for i in range(10):
            total.append(i+1)
        common = []
        for i in range(4):
            chosen = choice(total)
            total.pop(total.index(chosen))
            common.append(chosen)

        uncommon = []
        for i in range(3):
            chosen = choice(total)
            total.pop(total.index(chosen))
            uncommon.append(chosen)

        cross = []
        for i in range(2):
            chosen = choice(total)
            total.pop(total.index(chosen))
            cross.append(chosen)

        rare = total[0]

        for i in range(10):
            cid = None
            if i+1 in common:
                cid = 'common'+str(i)
            elif i+1 in uncommon:
                cid = 'uncommon'+str(i)
            elif i+1 in cross:
                cid = '❌'+str(i)
            elif i+1 == rare:
                cid = 'rare'+str(i)
            button = Button(label='❓', style=discord.ButtonStyle.blurple, custom_id=cid)
            view.add_item(button)

        await res.followup.send(embed=embed, view=view)
        def check(res):
            return ctx.user.id == res.user.id and res.channel == ctx.channel
        try:
            resp = await self.bot.wait_for('interaction', check=check, timeout=30)
            await resp.response.defer()
            pet_type = resp.data['custom_id']
        except TimeoutError:
            embed.add_field(name='Status', value='Timed Out')
            for i in view.children:
                i.disabled = True
                i.label = str(i.custom_id[:-1]).capitalize()
            await resp.edit_original_response(embed=embed, view=view)
            delete_cooldown('journey', ctx.user.id)
            return

        for i in view.children:
            if i.custom_id == pet_type:
                i.style = discord.ButtonStyle.green
            i.disabled = True
            i.label = str(i.custom_id[:-1]).capitalize()
        pet_type = pet_type[:-1]
        pets_choice = []
        if pet_type == 'common':
            pets_choice = pets[:petlevels[0]]
        elif pet_type == 'uncommon':
            pets_choice = pets[petlevels[0]:petlevels[1]]
        elif pet_type == 'rare':
            pets_choice = pets[petlevels[1]:]
        if pets_choice == []:
            embed.add_field(name='Result', value=':frowning: No Pet Found')
        else:
            pet = choice(pets_choice)
            if pet == 'polar bear':
                pet = 'polar_bear'
            elif pet == 'panda':
                pet = 'panda_face'
            elif pet == 'ladybug':
                pet = 'lady_beetle'
            embed.add_field(name='Result', value=f'You found a **{pet_type.upper()}** :{pet}:')
            userpets.append(pet)
        await resp.edit_original_response(embed=embed, view=view)
        updatejourney(ctx.user.id, money - 500, userpets)

    @app_commands.command(name='mypets', description='View your pets')
    async def mypets(self, ctx):
        await ctx.response.defer()
        userpets = getpets(ctx.user.id)
        rawpetsc = []
        rawpetsu = []
        rawpetsr = []
        pets_common = pets[:petlevels[0]]
        pets_uncommon = pets[petlevels[0]:petlevels[1]]
        pets_rare = pets[petlevels[1]:]
        for pet in userpets:
            if pet == 'polar_bear':
                pet = 'polar bear'
            elif pet == 'panda_face':
                pet = 'panda'
            elif pet == 'lady_beetle':
                pet = 'ladybug'
            if pet in pets_common:
                rawpetsc.append(pet)
            elif pet in pets_uncommon:
                rawpetsu.append(pet)
            elif pet in pets_rare:
                rawpetsr.append(pet)
        petsc = []
        for i in rawpetsc:
            if i == 'polar bear':
                i = 'polar_bear'
            elif i == 'panda':
                i = 'panda_face'
            elif i == 'ladybug':
                i = 'lady_beetle'
            i = f':{i}:'
            petsc1 = []
            for j in petsc:
                petsc1.append(j.replace('**', '').split('x')[0])
            if i in petsc1:
                item = petsc[petsc1.index(i)]
                item = item.replace('**', '')
                item = item.split('x')
                item = str(item[0]) + '**x' + str(int(item[1])+1) + '**'
                petsc[petsc1.index(i)] = item
            else:
                petsc.append(i+'**x1**')

        petsu = []
        for i in rawpetsu:
            if i == 'polar bear':
                i = 'polar_bear'
            elif i == 'panda':
                i = 'panda_face'
            elif i == 'ladybug':
                i = 'lady_beetle'
            i = f':{i}:'
            petsu1 = []
            for j in petsu:
                petsu1.append(j.replace('**', '').split('x')[0])
            if i in petsu1:
                item = petsu[petsu1.index(i)]
                item = item.replace('**', '')
                item = item.split('x')
                item = str(item[0]) + '**x' + str(int(item[1])+1) + '**'
                petsu[petsu1.index(i)] = item
            else:
                petsu.append(i+'**x1**')

        petsr = []
        for i in rawpetsr:
            if i == 'polar bear':
                i = 'polar_bear'
            elif i == 'panda':
                i = 'panda_face'
            elif i == 'ladybug':
                i = 'lady_beetle'
            i = f':{i}:'
            petsr1 = []
            for j in petsr:
                petsr1.append(j.replace('**', '').split('x')[0])
            if i in petsr1:
                item = petsr[petsr1.index(i)]
                item = item.replace('**', '')
                item = item.split('x')
                item = str(item[0]) + '**x' + str(int(item[1])+1) + '**'
                petsr[petsr1.index(i)] = item
            else:
                petsr.append(i+'**x1**')

        petlistc = ''
        ii = 0
        for i in petsc:
            ii += 1
            petlistc += f'**{ii}.** {i}\n'
        petlistu = ''
        ii = 0
        for i in petsu:
            ii += 1
            petlistu += f'**{ii}.** {i}\n'
        petlistr = ''
        ii = 0
        for i in petsr:
            ii += 1
            petlistr += f'**{ii}.** {i}\n'

        embed = discord.Embed(title='Your Pets', color=discord.Color.orange())
        embed.add_field(name='Common', value=petlistc, inline=False)
        embed.add_field(name='Uncommon', value=petlistu, inline=False)
        embed.add_field(name='Rare', value=petlistr, inline=False)
        await ctx.followup.send(embed=embed)

    @app_commands.command(name='pets', description='View your pets')
    async def petscommand(self, ctx, page: app_commands.Range[int, 1, 2]):
        if page == 1:
            embed = discord.Embed(title='Pets', description='**Page 1/2** (`/pets 2` to view next page)', color=discord.Color.orange())
            embed.add_field(name='COMMON', value='**50-300 Extra** <:nebcoin:936570857684336640>', inline=False)
            for i in pets:
                if pets.index(i) == petlevels[0]:
                    break
                ii = i
                if i == 'ladybug':
                    i = 'lady_beetle'
                embed.add_field(name=f':{i}: {ii}', value=f'{pprice[pets.index(ii)]} <:nebcoin:936570857684336640>')
            embed.add_field(name='UNCOMMON', value='**350-550 Extra** <:nebcoin:936570857684336640>', inline=False)
            for i in pets:
                if pets.index(i) < petlevels[0]:
                    continue
                if pets.index(i) == petlevels[1]:
                    break
                embed.add_field(name=f':{i}: {i}', value=f'{pprice[pets.index(i)]} <:nebcoin:936570857684336640>')
            embed.add_field(name='RARE', value='**600-800 Extra** <:nebcoin:936570857684336640>', inline=False)
            for i in pets:
                if pets.index(i) < petlevels[1]:
                    continue
                if pets.index(i) == pets.index('llama'):
                    break
                ii = i
                if i == 'panda':
                    i = 'panda_face'
                embed.add_field(name=f':{i}: {ii}', value=f'{pprice[pets.index(ii)]} <:nebcoin:936570857684336640>')
            embed.set_footer(text='View your pets with /mypets')
            await ctx.response.send_message(embed=embed)
        elif page == 2:
            embed = discord.Embed(title='Pets', description='**Page 2/2** (`/pets 1` to view previous page)', color=discord.Color.orange())
            embed.add_field(name='RARE', value='**850-1000 Extra** <:nebcoin:936570857684336640>', inline=False)
            for i in pets:
                if pets.index(i) < pets.index('llama'):
                    continue
                ii = i
                if i == 'polar bear':
                    i = 'polar_bear'
                embed.add_field(name=f':{i}: {ii}', value=f'{pprice[pets.index(ii)]} <:nebcoin:936570857684336640>')
            embed.set_footer(text='View your pets with /mypets')
            await ctx.response.send_message(embed=embed)

async def setup(bot:commands.Bot) -> None:
        await bot.add_cog(nebcoins(bot), guilds = [])
