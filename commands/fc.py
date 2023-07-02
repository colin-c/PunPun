import os
import random
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()

DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID"))

## this class contains all message/greetings
class FortuneCookie(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fortune Cookie File Loaded")
    
    @commands.command()
    async def fc(self, ctx):
        channel = self.client.get_channel(DISCORD_SERVER_ID)
        with open("commands/fcmsg.txt", "r") as f:
            randomResponses = f.readlines()
            response = random.choice(randomResponses)
        await channel.send(f'{response}')

async def setup(client):
    await client.add_cog(FortuneCookie(client))