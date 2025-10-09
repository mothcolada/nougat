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
        'channel': 1327524115526979605
    },
    'blog': {
        'link': 'https://nomnomnami.com/blog/resources/main.js',
        'file': 'blog.js',
        'parse': checkweb.parse_blog,
        'channel': 1327524115526979605
    },
    'ask': {
        'link': 'https://nomnomnami.com/ask/latest.html',
        'file': 'ask.html',
        'parse': checkweb.parse_ask,
        'channel': 1330602659023028357
    },
    'status.cafe': {
        'link': 'https://status.cafe/users/nomnomnami.atom',
        'file': 'nomnomnami.atom',
        'parse': checkweb.parse_status_cafe,
        'channel': 1327524115526979605
    },
    'neocities': {
        'link': 'https://neocities.org/site/nomnomnami',
        'file': 'neocities.html',
        'parse': checkweb.parse_neocities,
        'channel': 1327524115526979605
    },
    'trick': {
        'link': 'https://trick.pika.page/posts_feed',
        'file': 'posts_feed.rss',
        'parse': checkweb.parse_trick,
        'channel': 1325920952529457153
    },
}


for s in sources:
    sources[s]['down'] = False


async def check_all():
    for s in sources:
        print('checking: ' + s)
        source = sources[s]
        channel = client.get_channel(1074754885070897202)
        messages = checkweb.check(source)
        for message in messages:
    
            await channel.send(embed   = message['embed'])
            if len(message['files']) >= 1:
                await channel.send(files = message['files'])
        
        await asyncio.sleep(1)  # avoid heartbeat blocking


client = discord.Client(intents=discord.Intents.default())
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    print('Logged in as ' + str(client.user))

    while True:
        await check_all()
        await asyncio.sleep(10)
            
    #await client.close()


load_dotenv()
client.run(os.getenv("TOKEN"))

