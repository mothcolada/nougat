import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import datetime


TEST_CHANNEL = 1074754885070897202

times = [datetime.time(hour=h, minute=0, tzinfo=datetime.UTC) for h in range(24)]

class HourlyDrop(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.drop.start()

    @tasks.loop(time=times)
    async def drop(self):
        if self.bot.is_ready():
            time_since_start = datetime.datetime.now() - datetime.datetime.fromtimestamp(1774321199)
            hour = int(time_since_start.total_seconds() / 3600)
            channel = self.bot.get_channel(1485685766033117245 if self.bot.is_nougat else TEST_CHANNEL)
            file = discord.File(f"drop/{hour}.png", spoiler=(hour in [27, 63]))
            await channel.send(f"Hour {hour} of posting Drop every hour until Escape from Wormwood comes out", file=file)


async def setup(bot: commands.Bot):
    await bot.add_cog(HourlyDrop(bot))
