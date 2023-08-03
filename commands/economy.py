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
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 100
            user_eco[str(ctx.author.id)]["Inventory"] = []

            with open("commands/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)

        eco_embed = discord.Embed(title=f"{member.name}'s Balance", description="The current balance", color=discord.Color.green())
        # eco_embed.set_thumbnail(url=ctx.author.avatar_url)
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
            user_eco[str(ctx.author.id)]["Inventory"] = []

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
            await ctx.send(f'`You are tired... you can do it again in {round(error.retry_after, 0)} seconds`')

## daily work
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.command(aliases=["daily"])
    async def work(self, ctx):
        with open("commands/eco.json", "r") as f:
            user_eco = json.load(f)

        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 100
            user_eco[str(ctx.author.id)]["Inventory"] = []

            with open("commands/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)   
        
        curr_bal = user_eco[str(ctx.author.id)]["Balance"]
        amount = random.randint(140, 180)
        new_bal = curr_bal + amount

        eco_embed = discord.Embed(title=f"{ctx.author.name} Completed Work Today!", description="Congrats, you have completed your 8 hour shift! You deserve a break!", color=discord.Color.blue())
        eco_embed.add_field(name="Income Today:", value=f"${amount}", inline=False)
        eco_embed.add_field(name="New Balance:", value=f"${new_bal}", inline=False)
        eco_embed.set_footer(text="The rest of the day is up to you!!")

        await ctx.send(embed=eco_embed)
        user_eco[str(ctx.author.id)]["Balance"] += amount

        with open("commands/eco.json", "w") as f:
            json.dump(user_eco, f, indent=4)

    @work.error
    async def work_error(self, ctx, error):
         if isinstance(error, commands.CommandOnCooldown):

            seconds = round(error.retry_after,0) % (24 * 3600)
            hours = seconds//3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            
            await ctx.send(f'`You have already worked your daily shift, come back in {hours} hours, {minutes} minutes, {seconds} seconds.`')


async def setup(client):
    await client.add_cog(Economy(client))
