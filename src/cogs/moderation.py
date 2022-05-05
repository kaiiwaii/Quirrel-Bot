from discord.ext import commands
import discord, subprocess
from dotenv import dotenv_values

env = dotenv_values(".env")

class Moderation(commands.Cog):
    def __init__(self, db, bot):
        self.db = db
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        embed = discord.Embed(title="User kicked", description=f"{member} was kicked by {ctx.author}", color=0x7C9EB8)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)
    
    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        embed = discord.Embed(title="User banned", description=f"{member} was banned by {ctx.author}", color=0x7C9EB8)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        async with self.db.pool.acquire() as con:

            #get warns from db and if length > 3, kick user
            warns = await con.fetch("SELECT * FROM warns WHERE user_id = $1", member.id)
            if len(warns) >= 2:
                await member.ban(reason=reason)
                embed = discord.Embed(title="User banned", description=f"{member} was kicked because of too much warns", color=0x7C9EB8)
                embed.add_field(name="Reason", value=reason)
                await ctx.send(embed=embed)
            else:
                await con.execute("INSERT INTO warns (user_id, reason, moderator_id, moderator_name) VALUES ($1, $2, $3, $4)", member.id, reason, ctx.author.id, ctx.author.name)
                embed = discord.Embed(title="User warned", description=f"{member} was warned by {ctx.author}", color=0x7C9EB8)
                embed.add_field(name="Reason", value=reason, inline=False)
                await ctx.send(embed=embed)

    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def delwarn(self, ctx, member: discord.Member, *, warnid):
        async with self.db.pool.acquire() as con:
            await con.execute("DELETE FROM warns WHERE user_id = $1 and id = $2", member.id, warnid)
            embed = discord.Embed(title="Deleted warn from user", description=f"Index: {warnid}", color=0x7C9EB8)
            await ctx.send(embed=embed)
        
    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def listwarns(self, ctx, member: discord.Member):
        async with self.db.pool.acquire() as con:
            warns = await con.fetch("SELECT * FROM warns WHERE user_id = $1", member.id)
        embed = discord.Embed(title=f"Warns for {member.name}", color=discord.Color.blue())
        for warn in warns:
            embed.add_field(name=f"{warn['reason']}", value=f"Warned by {warn['moderator_name']}")
        await ctx.send(embed=embed)

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def clearwarns(self, ctx, member: discord.Member):
        async with self.db.pool.acquire() as con:
            await con.execute("DELETE FROM warns WHERE user_id = $1", member.id)
        embed = discord.Embed(title=f"Warns for {member.name}", color=discord.Color.blue())
        embed.add_field(name="Warns", value="Cleared")
        await ctx.send(embed=embed)

    @commands.command()
    async def runshell(self, ctx, command: str, *args):
        if discord.is_owner(ctx.author):
            await ctx.author.send("Enter password:")
            
            def check(m):
                return m.author == ctx.author and m.content == env["sh_passwd"]
            try:
                await self.bot.wait_for("message", check=check, timeout=10.0)
            except: #TimeoutError
                await ctx.author.send("No")
                return
                
            command.join(args)
            try:
                await ctx.author.send("Executing command")
                result = subprocess.check_output(command, shell=True)
                await ctx.author.send(result.decode('utf-8'))
            except subprocess.CalledProcessError as e:
                await ctx.author.send(e.output)          

        else:
            await ctx.send("You are not the owner of the server")