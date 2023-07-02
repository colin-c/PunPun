import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()

DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID"))

## this class contains flipping a coin
class Coin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Coin File Loaded")

    @commands.command()
    async def coin(self, ctx):
        result = random.choice(["Head", "Tail"])
        
        if (result == "Head"):
            head_message = discord.Embed(title="HEAD", color=discord.Color.green())
            head_message.set_image(url="https://hips.hearstapps.com/digitalspyuk.cdnds.net/16/28/1468204896-pikachu-caterpie.gif?resize=980:*")
            await ctx.send(embed = head_message)
        else:
            tail_message = discord.Embed(title="TAIL", color=discord.Color.red())
            tail_message.set_image(url="https://media.tenor.com/vb0GTerCLNkAAAAC/cute-anime-cat-gif.gif")
            await ctx.send(embed = tail_message)

async def setup(client):
    await client.add_cog(Coin(client))


