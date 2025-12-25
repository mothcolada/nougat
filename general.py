import discord


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


async def log(message):
    print(message)
    log_channel = client.get_channel(1425915517184512041)  # my #nougat-log channel
    await log_channel.send(message)


async def report(message):  # i simplified this massively because i don't think it ended up being useful how it was
    await log('<@422162909582589963> ' + message)


def is_nougat():
    return (client.user.id == 1425561875885719634)


def get_guild():
    if is_nougat():
        return client.get_guild(1325038200452022334)  # namiverse
    else:
        return client.get_guild(422163243528617994)  # bea hive
