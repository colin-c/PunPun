import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID"))

## this class contains all message/greetings
class Greeting(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Greeting File Loaded")

    @commands.command()
    async def hello(self, ctx):
        channel = self.client.get_channel(DISCORD_SERVER_ID)
        await channel.send(f'Hello there {ctx.author.mention}!')

    @commands.command()
    async def goodbye(self, ctx):
        channel = self.client.get_channel(DISCORD_SERVER_ID)
        await channel.send(f'I hope to see you again {ctx.author.mention}!')
    
    @commands.command(aliases=[ily])
    async def iloveyou(self, ctx):
        channel = self.client.get_channel(DISCORD_SERVER_ID)
        await channel.send(f'I love you too, {ctx.author.mention} <3')

async def setup(client):
    await client.add_cog(Greeting(client))