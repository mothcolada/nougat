import json
import datetime
import math

import general
from general import client


# TODO: face randomization maybe

char_data = json.load(open('char_data.json', 'r'))


async def run():
    offset = datetime.timedelta(hours=-7)
    mst = datetime.timezone(offset)
    now_mst = datetime.datetime.now(tz=mst)

    # check 1: only continue if it has been at least a day since last scheduled change
    since_last_changed = now_mst - datetime.datetime.fromtimestamp(char_data['last_changed'], tz=mst)
    if since_last_changed < datetime.timedelta(days=1):
        return

    char = get_char_for_date(now_mst)
    new_icon = open(f'faces/{char}.png', 'rb').read()
    server = general.get_guild()

    # check 2: compare bytes of current icon and the icon we want to change it to, only continue if different
    current_icon = await server.icon.read()
    if new_icon == current_icon:
        await general.log('same icon')
        return
    await general.log('different icon')
    # check 1 is enough in a vacuum, but with me pushing updates, check 2 is an extra failsafe
    # to not accidentally ping for a character who is already the icon

    await server.edit(icon=new_icon)

    if general.is_nougat():
        channel = client.get_channel(1330485605515264030)  # Daily Character thread
    else:
        channel = client.get_channel(1074754885070897202)  # personal testing channel
    await channel.send(daily_message(now_mst))

    # round time to most recent MST midnight
    rounded_time = math.floor((now_mst.timestamp() + offset.total_seconds()) / 86400) * 86400 - offset.total_seconds()
    char_data['last_changed'] = rounded_time

    json.dump(char_data, open('char_data.json', 'w'), indent=4)


def daily_message(date: datetime.datetime):
    message = '<@&1330488425006239797> '

    # "Treat!" or "Happy birthday, Treat!"
    day = f'{date.month}/{date.day}'
    if day in char_data['birthdays']:
        message += 'Happy birthday, '
    message += name_of_char(get_char_for_date(date)) + '!'

    # "Happy 10th anniversary to Lonely Wolf Treat!"
    if day in char_data['anniversaries'].keys():
        anniversaries = char_data['anniversaries'][day]
        for anniversary in anniversaries:
            game_age = date.year - anniversary['year']
            message += f' Happy {ordinal(game_age)} anniversary to {anniversary['game']}!'

    return message


def get_char_for_date(date: datetime.datetime):
    # 2024 is a year with a leap day, calendar includes leap day for when it happens
    day_in_year = (datetime.datetime(2024, date.month, date.day) - datetime.datetime(2024, 1, 1)).days
    return char_data['calendar'][day_in_year]


def name_of_char(id):
    name = id.title()
    if name[-1] in '0123456789':
        return name[:-1]
    return name


def print_calendar(year):
    date = datetime.datetime(year, 1, 1)
    while date.year == year:
        print(f'{date.month}/{date.day} - {daily_message(date)}')
        date += datetime.timedelta(days=1)


def ordinal(n: int):  # stolen from stack overflow because i'm lazy
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix
