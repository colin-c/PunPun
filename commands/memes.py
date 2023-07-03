import discord
from discord.ext import commands

class Memes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Messages File Loaded")

    @commands.command(aliases=["ily"])
    async def iloveyou(self, ctx):
        iloveyou_message = discord.Embed(title=f"I love you too *{ctx.author.name}*", color=discord.Color.pink())
        iloveyou_message.set_image(url="https://i0.wp.com/drunkenanimeblog.com/wp-content/uploads/2023/06/suzume-header-gif.gif?fit=498%2C280&ssl=1")
        
        await ctx.send(embed = iloveyou_message)

    @commands.command()
    async def exercise(self, ctx):
        exercise_message = discord.Embed(title=f"Run run run! *{ctx.author.name}*", color=discord.Color.green())
        exercise_message.set_image(url="https://cdn.dribbble.com/userupload/5904254/file/original-a500014d670371bb97459336c45431df.gif")
        
        await ctx.send(embed = exercise_message)

    @commands.command()
    async def bonk(self, ctx):
        bonk_message = discord.Embed(title=f"**Bonk!**", color=discord.Color.orange())
        bonk_message.set_image(url="https://media.tenor.com/CrmEU2LKix8AAAAC/anime-bonk.gif")

        await ctx.send(embed = bonk_message)

async def setup(client):
    await client.add_cog(Memes(client))