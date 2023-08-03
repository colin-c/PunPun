import discord
import os
import base64
import json
from requests import post
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

# important credentials accessing spotify API
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# get the access token from spotify
def get_token():

    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"

    header = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url,headers=header, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]

    return token

# authorization header request
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# class contains all music related features
class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music File Loaded")

    # join voice channel
    @commands.command(pass_context = True)
    async def join(self, ctx):

        if(ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.send(f'`Pun Pun just joined`')

        else:
            await ctx.send(f'`You are not in a voice channel right now. You must be in a voice channel to use this command`')
    
    # leaves voice channel
    @commands.command(pass_context = True, aliases = ["disconnect", "quit"])
    async def leave(self, ctx):

        if(ctx.author.voice):
            await ctx.guild.voice_client.disconnect()
            await ctx.send(f'`Pun Pun left`')

        else:
            await ctx.send(f'`Pun Pun is not in a voice channel`')

    @commands.command()
    async def play(self, ctx, arg1):
        token = get_token()

async def setup(client):
    await client.add_cog(Music(client))