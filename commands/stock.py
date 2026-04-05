from datetime import datetime

import discord
import yfinance as yf
from discord.ext import commands


def _format_money(value):
    if value is None:
        return "N/A"

    try:
        number = float(value)
    except (TypeError, ValueError):
        return "N/A"

    return f"${number:,.2f}"


def _pick_session_label(history_index):
    if history_index is None or history_index.empty:
        return "today"

    latest_timestamp = history_index[-1]
    if hasattr(latest_timestamp, "to_pydatetime"):
        latest_timestamp = latest_timestamp.to_pydatetime()

    return latest_timestamp.strftime("%A").lower()


class Stock(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Stock File Loaded")

    @commands.command()
    async def stock(self, ctx, ticker: str | None = None):
        if not ticker:
            await ctx.send("```usage: !pp stock AAPL```")
            return

        try:
            stock = yf.Ticker(ticker.upper())
            info = stock.info
            history = stock.history(period="5d", interval="1d")
        except Exception:
            await ctx.send("```could not fetch stock data right now```")
            return

        if not info:
            await ctx.send(f"```no stock data found for {ticker.upper()}```")
            return

        symbol = info.get("symbol") or ticker.upper()
        company_name = info.get("longName") or info.get("shortName") or "N/A"
        exchange_name = info.get("fullExchangeName") or info.get("exchange") or "N/A"
        current_price = info.get("currentPrice") or info.get("regularMarketPrice")

        session_label = "today"
        day_high = info.get("dayHigh") or info.get("regularMarketDayHigh")
        day_low = info.get("dayLow") or info.get("regularMarketDayLow")

        if history is not None and not history.empty:
            latest_row = history.iloc[-1]
            session_label = _pick_session_label(history.index)
            current_price = latest_row.get("Close", current_price)
            day_high = latest_row.get("High", day_high)
            day_low = latest_row.get("Low", day_low)

        stock_card = discord.Embed(
            title=company_name,
            description=f"`{symbol}`",
            color=discord.Color.green(),
        )
        stock_card.add_field(name="Exchange", value=exchange_name, inline=False)
        stock_card.add_field(name="Current Price", value=_format_money(current_price), inline=True)
        stock_card.add_field(
            name=f"{session_label.title()} High",
            value=_format_money(day_high),
            inline=True,
        )
        stock_card.add_field(
            name=f"{session_label.title()} Low",
            value=_format_money(day_low),
            inline=True,
        )
        stock_card.set_footer(text=f"Requested by {ctx.author.display_name}")

        await ctx.send(embed=stock_card)


async def setup(client):
    await client.add_cog(Stock(client))
