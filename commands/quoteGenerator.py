import os
import random
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()

DISCORD_SERVER_ID = int(os.getenv("DISCORD_SERVER_ID"))

## this class contains all quoteGenerator commands
class quoteGenerator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Quote Generator File Loaded")

    # generate a random quote from the API
    @commands.command(aliases = ["getquote"])
    async def getQuote(self, ctx):

        # get a quote from an zen quotes API
        response = requests.get("https://zenquotes.io/api/random")
        json_data = response.json()
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        await ctx.send(quote)

async def setup(client):
    await client.add_cog(quoteGenerator(client))