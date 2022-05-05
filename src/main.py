from bot import Bot
import asyncio
from db import Database
from dotenv import dotenv_values

env = dotenv_values(".env")
token = env.pop("token")
env.pop("sh_passwd")


async def run():
    db = Database(env)
    await db.connect()
    bot = Bot("!", db)
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(run())
