import discord
from bs4 import BeautifulSoup
import asyncio
import json
import checkweb
import os
from dotenv import load_dotenv


load_dotenv() # load .env so we can use bot token

sources = {
    # 'posts': {
    #     'link': 'https://nomnomnami.com/posts/index.html',
    #     'file': 'posts.html',
    #     'parse': checkweb.parse_posts,
    # },
    # 'blog': {
    #     'link': 'https://nomnomnami.com/blog/resources/main.js',
    #     'file': 'blog.js',
    #     'parse': checkweb.parse_blog
    # },
    # 'ask': {
    #     'link': 'https://nomnomnami.com/ask/latest.html',
    #     'file': 'ask.html',
    #     'parse': checkweb.parse_ask
    # },
    # 'status.cafe': {
    #     'link': 'https://status.cafe/users/nomnomnami.atom',
    #     'file': 'nomnomnami.atom',
    #     'parse': checkweb.parse_status_cafe
    # },
    # 'neocities': {
    #     'link': 'https://neocities.org/site/nomnomnami',
    #     'file': 'neocities.html',
    #     'parse': checkweb.parse_neocities
    # },
    'trick': {
        'link': 'https://trick.pika.page/posts_feed',
        'file': 'posts_feed.rss',
        'parse': checkweb.parse_trick
    },
}

# data = json.load(open('data.json', 'r'))

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

    await tree.sync(guild=client.get_guild(422163243528617994))
    print('SYNCED')

    # while True:
    await check_all()
    await asyncio.sleep(10)
            
    #await client.close()


@client.event
async def on_message(message: discord.Message):
    if message.content == 'kys':
        await message.channel.send('oh ok')
        await client.close()


@tree.command(name='hello', description='uisakdjkd')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message('DIE', ephemeral=True)

@tree.command(name='setchannel', description='uisakdjkd')
async def setchannel(interaction: discord.Interaction):
    await interaction.response.send_message('DIE')

@tree.command(name='setmessage', description='yea')
async def setmessage(interaction: discord.Interaction):
    await interaction.response.send_message('ok')

@tree.command(name='info', description='okasyd')
async def info(interaction: discord.Interaction):
    await interaction.response.send_message('DIE')


load_dotenv()

#client.run(os.getenv("TOKEN"))


print(os.getenv("TOKEN"))


messages = checkweb.check(sources['trick'])
for message in messages:
    print(message['embed'].description)
