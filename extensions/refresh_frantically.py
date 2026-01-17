import discord
from discord.ext import commands, tasks
import requests


class RefreshFrantically(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.refresh.start()
    

    @tasks.loop(seconds=5.0)
    async def refresh(self):
        if self.bot.is_ready():
            response = requests.get('https://nomnomnami.itch.io/week-with-timber')
            if response.status_code != 404:
                await self.bot.get_channel(1074754885070897202).send('<@422162909582589963> we might be back ' + str(response.status_code))
    

async def setup(bot: commands.Bot):
    await bot.add_cog(RefreshFrantically(bot))
