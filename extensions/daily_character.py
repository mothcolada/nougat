import datetime
import json
import zoneinfo
import logging
from pathlib import Path
import discord
from discord.ext import commands, tasks
from main import Nougat

# TODO: types


NAMIVERSE_ID = 1521632400453402732
NAMIVERSE_DAILY_CHAR_CHANNEL = 1521644859650474115
DAILY_CHAR_ROLE = 1521632400491417772

TEST_GUILD_ID = 422163243528617994
TEST_CHANNEL = 1074754885070897202


calendar_json = open("calendar.json", "r")
char_data = json.load(calendar_json)
calendar_json.close()

eastern_time = zoneinfo.ZoneInfo("America/New_York")  # Use zoneinfo so it tracks EST/EDT changes.
midnight = datetime.time(hour=0, minute=0, tzinfo=eastern_time)


class DailyCharacter(commands.Cog):
    def __init__(self, bot: Nougat):
        self.bot = bot
        self.daily_character.start()
        now_est = datetime.datetime.now(tz=eastern_time)
        print_calendar(now_est, now_est + datetime.timedelta(14))
        


    def cog_unload(self):
        self.daily_character.cancel()


    @tasks.loop(time=midnight)
    async def daily_character(self):
        await self.new_character()

    @daily_character.before_loop
    async def before_daily_character(self):
        await self.bot.wait_until_ready()
        await self.new_character()  # Check immediately if a new one is needed

    async def new_character(self):
        now_est = datetime.datetime.now(tz=eastern_time)
        char = get_char_for_date(now_est)
        if char == '':
            await self.bot.report('daily character not set for today')

        if now_est.month == 6 or (now_est.month == 7 and now_est.day <= 8):
            filename = f"faces/pride/{char}.png"
        else:
            filename = f"faces/{char}.png"

        with open(filename, "rb") as image:
            new_icon = image.read()

        server = self.bot.get_guild(NAMIVERSE_ID if self.bot.is_nougat else TEST_GUILD_ID)
        if not server:
            raise Exception('server not found')

        # compare bytes of current icon and the icon we want to change it to, only continue if different
        current_icon = server.icon

        if not current_icon:
            raise Exception('icon not found')

        current_icon = await current_icon.read()
        if new_icon == current_icon:
            logging.info("new icon matches current icon; cancelling daily character")
            return

        await server.edit(icon=new_icon)

        channel = self.bot.get_channel(NAMIVERSE_DAILY_CHAR_CHANNEL if self.bot.is_nougat else TEST_CHANNEL)  # Daily Character thread
        if not isinstance(channel, discord.PartialMessageable):
            raise Exception('daily character channel not found')
            
        await channel.send(daily_message(now_est))


def daily_message(date: datetime.datetime):
    message = f"<@&{DAILY_CHAR_ROLE}> "  # ping

    # "Treat!" or "Happy birthday, Treat!"
    day = f"{date.month}/{date.day}"
    char_id = get_char_for_date(date)
    char = name_of_char(char_id)
    if day in char_data["birthdays"]:
        message += "Happy birthday, "
    if (date.month == 6 or (date.month == 7 and date.day <= 9)) and char_id in char_data["pride"].keys(): # pride
        if day in char_data["birthdays"]:
            message += char + "!"
        message += f"{char} is {char_data['pride'][char_id]}!"
    else:
        message += char + "!"

    # "Happy 10th anniversary to Lonely Wolf Treat!"
    if day in char_data["anniversaries"].keys():
        anniversaries = char_data["anniversaries"][day]
        for anniversary in anniversaries:
            game_name = anniversary["game"]
            game_age = date.year - anniversary["year"]
            if game_age > 0:
                message += f" Happy {ordinal(game_age)} anniversary to {game_name}!"
            else:
                message += f" Happy release day to {game_name}!"

    return message


def get_char_for_date(date: datetime.datetime):
    # 2016 is a year with a leap day, calendar includes leap day for when it happens
    day_in_year = (datetime.datetime(2016, date.month, date.day) - datetime.datetime(2016, 1, 1)).days
    return char_data["daily"][day_in_year]


def name_of_char(id: str):
    name = id.split("-")[0].replace("_", " ").title()

    if id == "":
        return ""
    if id == "Mr Brew":
        return "Mr. Brew"
    if id == "Nougat":
        return "Me"
    if id in ['Searina', 'Illi', 'Ezel', 'Vido']:
        return id.upper()

    return name


def print_calendar(start_date, end_date):
    now_est = datetime.datetime.now(tz=eastern_time)
    date = start_date # datetime.datetime(now_est.year, 1, 1)
    while date < end_date:
        char_id = get_char_for_date(date)
        
        if date.month == 6 or (date.month == 7 and date.day <= 8):
            filename = f"faces/pride/{char_id}.png"
        else:
            filename = f"faces/{char_id}.png"

        if not Path(filename).exists():
            print("X", end=" ")

        print(f"{date.month}/{date.day} - {char_id} - {daily_message(date)}")

        date += datetime.timedelta(days=1)


def ordinal(n: int):  # stolen from stack overflow because i'm lazy
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    return str(n) + suffix


async def setup(bot: commands.Bot):
    await bot.add_cog(DailyCharacter(bot))

if __name__ == "__main__":
    now_est = datetime.datetime.now(tz=eastern_time)
    print_calendar(datetime.datetime(now_est.year, 1, 1), datetime.datetime(now_est.year+1, 1, 1))
