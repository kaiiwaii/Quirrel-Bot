import discord, random
from discord.ext import commands, pages

GAME_MAP = {
    "crossroads": [
        "https://vignette.wikia.nocookie.net/hollowknight/images/6/69/Forgotten_Crossroads_Map.jpg/revision/latest?cb=20170823160942&path-prefix=es",
        "https://gamesmobilepc.com/wp-content/uploads/2019/09/Forgotten-Crossroads-1024x434.jpg"
    ],
    "howlingcliffs": [
        "https://images-ext-1.discordapp.net/external/haej9vtNWo0HxPJPRw9xKTzICS4xE_qaVOfoBv9qp94/%3Fpid%3DImgDet%26w%3D221%26h%3D165%26c%3D7%26dpr%3D1%2C25/https/th.bing.com/th/id/OIP._2MZr0AoR2sNDmbicS3_awHaFj",
        "https://i1.wp.com/gamesmobilepc.com/wp-content/uploads/2019/09/Howling-Cliffs.jpg?resize=723%2C453&ssl=1"
    ],
    "greenpath": [
        "https://static.wikia.nocookie.net/hollowknight/images/1/19/Greenpath_Map_Clean.png/revision/latest?cb=20190103172634",
        "https://vignette.wikia.nocookie.net/hollowknight/images/4/47/Greenpath_Map.png/revision/latest?cb=20190103172634"
    ],
    "cystalpeaks": [
        "https://images-ext-2.discordapp.net/external/Ww3FyZSWA3GlklkIDV1zn9e6pCdpkYBpOVvs5fY0j8k/%3Fpid%3DImgDet%26w%3D221%26h%3D152%26c%3D7%26dpr%3D1%2C25/https/th.bing.com/th/id/OIP.GBpqjYQ3PIyHbNZMhLml5AHaFG",
        "http://gamerwalkthroughs.com/wp-content/uploads/2018/06/Hollow-Knight-Crystal-Peak-Map.jpg"
    ],
    "fungalwastes": [
        "https://images-ext-1.discordapp.net/external/WE9IuTwGDWYDxGl9BdUs41AE0vjUVrkwjYtWp5hPOMc/%3Fpid%3DImgDet%26rs%3D1/https/th.bing.com/th/id/OIP._DHn0ffkxX8yaUOpZjWrbQHaIL",
        "http://gamerwalkthroughs.com/wp-content/uploads/2018/06/Hollow-Knight-Fungal-Wastes-Map.jpg"
    ],
    "ancientbasin": [
        "https://images-ext-2.discordapp.net/external/BEvnr3QTfho86xd7XnnBIjBp0bysTWFB-_9ckTwDRNk/%3Fpid%3DImgDet%26w%3D221%26h%3D110%26c%3D7%26dpr%3D1%2C25/https/th.bing.com/th/id/OIP.MIMDJhqHiedTmkWhXBHH1gHaDt",
        "http://gamerwalkthroughs.com/wp-content/uploads/2018/07/Hollow-Knight-Ancient-Basin-Map.jpg"
    ],
    "royalwaterways": [
        "https://images-ext-1.discordapp.net/external/vYQW-Cwfn4Zkno8YIeLX66MEQlgb1F2OGJragmN8zxE/https/hollowknight.ru/wp-content/uploads/karta-korolevskih-stokov-hollow-knight.jpg",
        "http://gamerwalkthroughs.com/wp-content/uploads/2018/07/Hollow-Knight-Royal-Waterways-Map.jpg"
    ],
    "deepnest": [
        "https://images-ext-2.discordapp.net/external/iyioOz3zPCI0tL0CXLxY8-5rjnvamtPvgrKZsGN3PIM/%3Fpid%3DImgDet%26w%3D221%26h%3D109%26c%3D7%26dpr%3D1%2C25/https/th.bing.com/th/id/OIP.dlLvaeK_W1PsYT58HMS3bAHaDq",
        "http://gameplay.tips/uploads/posts/2017-03/1488486693_deepnest.jpg"
    ],
    "kingdomsedge": [
        "https://images-ext-2.discordapp.net/external/iADtm06uWnQm-4KeHuKiJRmrTNfusVWPvpHsqjl4Bnk/https/hollowknight.ru/wp-content/uploads/karta-kraya-korolevstva-hollow-knight.jpg?width=694&height=661",
        "https://gamescrack.org/wp-content/uploads/2019/09/Hollow_Knight_Bosses_56.jpg"
    ],
    "cityoftears": [
        "https://vignette.wikia.nocookie.net/hollowknight/images/b/b5/City_of_Tears_Map_Clean.png/revision/latest/scale-to-width-down/310?cb=20190809142102"
        "https://steamuserimages-a.akamaihd.net/ugc/83720896512700333/B365065BDEE7C1F0287A0C800FBEE3C7F166ED83/"
    ],
    "fogcanyon": [
        "https://images-ext-2.discordapp.net/external/DT7btuYv-eZpRcNbOLS7nRFZ4cRSFSYomCf4ZJVrFk4/%3Fpid%3DImgDet%26w%3D219%26h%3D190%26c%3D7%26dpr%3D1%2C25/https/th.bing.com/th/id/OIP.kt-XbxPyHEC02Rgb_Jd9MwAAAA",
        "http://gamerwalkthroughs.com/wp-content/uploads/2018/08/Hollow-Knight-Fog-Canyon-Map.jpg"
    ],
    "restinggrounds": [
        "https://images-ext-1.discordapp.net/external/GHkc9f3Vr8M_2gg3vEIoHlgcWgfXE1SMs2RoCM1RGmM/%3Fpid%3DImgDet%26w%3D221%26h%3D110%26c%3D7%26dpr%3D1%2C25/https/th.bing.com/th/id/OIP.S9xvqz0nE56lDL66qLvfuAHaDt",
        "http://gameplay.tips/uploads/posts/2017-03/1488486685_resting-grounds.jpg"
    ],
    "full": [
        "http://www.drglovegood.com/wp-content/uploads/2018/09/aZGgmUC-1024x693.png",
        "http://www.drglovegood.com/wp-content/uploads/2018/09/aZGgmUC-1024x693.png"
    ]
}


