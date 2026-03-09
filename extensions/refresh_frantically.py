import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

class RefreshFrantically(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.refresh.start()
    

    @tasks.loop(seconds=15.0)
    async def refresh(self):
        if self.bot.is_ready():
            response = requests.get(f"https://nomnomnami.itch.io/week-with-timber?password={os.environ['WWT_PASSWORD']}")
            soup = BeautifulSoup(response.content, 'html.parser')
            timestamp = soup.find('div', {'class': 'update_timestamp'})
            if not timestamp:
                return
            if timestamp.find('abbr')['title'] != '19 January 2026 @ 22:20 UTC':
                await self.bot.get_channel(1074754885070897202).send('<@422162909582589963> we might be back ' + str(response.status_code))
    

async def setup(bot: commands.Bot):
    await bot.add_cog(RefreshFrantically(bot))
