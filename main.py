import asyncio
import datetime
import os
import pathlib
import pkgutil
from functools import cached_property
import logging

import aiohttp
# import asqlite
import discord
from discord.ext import commands
from dotenv import load_dotenv

# TODO: use database instead of json for nami feeds

NOUGAT_ID = 1425561875885719634
MOTHCOLADA_ID = 422162909582589963
LOG_CHANNEL = 1425915517184512041
MOD_ROLE_ID = 1521632400604397672

NAMIVERSE_GUILD_ID = 1521632400453402732

TAVERN_CHANNEL_TARGETS = {  # every possible sfw channel and its target 18+ channel in Namitavern
    1074754885070897202: 1537552461605249064,  # test
    1521633877859500072: 1537117062416302150,  # nami-news
    1521633846477721680: 1537117062416302150,  # nami-feeds (same target channel as above)
    1521632401334210659: 1537116000212877392   # nami-asks
}
TAVERN_ROLE_TARGETS = {  # every possible role ping and its respective role in Namitavern
    "<@&1539330597577560164>": "<@&1539330623947276288>",  # Test Ping
    "<@&1521632400491417770>": "<@&1537115998442889268>",  # Nami News
    "<@&1521632400453402739>": "<@&1537115998426235060>",  # Nami Feeds
    "<@&1521632400453402738>": "<@&1537115998426235059>"   # Nami Asks
}

DATABASE_PATH = pathlib.Path(__file__).parent / "database.sqlite"

INTENTS = discord.Intents.default()
INTENTS.message_content = True


class Nougat(commands.Bot):
    STARTED_AT: datetime.datetime
    session: aiohttp.ClientSession
    # pool: asqlite.Pool
    user: discord.ClientUser
    log_webhook: discord.Webhook


    def __init__(
        self,
        command_prefix,
        session: aiohttp.ClientSession,
        # pool: asqlite.Pool,
        **options,
    ) -> None:
        super().__init__(command_prefix, **options)
        self.session = session
        # self.pool = pool
        self.STARTED_AT = discord.utils.utcnow()

        self.log_webhook = discord.Webhook.from_url(os.environ["WEBHOOK_URL"], session=session)


    async def setup_hook(self):
        extensions = [m.name for m in pkgutil.iter_modules(["extensions"], prefix="extensions.") if not m.name.startswith("_")]
        for extension in extensions:
            await self.load_extension(extension)


    async def on_ready(self):
        await self.log("good morning world")
        # channel = self.get_channel(1521633846477721680)
        # if isinstance(channel, discord.TextChannel):
        #     message = await channel.fetch_message(1539274757290332272)
        #     print(message.embeds[0].image)
        # await message.edit(content=message.content, embed=embed)
        # await self.close()
        # exit()


    async def on_message(self, message: discord.Message):
        if (message.type == discord.MessageType.auto_moderation_action):
            await message.channel.send(f"<@&{MOD_ROLE_ID}>")


    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        emoji = payload.emoji
        user = payload.member
        if not user:
            return
        channel = self.get_channel(payload.channel_id)
        if not isinstance(channel, discord.TextChannel):
            return
        message = await channel.fetch_message(payload.message_id)

        if user.guild_permissions.manage_messages and message.author.id == self.user.id:  # moderator performing action on nougat message
            # refresh image url of embed
            if emoji.name in "🔄🔃🔁":
                try:
                    await message.remove_reaction(emoji, user)
                except discord.NotFound as e:
                    pass
                await message.edit(content=message.content, embeds=message.embeds)

            # move nami post to namitavern
            if emoji.name == "🔞":
                try:  # will error if channel not found (should not happen)
                    target_channel = self.get_channel(TAVERN_CHANNEL_TARGETS[channel.id])
                    if not isinstance(target_channel, discord.TextChannel):
                        return
                    # replace role pings
                    new_content = message.content
                    for original_role in TAVERN_ROLE_TARGETS:
                        new_content = new_content.replace(original_role, TAVERN_ROLE_TARGETS[original_role])

                    if len(message.attachments) == 0:
                        await target_channel.send(content=new_content, embeds=message.embeds)
                    else:
                        await message.forward(target_channel)

                except:
                    await self.report("move to namitavern failed!")
                finally:  # regardless of error, delete post in sfw channel
                    await message.delete()


    async def log(self, message):
        logging.info(message)
        await self.log_webhook.send(message, username=self.user.name)


    async def report(self, message):
        logging.error(message)
        await self.log_webhook.send(f"<@{MOTHCOLADA_ID}> {message}", username=self.user.name)


    @cached_property
    def is_nougat(self):
        return self.user.id == NOUGAT_ID


async def main():
    load_dotenv()

    async with (
        aiohttp.ClientSession() as session,
        # asqlite.create_pool(str(DATABASE_PATH)) as db_pool,
        Nougat(
            command_prefix=commands.when_mentioned,
            # pool=db_pool,
            session=session,
            intents=INTENTS,
        ) as bot,
    ):
        discord.utils.setup_logging()
        await bot.start(os.environ["TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
