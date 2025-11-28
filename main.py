import discord
from bs4 import BeautifulSoup
import asyncio
import json
import checkweb
import os
from dotenv import load_dotenv


sources = json.load(open('data.json', 'r'))
for s in sources:
    sources[s]['issue'] = False


async def log(message):
    print(message)
    log_channel = client.get_channel(1425915517184512041)  # my #nougat-log channel
    await log_channel.send(message)


async def report_status(s,ex,i):  # the sexi report system (source, exception, and issue) (useful variable naming be damned)
    try:  # if anything goes wrong, tell me (mothcolada)
        if i:  # issue!
            await log(content = '<@422162909582589963> ' + str(s) + ' ' + str(ex))
        else:
            await log(content = str(s) + ' ' + str(ex))
    except:  # uhhhhhhhhh
        print('uh oh ' + str(s) + ' ' + str(ex))


async def check(source):
    if str(client.user) == 'Nougat#2777':  # in namiverse use namiverse channels
        channel = client.get_channel(source['channel'])
    else:  # personal test bot
        channel = client.get_channel(1074754885070897202)

    # get all the messages to send
    messages = checkweb.check(source)
    if (len(messages) > 3 and not source['name'] == 'ask') or len(messages) > 10:  # prevent spam pings if a bug happens that makes it detect 4+ new messages from one source at once
        raise Exception('too many messages to send')

    for message in messages:
        await channel.send(message['content'], embed=message['embed'])
        if 'images' in message.keys() and len(message['images']) >= 1:  # i'll (situationally) put images in the embed later
            await channel.send(files=message['images'])


async def check_all():
    global sources
    for s in sources:
        if s in ['trick', 'posts', 'status_cafe', 'ask']:
            source = sources[s]
            try:
                await check(source)
                
                # save new stuff
                json.dump(sources, open('data.json', 'w'), indent=4)
                # report if issue was happening but it works now
                if source['issue']:
                    source['issue'] = False
                    await report_status(s, 'we did it reddit', source['issue'])

            except Exception as e:
                # reload
                sources = json.load(open('data.json', 'r'))
                # report if an issue happens
                if not source['issue']:
                    source['issue'] = True
                    await report_status(s, e, source['issue'])
            
            await asyncio.sleep(1)  # avoid heartbeat blocking


# THE BOT!!!!!

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # start
    await log(f'good morning world i am {str(client.user)}')

    # loop: constantly check all sources
    while True:
        await check_all()
        await asyncio.sleep(10)


@client.event
async def on_message(message: discord.Message):
    # if i send "die" in my #nougat-log channel, shut down the bot
    if message.author.id == 422162909582589963 and message.channel.id == 1425915517184512041 and message.content == 'die':
        await log('good night')
        await client.close()


load_dotenv()  # load .env so we can use bot token
client.run(os.getenv("TOKEN"))

