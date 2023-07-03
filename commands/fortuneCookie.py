import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()

DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID"))

## this class contains all FortuneCookie commands
class FortuneCookie(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fortune Cookie File Loaded")

    @commands.command(aliases=["fc"])
    async def fortuneCookie(self, ctx):
        result = random.choice(["Good", "Bad", "Love"])
        
        if (result == "Good"):
            with open("commands/fcGood.txt", "r") as f:
                randomResponses = f.readlines()
                response = random.choice(randomResponses)

            fcGood_message = discord.Embed(title="Good", description=response, color=discord.Color.green())
            await ctx.send(embed = fcGood_message)
        elif (result == "Bad"):
            with open("commands/fcBad.txt", "r") as f:
                randomResponses = f.readlines()
                response = random.choice(randomResponses)

            fcBad_message = discord.Embed(title="Bad", description=response, color=discord.Color.red())
            await ctx.send(embed = fcBad_message)
        elif (result == "Love"):
            with open("commands/fcLove.txt", "r") as f:
                randomResponses = f.readlines()
                response = random.choice(randomResponses)

            fcLove_message = discord.Embed(title="Love", description=response, color=discord.Color.pink())
            await ctx.send(embed = fcLove_message)
    


async def setup(client):
    await client.add_cog(FortuneCookie(client))