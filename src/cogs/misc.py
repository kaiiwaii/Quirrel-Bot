from discord.ext import commands
import discord
from datetime import datetime

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency: {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def dws(self, ctx):
        d0 = datetime.date(2019, 2, 14)
        d1 = datetime.date.today()
        delta = d1 - d0
        embed = discord.Embed(color=0x7C9EB8, timestamp=datetime.datetime.utcnow())
        embed.title = "Días desde el anuncio de SilkSong"
        embed.description = f"{str(delta).split()[0]} días"
        await ctx.send(embed=embed)
        
    @commands.command()
    async def info(self, ctx):
        """
        Info about the bot
        """
        embed = discord.Embed(
            title='Info',
            description='This bot is made by 0xKai')
        embed.add_field(name='Prefix', value=self.bot.command_prefix)
        embed.add_field(name='Version', value='1.0.0')
        await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def say(self, ctx, *, message):
        """
        Make the bot say something
        """
        await ctx.send(message)