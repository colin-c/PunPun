import random

import discord
from discord.ext import commands


class Coin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Coin File Loaded")

    @commands.command()
    async def coin(self, ctx):
        result = random.choice(["Heads", "Tails"])
        coin_card = discord.Embed(
            title=result,
            color=discord.Color.gold(),
        )
        coin_card.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=coin_card)


async def setup(client):
    await client.add_cog(Coin(client))
