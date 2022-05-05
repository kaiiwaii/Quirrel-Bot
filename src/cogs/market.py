from discord.ext import commands, pages
import discord, json
from datetime import datetime

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
    async def buy(self, ctx, *item):
        item = "".join(item)
        async with self.db.pool.acquire() as con:

            db_user = await con.fetchrow("SELECT balance FROM users WHERE id = $1", ctx.author.id)
            if db_user is None:
                await con.execute("INSERT INTO USERS (id) VALUES ($1)", ctx.author.id)
                db_user = {"balance": 0}
            product = await con.fetchrow("SELECT name, price FROM market WHERE similarity(name, $1) > 0.2", item)
            
            if product is None:
                embed = discord.Embed(title="Error", color=0xff0000)
                embed.add_field(name="No se encontró el producto", value="Por favor, comprueba que el nombre es correcto")
                await ctx.send(embed=embed)
                return
            
            if int(db_user["balance"]) < int(product["price"]):
                embed = discord.Embed(title="Error", description="No tienes suficiente dinero", color=0x7C9EB8)
                await ctx.send(embed=embed)
            else:
                print(type(product["name"]))
                await con.execute("UPDATE users SET balance = balance - $1, inventory = inventory || json_build_object($2::text, $3::timestamp)::jsonb WHERE id = $4", 
                    int(product["price"]), product["name"], datetime.utcnow(), ctx.author.id)

                embed = discord.Embed(title="Compra", description=f"Has comprado {product['name']} por {product['price']}", color=0x7C9EB8)
                await ctx.send(embed=embed)

    @commands.command()
    async def bag(self, ctx):
        async with self.db.pool.acquire() as con:
            inventory = await con.fetchrow("SELECT inventory FROM users WHERE id = $1", ctx.author.id)
            if inventory is None:
                await con.execute("INSERT INTO USERS (id) VALUES ($1)", ctx.author.id)
                embed = discord.Embed(title="Bolsa", description="No tienes nada en tu bolsa", color=0x7C9EB8)

                await ctx.send(embed=embed)
                return

            embed = discord.Embed(title="Bolsa", color=0x7C9EB8)
            print(inventory["inventory"])
            for k, v in json.loads(inventory["inventory"]).items():
                dt = datetime.fromisoformat(v)
                embed.add_field(name=k, value=f"Comprado el {dt.strftime('%d/%m/%Y')} a las {dt.strftime('%H:%M:%S')}")
            await ctx.send(embed=embed)

    @commands.command()
    async def balance(self, ctx):
        async with self.db.pool.acquire() as con:
            user = await con.fetchrow("SELECT balance FROM users WHERE id = $1", ctx.author.id)
            if user is None:
                await con.execute("INSERT INTO USERS (id) VALUES ($1)", ctx.author.id)
                user = {"balance": 0}
            embed = discord.Embed(title="Balance", description=f"{user['balance']}", color=0x7C9EB8)
            await ctx.send(embed=embed)
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def add_money(self, ctx, user: discord.User, amount: int):
        async with self.db.pool.acquire() as con:
            db_user = await con.fetchrow("SELECT balance FROM users WHERE id = $1", user.id)
            if db_user is None:
                await con.execute("INSERT INTO USERS (id) VALUES ($1)", user.id)
                db_user = {"balance": amount}
            await con.execute("UPDATE users SET balance = balance + $1 WHERE id = $2", amount, user.id)
            embed = discord.Embed(title="Balance", description=f"{db_user['balance']}", color=0x7C9EB8)
            await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def remove_money(self, ctx, user: discord.User, amount: int):
        async with self.db.pool.acquire() as con:
            db_user = await con.fetchrow("SELECT balance FROM users WHERE id = $1", user.id)
            if db_user is None:
                await con.execute("INSERT INTO USERS (id) VALUES ($1)", user.id)
                db_user = {"balance": 0}
            await con.execute("UPDATE users SET balance = $1 WHERE id = $2", int(db_user["balance"]) - amount, user.id)
            embed = discord.Embed(title="Balance", description=f"{db_user['balance']}", color=0x7C9EB8)
            await ctx.send(embed=embed)
    
    @commands.has_permissions(administrator=True)
    @commands.command()
    async def add_item(self, ctx, name: str, price: int, description: str):
        async with self.db.pool.acquire() as con:
            await con.execute("INSERT INTO market (name, price, description) VALUES ($1, $2, $3)", name, price, description)
            embed = discord.Embed(title="Market", description=f"Has añadido {name} por {price}", color=0x7C9EB8)
            await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def remove_item(self, ctx, name: str):
        async with self.db.pool.acquire() as con:
            await con.execute("DELETE FROM market WHERE name = $1", name)
            embed = discord.Embed(title="Market", description=f"Has borrado {name}", color=0x7C9EB8)
            await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def edit_item(self, ctx, name: str, price: int, description: str):
        async with self.db.pool.acquire() as con:
            await con.execute("UPDATE market SET price = $1, description = $2 WHERE name = $3", price, description, name)
            embed = discord.Embed(title="Market", description=f"Has editado {name} por {price}", color=0x7C9EB8)
            await ctx.send(embed=embed)


            


