import discord
import asyncio
import os
from dotenv import load_dotenv

import general
from general import client
import feeds
import starboard
import character


@client.event
async def on_ready():
    await general.log(f'good morning world i am {client.user.name}')

    # loop: constantly check all sources
    await starboard.refresh_all()
    while True:
        await feeds.run()
        await asyncio.sleep(3)
        # await character.run()
        # await asyncio.sleep(3)


@client.event
async def on_message(message: discord.Message):
    # if i send "die" in my #nougat-log channel, shut down the bot
    if message.author.id == 422162909582589963 and message.channel.id == 1425915517184512041 and message.content == 'die':
        await general.log('good night')
        await client.close()


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    if reaction.emoji.name == 'star':
        await starboard.add_star(reaction, user)


@client.event
async def on_reaction_remove(reaction: discord.Reaction, user: discord.Member):
    if reaction.emoji.name == 'star':
        await starboard.remove_star(reaction, user)


load_dotenv()
client.run(os.getenv("NOUGAT_TOKEN"))

