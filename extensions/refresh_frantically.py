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
    

    @tasks.loop(seconds=5.0)
    async def refresh(self):
        if self.bot.is_ready():
            response = requests.get(f"http://moonlightjammers.itch.io/foxy-succubus-maker/", headers={"Cookie": os.environ['WWT_COOKIE']})  # f"https://nomnomnami.itch.io/week-with-timber?password={os.environ['WWT_PASSWORD']}"
            print(response.text)
            if "A password is required" in response.text:
                return
            channel = self.bot.get_channel(1074754885070897202)
            if isinstance(channel, discord.TextChannel):
                await channel.send('<@422162909582589963> we might be back ' + str(response.status_code))

            # soup = BeautifulSoup(response.content, 'html.parser')
            # timestamp = soup.find('div', {'class': 'update_timestamp'})
            # if not timestamp:
            #     return
            # abbr = timestamp.find('abbr')
            # if abbr and abbr['title'] != '30 July 2026 @ 01:19 UTC':
            #     channel = self.bot.get_channel(1074754885070897202)
            #     if isinstance(channel, discord.TextChannel):
            #         await channel.send('<@422162909582589963> we might be back ' + str(response.status_code))
    

async def setup(bot: commands.Bot):
    await bot.add_cog(RefreshFrantically(bot))
