from discord.ext import commands
import discord

import json

from cogs.moderation import Moderation
from cogs.misc import Misc
from cogs.trivia import Trivia
from cogs.market import Market

class Bot(commands.Bot):
    def __init__(self, command_prefix, db):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix, intents=intents)
        self.db = db
        self.questions = json.load(open("data/questions.json"))
        self.add_cog(Moderation(self.db))
        self.add_cog(Misc(self))
        self.add_cog(Trivia(self, self.questions))
        self.add_cog(Market(self.db))
        
        
    async def on_ready(self):
        print('Bot started')
