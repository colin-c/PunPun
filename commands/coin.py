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
            head_message.set_image(url="https://ih1.redbubble.net/image.2982672877.3829/poster,504x498,f8f8f8-pad,600x600,f8f8f8.jpg")
            await ctx.send(embed = head_message)
        else:
            tail_message = discord.Embed(title="TAIL", color=discord.Color.red())
            tail_message.set_image(url="https://i.kym-cdn.com/photos/images/original/000/996/823/191.jpg")
            await ctx.send(embed = tail_message)

async def setup(client):
    await client.add_cog(Coin(client))