class Game(commands.Cog):
    def __init__(self, db, enemies):
        self.enemies = enemies
        self.db = db

    @commands.command()
    async def map(self, ctx, zone, spoiler="no"):
        if zone in GAME_MAP:
            embed = discord.Embed(title=f"{zone.title()} Map", color=0x00ff00)
            embed.set_image(url=GAME_MAP[zone][1 if spoiler == "spoiler" else 0])
            await ctx.send(embed=embed)
        elif zone == "all":
            mpages = []
            for zone in GAME_MAP:
                embed = discord.Embed(title=f"{zone.title()} Map", color=0x00ff00)
                embed.set_image(url=GAME_MAP[zone][1 if spoiler == "spoiler" else 0])
                mpages.append(embed)
            pag = pages.Paginator(pages=mpages)
            await pag.send(ctx)
        else:
            embed = discord.Embed(title="Error", color=0xff0000)
            embed.add_field(name="Error", value="That map doesn't exist.", inline=False)
            embed.add_field(name="Available Maps", value="\n".join(GAME_MAP.keys()))
            await ctx.send(embed=embed)

    @commands.command()
    async def fight(self, ctx):
        m = random.choice(self.enemies.keys())
        embed = discord.Embed(title=f"Has luchado contra un {m}", color=0x00ff00)
        async with self.db.acquire() as con:
            u = await con.fetchrow("SELECT xp FROM users WHERE id = $1", ctx.author.id)
            if u is None:
                await con.execute("INSERT INTO users (id) VALUES ($1)", ctx.author.id)
                
        if random.randint(0, 1) == 0:
            async with self.db.acquire() as con:
                await con.execute("UPDATE users SET xp = xp + $1 WHERE id = $2", m[0], ctx.author.id)

            embed.add_field(name=f"Has ganado {m[0]} <:Geo:835657052017524769>", value="Sigue así y pronto liberarás Hallownest!", inline=False)
        else:
            embed.add_field(name=f"Has perdido {m[1]} <:Geo:835657052017524769>", value="Una pena. Quizá deberías mejorarte el aguijón y probar otra vez", inline=False)
            async with self.db.acquire() as con:
                await con.execute("UPDATE users SET xp = xp - $1 WHERE id = $2", m[1], ctx.author.id)

        await ctx.send(embed=embed)


