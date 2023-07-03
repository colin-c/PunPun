import discord
import json
import random
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

class Economy(commands.Cog):
    def __init___(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Economy File Loaded")

## checks balance
    @commands.command(aliases=["bal"])
    async def balance(self, ctx, member: discord.Member=None):
        with open("commands/eco.json", "r") as f:
            user_eco = json.load(f)

        ## check one's own balance
        if member is None:
            member = ctx.author
        ## otherwise, the balance of the 'member' selected
        elif member is not None:
            member = member

        if str(member.id) not in user_eco:
            user_eco[str(member.id)] = {}
            user_eco[str(member.id)]["Balance"] = 100

            with open("commands/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        eco_embed = discord.Embed(title=f"{member.name}'s Balance", description="The current balance", color=discord.Color.green())
        #eco_embed.set_thumbnail(url=ctx.message.author.avatar_url)
        eco_embed.add_field(name="Current Balance:", value=f"${user_eco[str(member.id)]['Balance']}")

        await ctx.send(embed=eco_embed)


## pinpocket others
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(aliases=["pocket"])
    async def pinpocket(self, ctx):
        with open("commands/eco.json", "r") as f:
            user_eco = json.load(f)

        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 100

            with open("commands/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)
        
        curr_bal = user_eco[str(ctx.author.id)]["Balance"]
        amount = random.randint(-30, 50)
        new_bal = curr_bal + amount

        if (curr_bal > new_bal):
            eco_embed = discord.Embed(title="Oh No! - You've been robbed", description="The stranger caught your misdeed and beated you to death", color=discord.Color.red())
            eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)
            eco_embed.set_footer(text="Maybe try finding an easier target ._.", icon_url=None)
            await ctx.send(embed=eco_embed)

            user_eco[str(ctx.author.id)]["Balance"] += amount

            with open("commands/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)
        elif (curr_bal < new_bal):
            eco_embed = discord.Embed(title="Nice One! - Free Money $$$", description="You were able to slip through their wallet as you passed by that innocent civilian", color=discord.Color.green())
            eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)
            eco_embed.set_footer(text="What a cruel world this is... lucky you", icon_url=None)
            await ctx.send(embed=eco_embed)

            user_eco[str(ctx.author.id)]["Balance"] += amount

            with open("commands/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)
        elif (curr_bal == new_bal):
            eco_embed = discord.Embed(title="Oh well!", description="It seems like nothing happened today", color=discord.Color.yellow())
            eco_embed.set_footer(text="Try again later?", icon_url=None)
            await ctx.send(embed=eco_embed)

    ## message for timer error
    @pinpocket.error
    async def pinpocket_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'`This command is on cooldown, you can use it in {round(error.retry_after, 0)} seconds`')


## daily work

async def setup(client):
    await client.add_cog(Economy(client))
