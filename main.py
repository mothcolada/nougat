import discord
from discord.ext import tasks, commands
import asyncio
import os
from dotenv import load_dotenv
import sqlite3

# from daily_character import print_calendar
# print_calendar(2026)


# TODO: use database instead of json for nami feeds
# TODO: add more characters to calendar (1/16 and later, oh my god please just do it it's so soon)

# conn = sqlite3.connect('database.db')
# cursor = conn.cursor()


class Bot(commands.Bot):
    is_nougat: bool

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)


    async def setup_hook(self):
        self.is_nougat = self.user.id == 1425561875885719634  # could be either Nougat or my test bot miscolada
        await self.load_extension('daily_character')
        await self.load_extension('nami_feeds')
        await self.load_extension('refresh_frantically')


    async def on_ready(self):
        await self.log(f'good morning world i am {self.user.name}')
        await self.get_cog('DailyCharacter').new_character()  # try to change icon if outdated


    async def on_message(self, message: discord.Message):
        # if i send "die" in my #nougat-log channel, shut down the bot
        if message.author.id == 422162909582589963 and message.channel.id == 1425915517184512041 and message.content == 'die':
            await self.log('good night')
            await self.close()


    async def log(self, message):
        print(message)
        await self.get_channel(1425915517184512041).send(message)  # my #nougat-log channel


    async def report(self, message):
        await self.log('<@422162909582589963> ' + str(message))


bot = Bot()
load_dotenv()
bot.run(os.getenv('TOKEN'))

