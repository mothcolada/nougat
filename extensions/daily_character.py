import datetime
import json
import zoneinfo

from discord.ext import commands, tasks

# TODO: types


NAMIVERSE_ID = 1325038200452022334
NAMIVERSE_DAILY_CHAR_THREAD = 1330485605515264030
DAILY_CHAR_ROLE = 1330488425006239797

TEST_GUILD_ID = 422163243528617994
TEST_CHANNEL = 1074754885070897202



char_data = json.load(open("calendar.json", "r"))  # FIXME: Unclosed file descriptor

eastern_time = zoneinfo.ZoneInfo("America/New_York")  # Use zoneinfo so it tracks EST/EDT changes.
midnight = datetime.time(hour=0, minute=0, tzinfo=eastern_time)


class DailyCharacter(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.daily_character.start()

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
        new_icon = open(f"faces/{char}.png", "rb").read()  # FIXME: Unclosed file descriptor

        server = self.bot.get_guild(NAMIVERSE_ID if self.bot.is_nougat else TEST_GUILD_ID)
        if not server:
            raise Exception('server not found')
            return

        # compare bytes of current icon and the icon we want to change it to, only continue if different

        current_icon = server.icon
        if not current_icon:
            raise Exception('icon not found')
            return
        
        current_icon = await current_icon.read()
        if new_icon == current_icon:
            print("same icon")
            return

        await server.edit(icon=new_icon)

        channel = self.bot.get_channel(NAMIVERSE_DAILY_CHAR_THREAD if self.bot.is_nougat else TEST_CHANNEL)  # Daily Character thread
        await channel.send(daily_message(now_est))
        # except Exception as e:
        #     await self.bot.report(e)


def daily_message(date: datetime.datetime):
    message = f"<@&{DAILY_CHAR_ROLE}> "  # ping

    # "Treat!" or "Happy birthday, Treat!"
    day = f"{date.month}/{date.day}"
    if day in char_data["birthdays"]:
        message += "Happy birthday, "
    message += name_of_char(get_char_for_date(date)) + "!"

    # "Happy 10th anniversary to Lonely Wolf Treat!"
    if day in char_data["anniversaries"].keys():
        anniversaries = char_data["anniversaries"][day]
        for anniversary in anniversaries:
            game_name = anniversary["game"]
            game_age = date.year - anniversary["year"]
            message += f" Happy {ordinal(game_age)} anniversary to {game_name}!"

    return message


def get_char_for_date(date: datetime.datetime):
    # 2024 is a year with a leap day, calendar includes leap day for when it happens
    day_in_year = (datetime.datetime(2024, date.month, date.day) - datetime.datetime(2024, 1, 1)).days
    return char_data["daily"][day_in_year]


def name_of_char(id):
    # specifal formatting
    if id == "Mrbrew":
        return "Mr. Brew"

    # other characters
    name = id.title()
    if name[-1] in "0123456789":
        return name[:-1]
    return name


def print_calendar(year):
    date = datetime.datetime(year, 1, 1)
    while date.year == year:
        print(f"{date.month}/{date.day} - {get_char_for_date(date)} - {daily_message(date)}")
        date += datetime.timedelta(days=1)


def ordinal(n: int):  # stolen from stack overflow because i'm lazy
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    return str(n) + suffix


async def setup(bot: commands.Bot):
    await bot.add_cog(DailyCharacter(bot))
