#### TESTING to get the channel ID 

## channel Test bot server: 1025140342263119974

# @client.event
# async def on_message(message):
#     #channel = client.get_channel(1025140342263119974)
#     #await channel.send('testing')
#     print(message.author, message.content, message.channel.id)
#
# pip install python-dotenv
#

import discord
import os
import asyncio

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True

client = commands.Bot(command_prefix='b!', intents=intents)

@client.event
async def on_ready():
    print('Connection is Sucessful!')

async def load():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            await client.load_extension(f"commands.{filename[:-3]}")


async def main():
    async with client:
        await load()
        await client.start(TOKEN)


asyncio.run(main())