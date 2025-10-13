import discord
from bs4 import BeautifulSoup
import asyncio
import json
import checkweb
import os
from dotenv import load_dotenv


sources = {
    'home': {
        'link': 'https://nomnomnami.com/index.html',
        'file': 'announcements.html',
        'parse': checkweb.parse_announcements,
        'channel': 1327524115526979605,
        'message': '## New announcement! <@&1325598062198128640>'
    },
    'newsfeed': {
        'link': 'https://nomnomnami.com/index.html',
        'file': 'newsfeed.html',  # yes im downloading the same thing twice to different files its just easier that way idk
        'parse': checkweb.parse_newsfeed,
        'channel': 1327524115526979605,
        'message': '### New news! <@&1327524420033712173>'
    },
    'posts': {
        'link': 'https://nomnomnami.com/posts/index.html',
        'file': 'posts.html',
        'parse': checkweb.parse_posts,
        'channel': 1327524115526979605,
        'message': '### New post! <@&1327524420033712173>'
    },
    'blog': {
        'link': 'https://nomnomnami.com/blog/resources/main.js',
        'file': 'blog.js',
        'parse': checkweb.parse_blog,
        'channel': 1327524115526979605,
        'message': '### New blog post! <@&1327524420033712173>'
    },
    'ask': {
        'link': 'https://nomnomnami.com/ask/latest.html',
        'file': 'ask.html',
        'parse': checkweb.parse_ask,
        'channel': 1330602659023028357,
        'message': '### New ask! <@&1427133678173294654>'
    },
    'status.cafe': {
        'link': 'https://status.cafe/users/nomnomnami.atom',
        'file': 'nomnomnami.atom',
        'parse': checkweb.parse_status_cafe,
        'channel': 1327524115526979605,
        'message': '### New status! <@&1327524420033712173>'
    },
    'neocities': {
        'link': 'https://neocities.org/site/nomnomnami',
        'file': 'neocities.html',
        'parse': checkweb.parse_neocities,
        'channel': 1327524115526979605,
        'message': '### New Neocities update! <@&1327524420033712173>'
    },
    'trick': {
        'link': 'https://trick.pika.page/posts_feed',
        'file': 'trick.rss',
        'parse': checkweb.parse_trick,
        'channel': 1325920952529457153,
        'message': '### New Letter from Trick! <@&1327518346178203670>'
    },
}

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


async def check_all():
    for s in sources:
        source = sources[s]
        try:
            if str(client.user) == 'Nougat#2777':  # in namiverse use namiverse channels
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

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # start
    print('Logged in as ' + str(client.user))
    await log('good morning')


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

