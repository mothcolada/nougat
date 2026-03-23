import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import datetime


TEST_CHANNEL = 1074754885070897202

times = [
    # datetime.time(hour=0, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=1, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=2, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=3, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=4, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=5, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=6, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=7, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=8, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=9, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=10, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=11, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=12, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=13, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=14, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=15, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=16, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=17, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=18, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=19, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=20, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=21, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=22, minute=0, tzinfo=datetime.UTC),
    # datetime.time(hour=23, minute=0, tzinfo=datetime.UTC)
]

class HourlyDrop(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.drop.start()

    @tasks.loop(time=times)
    async def drop(self):
        if self.bot.is_ready():
            time_since_start = datetime.datetime.now() - datetime.datetime.fromtimestamp(1774283000)
            hour = int(time_since_start.total_seconds() / 3600)

            channel = self.bot.get_channel(1485685766033117245 if self.bot.is_nougat else TEST_CHANNEL)
            await channel.send(f"Hour {hour} of posting Drop every hour until their game comes out", file=discord.File(f"drop/{hour}.png"))


async def setup(bot: commands.Bot):
    await bot.add_cog(HourlyDrop(bot))
