from discord.ext import commands, pages
import discord

class Market(commands.Cog):
    def __init__(self, db):
        self.db = db
    
    @commands.command()
    async def market(self, ctx: discord.ApplicationContext):
        async with self.db.pool.acquire() as con:
            market = await con.fetch("SELECT name, price, description FROM market ORDER BY price ASC")

        mpages = []

        for row in market:

            e = discord.Embed(title="Market", color=0x7C9EB8)
            e.add_field(name=row[0], value=f"Precio: {row[1]}")
            e.add_field(name="Descripción", value=row[2])
            mpages.append(e)
        
        pag = pages.Paginator(pages=mpages)
        await pag.send(ctx)

    @commands.command()
    async def buy(self, ctx, item: str):
        async with self.db.pool.acquire() as con:
            user = await con.fetchrow("SELECT balance FROM users WHERE user_id = $1", ctx.author.id)
            if user is None:
                await con.execute("INSERT INTO USERS (id) VALUES ($1)", ctx.author.id)
            user = {"balance": 0}
            product = await con.fetch("SELECT name, price FROM market WHERE name LIKE $1", item)
            if int(user["balance"]) < int(product["price"]):
                embed = discord.Embed(title="Error", description="No tienes suficiente dinero", color=0x7C9EB8)
                await ctx.send(embed=embed)
            else:
                await con.execute("UPDATE users SET balance = $1, inventory = inventory || $2::jsonb  WHERE user_id = $2", int(user["balance"]) - int(product["price"]), ctx.author.id)
                embed = discord.Embed(title="Compra", description=f"Has comprado {product['name']} por {product['price']}", color=0x7C9EB8)
                await ctx.send(embed=embed)
            


