import os
import random
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
        channel = self.client.get_channel(DISCORD_SERVER_ID)
        result = random.choice(["Head", "Tail"])
        await channel.send(f'{result}')

async def setup(client):
    await client.add_cog(Coin(client))


