import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID"))

## this class contains all Messages
class Messages(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Messages File Loaded")

    @commands.command()
    async def hello(self, ctx):
        channel = self.client.get_channel(DISCORD_SERVER_ID)
        await channel.send(f'Hello there {ctx.author.mention}!')

    @commands.command()
    async def goodbye(self, ctx):
        channel = self.client.get_channel(DISCORD_SERVER_ID)
        await channel.send(f'I hope to see you again``` {ctx.author.mention}!')
    
    @commands.command(aliases=["ily"])
    async def iloveyou(self, ctx):
        iloveyou_message = discord.Embed(title="I love you too", color=discord.Color.pink())
        iloveyou_message.set_image(url="https://preview.redd.it/cntkwp9wthb31.jpg?auto=webp&s=f4441eeb8bb1d77fe7e4c314ea7030b1eb93c29a")
        
        await ctx.send(embed = iloveyou_message)

async def setup(client):
    await client.add_cog(Messages(client))