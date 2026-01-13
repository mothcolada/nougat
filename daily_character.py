from discord.ext import tasks, commands
import json
import datetime
import math
import sqlite3


char_data = json.load(open('calendar.json', 'r'))


est = datetime.timezone(datetime.timedelta(hours=-5))
midnight = datetime.time(hour=0, minute=27, tzinfo=est)

class DailyCharacter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_character.start()


    @tasks.loop(time=midnight)
    async def daily_character(self):
        await self.new_character()


    async def new_character(self):
        now_est = datetime.datetime.now(tz=est)
        
        char = get_char_for_date(now_est)
        new_icon = open(f'faces/{char}.png', 'rb').read()

        # Namiverse (if Nougat) or bea hive (if miscolada)
        server = self.bot.get_guild(1325038200452022334 if self.bot.is_nougat else 422163243528617994)

        # compare bytes of current icon and the icon we want to change it to, only continue if different
        current_icon = await server.icon.read()
        if new_icon == current_icon:
            print('same icon')
            return

        await server.edit(icon=new_icon)

          # Daily Character thread (if Nougat) or personal testing channel (if miscolada)
        channel = self.bot.get_channel(1330485605515264030 if self.bot.is_nougat else 1074754885070897202)  # Daily Character thread
        await channel.send(daily_message(now_est))


def daily_message(date: datetime.datetime):
    message = '<@&1330488425006239797> '  # daily character ping

    # "Treat!" or "Happy birthday, Treat!"
    day = f'{date.month}/{date.day}'
    if day in char_data['birthdays']:
        message += 'Happy birthday, '
    message += name_of_char(get_char_for_date(date)) + '!'

    # "Happy 10th anniversary to Lonely Wolf Treat!"
    if day in char_data['anniversaries'].keys():
        anniversaries = char_data['anniversaries'][day]
        for anniversary in anniversaries:
            game_name = anniversary['game']
            game_age = date.year - anniversary['year']
            message += f' Happy {ordinal(game_age)} anniversary to {game_name}!'

    return message


def get_char_for_date(date: datetime.datetime):
    # 2024 is a year with a leap day, calendar includes leap day for when it happens
    day_in_year = (datetime.datetime(2024, date.month, date.day) - datetime.datetime(2024, 1, 1)).days
    return char_data['daily'][day_in_year]


def name_of_char(id):
    # specifal formatting
    if id == 'Mrbrew':
        return 'Mr. Brew'

    # other characters
    name = id.title()
    if name[-1] in '0123456789':
        return name[:-1]
    return name


def print_calendar(year):
    date = datetime.datetime(year, 1, 1)
    while date.year == year:
        print(f'{date.month}/{date.day} - {get_char_for_date(date)} - {daily_message(date)}')
        date += datetime.timedelta(days=1)


def ordinal(n: int):  # stolen from stack overflow because i'm lazy
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix


async def setup(bot):
    await bot.add_cog(DailyCharacter(bot))
