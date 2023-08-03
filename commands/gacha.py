import discord
import json
import random
import csv
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

class Gacha(commands.Cog):
    def __init___(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Gacha File Loaded")

    ## rolling for characters
    @commands.cooldown(1, 1800, commands.BucketType.user)
    @commands.command()
    async def roll(self, ctx):
        with open("commands/eco.json", "r") as f:
            user_eco = json.load(f)

        if str(ctx.author.id) not in user_eco:
            user_eco[str(ctx.author.id)] = {}
            user_eco[str(ctx.author.id)]["Balance"] = 100
            user_eco[str(ctx.author.id)]["Inventory"] = []

            with open("commands/eco.json", "w") as f:
                json.dump(user_eco, f, indent=4)  
        
        curr_bal = user_eco[str(ctx.author.id)]["Balance"]
        new_bal = curr_bal - 300

        ## if you don't have enough money
        if (new_bal < 0):
            eco_embed = discord.Embed(title=f"Sorry, you cannot roll :( ", description="You don't have enough money to roll", color=discord.Color.red())
            eco_embed.add_field(name="Current Balance:", value=f"${curr_bal}", inline=False)
            eco_embed.set_footer(text="You need $300 to roll... continue gaining that bread")
            
            await ctx.send(embed=eco_embed)
        
        else:
            characterTiers = ["S", "A", "B"]
            probability = [0.1, 0.4, 0.5]
            result = random.choices(characterTiers, probability)
            if (result[0] == "S"):

                with open("commands/characters/sTier.txt", "r") as f:
                    randomCharacter = f.readlines()
                    chosenCharacter = random.choice(randomCharacter).split(",")

                # if you own the character
                if(chosenCharacter[0] in user_eco[str(ctx.author.id)]["Inventory"]):

                    roll_message = discord.Embed(title=f"S Tier Pull!", description=f"Congrats, you have pulled {chosenCharacter[0]}!", color=discord.Color.yellow())
                    roll_message.set_image(url=f"{chosenCharacter[1]}")
                    roll_message.set_footer(text=f"You already own this character! New Balance: ${new_bal + 150}")
                    await ctx.send(embed = roll_message)

                    user_eco[str(ctx.author.id)]["Balance"] -= 150

                    with open("commands/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)

                else: 
                    roll_message = discord.Embed(title=f"S Tier Pull!", description=f"Congrats, you have pulled {chosenCharacter[0]}!", color=discord.Color.yellow())
                    roll_message.set_image(url=f"{chosenCharacter[1]}")
                    roll_message.set_footer(text=f"New Balance: ${new_bal}")
                    await ctx.send(embed = roll_message)

                    user_eco[str(ctx.author.id)]["Balance"] -= 300
                    user_eco[str(ctx.author.id)]["Inventory"].append(chosenCharacter[0])

                    with open("commands/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)


            elif (result[0] == "A"):

                with open("commands/characters/aTier.txt", "r") as f:
                    randomCharacter = f.readlines()
                    chosenCharacter = random.choice(randomCharacter).split(",")

                # if you own the character
                if(chosenCharacter[0] in user_eco[str(ctx.author.id)]["Inventory"]):

                    roll_message = discord.Embed(title=f"A Tier Pull!", description=f"Congrats, you have pulled {chosenCharacter[0]}!", color=discord.Color.purple())
                    roll_message.set_image(url=f"{chosenCharacter[1]}")
                    roll_message.set_footer(text=f"You already own this character! New Balance: ${new_bal + 150}")
                    await ctx.send(embed = roll_message)

                    user_eco[str(ctx.author.id)]["Balance"] -= 150

                    with open("commands/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)
                
                else:
                    roll_message = discord.Embed(title=f"A Tier Pull!", description=f"Congrats, you have pulled {chosenCharacter[0]}!", color=discord.Color.purple())
                    roll_message.set_image(url=f"{chosenCharacter[1]}")
                    roll_message.set_footer(text=f"New Balance: ${new_bal}")
                    await ctx.send(embed = roll_message)

                    user_eco[str(ctx.author.id)]["Balance"] -= 300
                    user_eco[str(ctx.author.id)]["Inventory"].append(chosenCharacter[0])

                    with open("commands/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)

            
            else:
                with open("commands/characters/bTier.txt", "r") as f:
                    randomCharacter = f.readlines()
                    chosenCharacter = random.choice(randomCharacter).split(",")

                # if you own the character
                if(chosenCharacter[0] in user_eco[str(ctx.author.id)]["Inventory"]):

                    roll_message = discord.Embed(title=f"B Tier Pull!", description=f"Congrats, you have pulled {chosenCharacter[0]}!", color=discord.Color.blue())
                    roll_message.set_image(url=f"{chosenCharacter[1]}")
                    roll_message.set_footer(text=f"You already own this character! New Balance: ${new_bal + 150}")
                    await ctx.send(embed = roll_message)

                    user_eco[str(ctx.author.id)]["Balance"] -= 150

                    with open("commands/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)

                else: 
                    roll_message = discord.Embed(title=f"B Tier Pull!", description=f"Congrats, you have pulled {chosenCharacter[0]}!", color=discord.Color.blue())
                    roll_message.set_image(url=f"{chosenCharacter[1]}")
                    roll_message.set_footer(text=f"New Balance: ${new_bal}")

                    await ctx.send(embed = roll_message)

                    user_eco[str(ctx.author.id)]["Balance"] -= 300
                    user_eco[str(ctx.author.id)]["Inventory"].append(chosenCharacter[0])

                    with open("commands/eco.json", "w") as f:
                        json.dump(user_eco, f, indent=4)
                    
    
    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            
            seconds = round(error.retry_after,0) % (24 * 3600)
            hours = seconds//3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            await ctx.send(f'`You must wait {minutes} minutes before rolling again.`')

async def setup(client):
    await client.add_cog(Gacha(client))
                        



            

        
        
