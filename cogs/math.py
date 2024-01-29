import discord
from discord import app_commands
from discord.ext import commands
from nebulafunctions.math.fmath import *
import math as mathf

class math(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot
        
    @app_commands.command(name='add', description='Add numbers')
    async def add(self, ctx, numbers: str):
        if ',' not in numbers:
            await ctx.response.send_message('Please separate the numbers with commas\n\nExample: `/add 1,2,3`', ephemeral=True)
            return
        numbers = numbers.replace(' ', '')
        numbers = numbers.split(',')
        for i in numbers:
            if nebulaisdigit(i):
                pass
            else:
                await ctx.response.send_message('Please use numbers only\n\nExample: `/add 1,2,3`', ephemeral=True)
                return
        ans = float(numbers[0])
        for i in numbers[1:]:
            ans += float(i)
        if '-' in str(ans):
            ans = f'({ans})'
        for i in numbers:
            if '-' in i:
                newi = f'({i})'
                numbers[numbers.index(i)] = newi
        numbers = ' + '.join(numbers)
        embed = discord.Embed(title='Add', description=f'{numbers}\n= **{ans}**', color = discord.Color.green())
        await ctx.response.send_message(embed=embed)
        
    @app_commands.command(name='subtract', description='Subtract numbers')
    async def subtract(self, ctx, numbers: str):
        if ',' not in numbers:
            await ctx.response.send_message('Please separate the numbers with commas\n\nExample: `/subtract 4,2,1`', ephemeral=True)
            return
        numbers = numbers.replace(' ', '')
        numbers = numbers.split(',')
        for i in numbers:
            if nebulaisdigit(i):
                pass
            else:
                await ctx.response.send_message('Please use numbers only\n\nExample: `/subtract 4,2,1`', ephemeral=True)
                return
        ans = float(numbers[0])
        for i in numbers[1:]:
            ans -= float(i)
        if '-' in str(ans):
            ans = f'({ans})'
        for i in numbers:
            if '-' in i:
                newi = f'({i})'
                numbers[numbers.index(i)] = newi
        numbers = ' - '.join(numbers)
        embed = discord.Embed(title='Subtract', description=f'{numbers}\n= **{ans}**', color = discord.Color.green())
        await ctx.response.send_message(embed=embed)

    @app_commands.command(name='multiply', description='Multiply numbers')
    async def multiply(self, ctx, numbers: str):
        if ',' not in numbers:
            await ctx.response.send_message('Please separate the numbers with commas\n\nExample: `/multiply 1,2,3`', ephemeral=True)
            return
        numbers = numbers.replace(' ', '')
        numbers = numbers.split(',')
        for i in numbers:
            if nebulaisdigit(i):
                pass
            else:
                await ctx.response.send_message('Please use numbers only\n\nExample: `/multiply 1,2,3`', ephemeral=True)
                return
        ans = float(numbers[0])
        for i in numbers[1:]:
            ans *= float(i)
        if '-' in str(ans):
            ans = f'({ans})'
        for i in numbers:
            if '-' in i:
                newi = f'({i})'
                numbers[numbers.index(i)] = newi
        numbers = ' x '.join(numbers)
        embed = discord.Embed(title='Multiply', description=f'{numbers}\n= **{ans}**', color = discord.Color.green())
        await ctx.response.send_message(embed=embed)
        
    @app_commands.command(name='divide', description='Divide numbers')
    async def divide(self, ctx, numbers: str):
        if ',' not in numbers:
            await ctx.response.send_message('Please separate the numbers with commas\n\nExample: `/divide 4,2`', ephemeral=True)
            return
        numbers = numbers.replace(' ', '')
        numbers = numbers.split(',')
        for i in numbers:
            if nebulaisdigit(i):
                pass
            else:
                await ctx.response.send_message('Please use numbers only\n\nExample: `/divide 4,2`', ephemeral=True)
                return
        ans = float(numbers[0])
        for i in numbers[1:]:
            ans /= float(i)
        if '-' in str(ans):
            ans = f'({ans})'
        for i in numbers:
            if '-' in i:
                newi = f'({i})'
                numbers[numbers.index(i)] = newi
        numbers = ' ÷ '.join(numbers)
        embed = discord.Embed(title='Divide', description=f'{numbers}\n= **{ans}**', color = discord.Color.green())
        await ctx.response.send_message(embed=embed)
        
    @app_commands.command(name='squareroot', description='Find the square root of a number')
    async def sroot(self, ctx, number: float):
        ans = mathf.sqrt(number)
        embed = discord.Embed(title='Square Root',description=f'**√{number} = {ans}**', colour = discord.Color.green())
        await ctx.response.send_message(embed=embed)
        
    @app_commands.command(name='cuberoot', description='Find the cube root of a number')
    async def croot(self, ctx, number: float):
        ans = number ** (1/3)
        embed = discord.Embed(title='Cube Root',description=f'**∛{number} = {ans}**', colour = discord.Color.green())
        await ctx.response.send_message(embed=embed)
    
    @app_commands.command(name='circumference', description='Find the circumference of a circle')
    @app_commands.choices(inputtype=[
        app_commands.Choice(name="Radius", value="1"),
        app_commands.Choice(name="Diameter", value="2")
    ])
    async def circumference(self, ctx, inputtype: app_commands.Choice[str], number: float):
        if inputtype.value == '1':
            ans = 2 * 3.14 * number
        elif inputtype.value == '2':
            ans = 3.14 * number
        
        embed = discord.Embed(title='Circumference',description=f'Circumference of a circle with *{inputtype.name.lower()}* `{number}` = `{ans}`',colour = discord.Color.gold())
        await ctx.response.send_message(embed=embed)
    
    @app_commands.command(name='speed', description='Find the speed of an object')
    async def speed(self, ctx, distance: float, time: float):
        ans = distance / time
        
        embed = discord.Embed(title='Speed',description=f'**Speed = Distance ÷ Time**\n= {distance} ÷ {time}\n**= {ans}**',colour = discord.Color.gold())
        await ctx.response.send_message(embed=embed)
        
    @app_commands.command(name='distance', description='Find the distance an object traveled')
    async def distance(self, ctx, speed: float, time: float):
        ans = speed * time
        
        embed = discord.Embed(title='Distance',description=f'**Distance = Speed × Time**\n= {speed} × {time}\n**= {ans}**',colour = discord.Color.gold())
        await ctx.response.send_message(embed=embed)
        
    @app_commands.command(name='time', description='Find the time an object takes to cover a distance')
    async def time(self, ctx, distance: float, speed: float):
        ans = distance / speed
        
        embed = discord.Embed(title='Distance',description=f'**Time = Distance ÷ Speed**\n= {distance} ÷ {speed}\n**= {ans}**',colour = discord.Color.gold())
        await ctx.response.send_message(embed=embed)
        
async def setup(bot:commands.Bot) -> None:
        await bot.add_cog(math(bot), guilds = []) #leave empty for all servers