import discord
import json
import random
import yt_dlp
import asyncio
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                  'options': '-vn'}
YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist' : True}


# class contains all music related features
class Music(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.queue = []

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

    # bot plays music
    @commands.command()
    async def play(self, ctx, *, search):
        channel = ctx.author.voice.channel if ctx.author.voice else None
        if not channel:
            await ctx.send(f'`You are not in a voice channel right now. You must be in a voice channel to use this command`')
        
        if not ctx.voice_client:
            await channel.connect()
        
        # uses the user input to gather the information it needs
        async with ctx.typing():
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                url = info['url']
                title = info['title'] 
                self.queue.append((url, title))
                await ctx.send(f'`Added to queue: **{title}**`')

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)
    
    # allow the bot to play the music
    async def play_next(self, ctx):
        if self.queue:
            url, title = self. queue.pop(0)
            source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda _:self.client.loop.create_task(self.play_next(ctx)))
            await ctx.send(f'`Now playing **{title}**`')
        
        elif not ctx.voice_client.is_playing():
            await ctx.send(f'`Queue is empty!`')
    
    # skip to next song in queue
    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send(f'`Skipped`')


async def setup(client):
    await client.add_cog(Music(client))