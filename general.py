import discord


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def log(message):
    print(message)
    log_channel = client.get_channel(1425915517184512041)  # my #nougat-log channel
    await log_channel.send(message)


async def report(s,ex,i):  # the sexi report system (source, exception, and issue) (useful variable naming be damned)
    try:  # if anything goes wrong, tell me (mothcolada)
        if i:  # issue!
            await log(content = '<@422162909582589963> ' + str(s) + ' ' + str(ex))
        else:
            await log(content = str(s) + ' ' + str(ex))
    except:  # uhhhhhhhhh
        print('uh oh ' + str(s) + ' ' + str(ex))
