import asyncio
import json
from urllib import error, parse, request

import discord
import yt_dlp
from discord.errors import ClientException
from discord.ext import commands


YTDL_FORMAT_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch1",
    "extractor_args": {
        "youtube": {
            "player_client": ["android", "web"],
            "player_skip": ["js"],
        }
    },
}

FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}


def _is_spotify_url(value):
    lowered = value.lower()
    return "open.spotify.com/" in lowered or "spotify.link/" in lowered


def _is_url(value):
    lowered = value.lower()
    return lowered.startswith("http://") or lowered.startswith("https://")


def _fetch_spotify_title(url):
    encoded_url = parse.quote(url, safe="")
    oembed_url = f"https://open.spotify.com/oembed?url={encoded_url}"
    req = request.Request(
        oembed_url,
        headers={"User-Agent": "Mozilla/5.0"},
    )

    with request.urlopen(req, timeout=10) as response:
        payload = json.load(response)

    return payload.get("title")


def _extract_track(query):
    with yt_dlp.YoutubeDL(YTDL_FORMAT_OPTIONS) as ytdl:
        info = ytdl.extract_info(query, download=False)

    if "entries" in info:
        entries = [entry for entry in info["entries"] if entry]
        if not entries:
            return None
        info = entries[0]

    audio_url = info.get("url")
    title = info.get("title") or "Unknown Title"
    webpage_url = info.get("webpage_url") or query

    if not audio_url:
        return None

    return {
        "title": title,
        "audio_url": audio_url,
        "webpage_url": webpage_url,
    }


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.players = {}

    def _get_player(self, guild_id):
        return self.players.setdefault(
            guild_id,
            {
                "queue": [],
                "current": None,
                "text_channel": None,
            },
        )

    def _get_active_voice_client(self, guild):
        if guild is None:
            return None

        if guild.voice_client is not None:
            return guild.voice_client

        for voice_client in self.client.voice_clients:
            if voice_client.guild == guild:
                return voice_client

        return None

    async def _send_music_card(self, channel, track, requested_by, description):
        music_card = discord.Embed(
            title=track["title"],
            description=description,
            color=discord.Color.blurple(),
        )
        music_card.add_field(name="Source", value=track["webpage_url"], inline=False)
        if track.get("matched_from"):
            music_card.add_field(name="Matched From", value=track["matched_from"], inline=False)
        music_card.set_footer(text=f"Requested by {requested_by}")
        await channel.send(embed=music_card)

    async def _start_next_track(self, guild):
        player = self._get_player(guild.id)
        voice_client = guild.voice_client

        if voice_client is None:
            player["current"] = None
            return

        if not player["queue"]:
            player["current"] = None
            return

        next_track = player["queue"].pop(0)
        player["current"] = next_track
        channel = player["text_channel"]

        try:
            audio_source = discord.FFmpegPCMAudio(next_track["audio_url"], **FFMPEG_OPTIONS)
            voice_client.play(
                audio_source,
                after=lambda exc: self.client.loop.call_soon_threadsafe(
                    asyncio.create_task,
                    self._handle_track_end(guild, exc),
                ),
            )
        except ClientException as exc:
            player["current"] = None
            if channel is not None:
                await channel.send(f"```could not start playback: {exc}```")
            return
        except Exception as exc:
            player["current"] = None
            if channel is not None:
                await channel.send(f"```playback failed: {type(exc).__name__}```")
            return

        if channel is not None:
            await self._send_music_card(
                channel,
                next_track,
                next_track["requested_by"],
                "Now playing",
            )

    async def _handle_track_end(self, guild, error_value):
        player = self._get_player(guild.id)
        channel = player["text_channel"]

        if error_value and channel is not None:
            await channel.send(f"```playback error: {error_value}```")

        player["current"] = None
        voice_client = guild.voice_client
        if voice_client is None or voice_client.is_paused() or voice_client.is_playing():
            return

        await self._start_next_track(guild)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music File Loaded")

    @commands.command(name="continue", aliases=["resume"])
    async def continue_music(self, ctx):
        voice_client = self._get_active_voice_client(ctx.guild)
        if voice_client is None or not voice_client.is_connected():
            await ctx.send("```i am not in a voice channel```")
            return

        if voice_client.is_paused():
            voice_client.resume()
            await ctx.send("```resumed```")
            return

        if voice_client.is_playing():
            await ctx.send("```music is already playing```")
            return

        await ctx.send("```nothing is paused right now```")

    @commands.command()
    async def play(self, ctx, *, query: str | None = None):
        if not query:
            await ctx.send("```usage: !pp play {youtube link | spotify link | song title}```")
            return

        source_query = query.strip()
        voice_state = getattr(ctx.author, "voice", None)
        if voice_state is None or voice_state.channel is None:
            await ctx.send("```join a voice channel first```")
            return

        matched_from = None

        if _is_spotify_url(source_query):
            try:
                spotify_title = await asyncio.to_thread(_fetch_spotify_title, source_query)
            except (error.HTTPError, error.URLError, TimeoutError, json.JSONDecodeError):
                await ctx.send("```could not read that spotify link```")
                return

            if not spotify_title:
                await ctx.send("```could not read that spotify link```")
                return

            source_query = spotify_title
            matched_from = "Spotify link search"
        elif not _is_url(source_query):
            matched_from = f"Search: {source_query}"

        try:
            track = await asyncio.to_thread(_extract_track, source_query)
        except Exception as exc:
            await ctx.send(f"```could not find a playable track: {type(exc).__name__}```")
            return

        if not track:
            await ctx.send("```could not find a playable track```")
            return

        track["requested_by"] = ctx.author.display_name
        track["matched_from"] = matched_from

        voice_client = self._get_active_voice_client(ctx.guild)
        try:
            if voice_client is None:
                voice_client = await voice_state.channel.connect()
            elif voice_client.channel != voice_state.channel:
                await voice_client.move_to(voice_state.channel)
        except ClientException as exc:
            await ctx.send(f"```could not join voice channel: {exc}```")
            return
        except discord.DiscordException as exc:
            await ctx.send(f"```discord voice error: {exc}```")
            return

        player = self._get_player(ctx.guild.id)
        player["text_channel"] = ctx.channel

        if voice_client.is_playing() or voice_client.is_paused() or player["current"] is not None:
            player["queue"].append(track)
            queued_card = discord.Embed(
                title=track["title"],
                description="Added to queue",
                color=discord.Color.gold(),
            )
            queued_card.add_field(name="Position", value=str(len(player["queue"])), inline=True)
            queued_card.add_field(name="Source", value=track["webpage_url"], inline=False)
            if matched_from:
                queued_card.add_field(name="Matched From", value=matched_from, inline=False)
            queued_card.set_footer(text=f"Requested by {ctx.author.display_name}")
            await ctx.send(embed=queued_card)
            return

        player["queue"].append(track)
        await self._start_next_track(ctx.guild)

    @commands.command()
    async def queue(self, ctx):
        player = self._get_player(ctx.guild.id)
        current = player["current"]
        upcoming = player["queue"][:5]

        queue_card = discord.Embed(
            title="Music Queue",
            color=discord.Color.dark_gold(),
        )

        if current is None:
            queue_card.description = "Nothing is playing right now."
        else:
            queue_card.add_field(name="Now Playing", value=current["title"], inline=False)

        if upcoming:
            queue_lines = [
                f"{index}. {track['title']}"
                for index, track in enumerate(upcoming, start=1)
            ]
            queue_card.add_field(name="Up Next", value="\n".join(queue_lines), inline=False)
        elif current is not None:
            queue_card.add_field(name="Up Next", value="Queue is empty.", inline=False)

        remaining = len(player["queue"]) - len(upcoming)
        if remaining > 0:
            queue_card.set_footer(text=f"{remaining} more track(s) waiting")

        await ctx.send(embed=queue_card)

    @commands.command()
    async def pause(self, ctx):
        voice_client = self._get_active_voice_client(ctx.guild)
        if voice_client is None or not voice_client.is_connected():
            await ctx.send("```i am not in a voice channel```")
            return

        if voice_client.is_paused():
            await ctx.send("```music is already paused```")
            return

        if not voice_client.is_playing():
            await ctx.send("```nothing is playing right now```")
            return

        voice_client.pause()
        await ctx.send("```paused```")

    @commands.command()
    async def skip(self, ctx):
        voice_client = self._get_active_voice_client(ctx.guild)
        if voice_client is None or not voice_client.is_connected():
            await ctx.send("```i am not in a voice channel```")
            return

        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()
            await ctx.send("```skipped```")
            return

        await ctx.send("```nothing is playing right now```")

    @commands.command()
    async def disconnect(self, ctx):
        voice_client = self._get_active_voice_client(ctx.guild)
        if voice_client is None or not voice_client.is_connected():
            await ctx.send("```i am not in a voice channel```")
            return

        player = self._get_player(ctx.guild.id)
        player["queue"].clear()
        player["current"] = None
        player["text_channel"] = None

        if voice_client.is_playing() or voice_client.is_paused():
            voice_client.stop()

        await voice_client.disconnect()
        await ctx.send("```disconnected```")


async def setup(client):
    await client.add_cog(Music(client))
