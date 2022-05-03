import discord
from discord.ext import commands
import random
from discord.ui import Button, View

class Trivia(commands.Cog):
    def __init__(self, bot, questions):
        self.questions = questions
        self.bot = bot

    @commands.command()
    async def trivia(self, ctx, *, mode="easy"):

        if mode == "easy":
            questions = self.questions["easy"]
        elif mode == "medium":
            questions = self.questions["medium"]
        elif mode == "hard":
            questions = self.questions["hard"]
        else:
            questions = self.questions["easy"]


        question = random.choice(list(questions.keys()))

        embed = discord.Embed(title=question, color=0x7C9EB8)
        trivia = TriviaView(questions[question])

        trivia.message = await ctx.send(embed=embed, view=trivia)
        await self.bot.wait_for("button_click")


class TriviaView(View):
    def __init__(self, question):
        self.options = [
        TriviaButton(question["option1"], "A", question["correct_option"]), \
        TriviaButton(question["option2"], "B", question["correct_option"]), \
        TriviaButton(question["option3"], "C", question["correct_option"])
        ] 

        super().__init__(timeout=10)
        for i in self.options:
            self.add_item(i)

        self.message = None

    async def on_timeout(self):
        for i in self.options:
            if i.finished == True:
                return

        embed = discord.Embed(title="No puedo estar aquí todo el día...", color=0x7C9EB8)
        await self.message.edit(embed=embed, view=None)


class TriviaButton(Button):
    def __init__(self, label, expected, correct):
        self.expected = expected
        self.correct = correct
        self.finished = None
        super().__init__(label=label, style=discord.ButtonStyle.green)
    
    async def callback(self, interaction):
        embed = discord.Embed(title="Respuesta ", color=0x7C9EB8)
        self.finished = True
        if self.expected == self.correct:
            embed.title += "correcta!"
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            embed.title += "incorrecta!"
            await interaction.response.edit_message(embed=embed, view=None)