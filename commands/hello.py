from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Hello File Loaded")

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"```hi @{ctx.author.display_name}```")


async def setup(client):
    await client.add_cog(Hello(client))
