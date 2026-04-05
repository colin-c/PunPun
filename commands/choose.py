import random

import discord
from discord.ext import commands


RIOT_CHOICES = ["League", "Valorant"]


class Choose(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Choose File Loaded")

    @commands.command()
    async def riot(self, ctx):
        selection = random.choice(RIOT_CHOICES)
        choose_card = discord.Embed(
            title=selection,
            color=discord.Color.orange(),
        )
        choose_card.set_footer(text=f"Requested by {ctx.author.display_name}")
        await ctx.send(embed=choose_card)


async def setup(client):
    await client.add_cog(Choose(client))
