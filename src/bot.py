from discord.ext import commands
import discord

import json

from cogs.moderation import Moderation
from cogs.misc import Misc
from cogs.trivia import Trivia
from cogs.market import Market
from cogs.game import Game

class Bot(commands.Bot):
    def __init__(self, command_prefix, db):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix, intents=intents)
        self.db = db
        self.questions = json.load(open("data/questions.json"))
        self.enemies = json.load(open("data/enemies.json"))
        self.add_cog(Moderation(self.db))
        self.add_cog(Misc(self))
        self.add_cog(Trivia(self, self.questions))
        self.add_cog(Market(self.db))
        self.add_cog(Game(self.db, self.enemies))

        self.owner_id = 686475352108826645
        
        
    async def on_ready(self):
        print('Bot started')

    async def on_error(self, event_method, *args, **kwargs):
        #send error to owner
        await self.get_user(self.owner_id).send(f'Error in {event_method}: {args}')
