import json
import re
from pathlib import Path

import discord
from discord.ext import commands


SLUR_DB_PATH = Path(__file__).resolve().parent.parent / "slur_counts.json"
SLUR_PATTERN = re.compile(
    r"^!pp\s+<@!?(\d+)>\s+slur(?:\s+(count|reset|minus)(?:\s+(\d+))?)?\s*$",
    re.IGNORECASE,
)


class SlurTracker(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._ensure_db()

    def _ensure_db(self):
        if not SLUR_DB_PATH.exists():
            SLUR_DB_PATH.write_text("{}", encoding="utf-8")

    def _load_counts(self):
        self._ensure_db()
        return json.loads(SLUR_DB_PATH.read_text(encoding="utf-8"))

    def _save_counts(self, counts):
        SLUR_DB_PATH.write_text(json.dumps(counts, indent=2), encoding="utf-8")

    def _get_entry(self, counts, member):
        entry = counts.setdefault(
            str(member.id),
            {
                "user": member.display_name,
                "count": 0,
            },
        )
        entry["user"] = member.display_name
        entry["count"] = max(0, int(entry.get("count", 0)))
        return entry

    @commands.Cog.listener()
    async def on_ready(self):
        print("Slur Tracker File Loaded")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        match = SLUR_PATTERN.match(message.content.strip())
        if not match:
            return

        mentioned_user_id, action, raw_value = match.groups()
        if not message.mentions:
            await message.channel.send("```mention a user first```")
            return

        member = message.mentions[0]
        if str(member.id) != mentioned_user_id:
            await message.channel.send("```mention a valid user```")
            return

        counts = self._load_counts()
        entry = self._get_entry(counts, member)
        action = (action or "").lower()

        if action == "count":
            count = entry["count"]
        elif action == "reset":
            entry["count"] = 0
            count = 0
            self._save_counts(counts)
        elif action == "minus":
            decrement = int(raw_value) if raw_value else 1
            entry["count"] = max(0, entry["count"] - decrement)
            count = entry["count"]
            self._save_counts(counts)
        else:
            entry["count"] += 1
            count = entry["count"]
            self._save_counts(counts)

        tracker_card = discord.Embed(
            title=member.display_name,
            color=discord.Color.red(),
        )
        tracker_card.add_field(name="Slur Count", value=str(count), inline=True)
        tracker_card.add_field(name="User", value=member.mention, inline=True)
        tracker_card.set_footer(text=f"Requested by {message.author.display_name}")

        await message.channel.send(embed=tracker_card)


async def setup(client):
    await client.add_cog(SlurTracker(client))
