import discord
from bs4 import BeautifulSoup
import asyncio
import json
import checkweb
import os
from dotenv import load_dotenv


load_dotenv() # load .env so we can use bot token

sources = {
    'posts': {
        'link': 'https://nomnomnami.com/posts/index.html',
        'file': 'posts.html',
        'parse': checkweb.parse_posts,
        'channel': 1327524115526979605,
        'message': ''
    },
    'blog': {
        'link': 'https://nomnomnami.com/blog/resources/main.js',
        'file': 'blog.js',
        'parse': checkweb.parse_blog,
        'channel': 1327524115526979605,
        'message': ''
    },
    'ask': {
        'link': 'https://nomnomnami.com/ask/latest.html',
        'file': 'ask.html',
        'parse': checkweb.parse_ask,
        'channel': 1330602659023028357,
        'message': ''
    },
    'status.cafe': {
        'link': 'https://status.cafe/users/nomnomnami.atom',
        'file': 'nomnomnami.atom',
        'parse': checkweb.parse_status_cafe,
        'channel': 1327524115526979605,
        'message': ''
    },
    'neocities': {
        'link': 'https://neocities.org/site/nomnomnami',
        'file': 'neocities.html',
        'parse': checkweb.parse_neocities,
        'channel': 1327524115526979605,
        'message': ''
    },
    'trick': {
        'link': 'https://trick.pika.page/posts_feed',
        'file': 'trick.rss',
        'parse': checkweb.parse_trick,
        'channel': 1325920952529457153,
        'message': ''
    },
}


for s in sources:
    sources[s]['issue'] = False


async def report_status(s,ex,i):  # the sexi report system (source, exception, and issue) (clear )
    try:  # if anything goes wrong, tell me (mothcolada)
        channel = client.get_channel(1425915517184512041)
        if i:  # issue!
            await channel.send(content = '<@422162909582589963> ' + str(s) + ' ' + str(ex))
        else:
            await channel.send(content = str(s) + ' ' + str(ex))
    except:  # uhhhhhhhhh
        print('uh oh')
        print(str(s) + ' ' + str(ex))


async def check_all():
    for s in sources:
        source = sources[s]
        try:
            if str(client.user) == 'Nougat#2777':  # in namiverse act normally
                channel = client.get_channel(source['channel'])
            else:  # personal test bot
                channel = client.get_channel(1074754885070897202)
            
            messages = checkweb.check(source)
            for message in messages:
                await channel.send(source['message'], embed = message['embed'])
                if len(message['files']) >= 1:  # i'll (situationally) put images in the embed later
                    await channel.send(files = message['files'])
            
            # report if issue was happening but it works now
            if source['issue']:
                source['issue'] = False
                await report_status(s, 'we did it reddit', source['issue'])
        except Exception as e: # report if an issue happens
            if not source['issue']:
                source['issue'] = True
                await report_status(s, e, source['issue'])
        await asyncio.sleep(1)  # avoid heartbeat blocking


# THE BOT!!!!!

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    # start
    print('Logged in as ' + str(client.user))
    channel = client.get_channel(1074754885070897202)
    await channel.send('i get up!')

    # loop: constantly check all sources
    while True:
        await check_all()
        await asyncio.sleep(10)
            
    # await client.close()

load_dotenv()
client.run(os.getenv("TOKEN"))

