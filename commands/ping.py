import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID"))

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping File Loaded")


    @commands.command()
    async def ping(self, ctx):
        channel = self.client.get_channel(DISCORD_SERVER_ID)
        bot_latency = round(self.client.latency * 1000)
        await channel.send(f'Ping is {bot_latency} ms, {ctx.author.mention}!')

async def setup(client):
    await client.add_cog(Pring(client))