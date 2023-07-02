import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID"))

## this class contains music commands
class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music File Loaded")
        



async def setup(client):
    await client.add_cog(Ping(client))