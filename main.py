import discord
import asyncio
import os
from dotenv import load_dotenv

import general
from general import client
import feeds
import character


character.print_calendar(2026)

@client.event
async def on_ready():
    await general.log(f'good morning world i am {client.user.name}')

    # loop: constantly check all sources
    while True:
        try: await character.run()
        except Exception as e: await general.report(e)
    
        try: await feeds.run()
        except Exception as e: await general.report(e)
        
        await asyncio.sleep(10)


@client.event
async def on_message(message: discord.Message):
    # if i send "die" in my #nougat-log channel, shut down the bot
    if message.author.id == 422162909582589963 and message.channel.id == 1425915517184512041 and message.content == 'die':
        await general.log('good night')
        await client.close()


load_dotenv()
client.run(os.getenv('TOKEN'))

