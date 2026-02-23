import asyncio
import datetime
import os
import pathlib
import pkgutil
from functools import cached_property

import aiohttp
# import asqlite
import discord
from discord.ext import commands
from dotenv import load_dotenv

# TODO: use database instead of json for nami feeds
# TODO: add more characters to calendar

NOUGAT_ID = 1425561875885719634  # FIXME: Make a configuration option
MOTHCOLADA_ID = 422162909582589963
LOG_CHANNEL = 1425915517184512041

DATABASE_PATH = pathlib.Path(__file__).parent / "database.sqlite"  # FIXME: Make a configuration option

INTENTS = discord.Intents.default()
INTENTS.message_content = True


class Nougat(commands.Bot):
    STARTED_AT: datetime.datetime
    session: aiohttp.ClientSession
    # pool: asqlite.Pool
    user: discord.ClientUser

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

    async def setup_hook(self):
        extensions = [m.name for m in pkgutil.iter_modules(["extensions"], prefix="extensions.") if not m.name.startswith("_")]
        for extension in extensions:
            await self.load_extension(extension)

    async def on_ready(self):
        await self.log(f"good morning world i am {self.user.name}")


    async def log(self, message: str):
        # TODO: Use logging instead of prints
        # TODO: Use a webhook instead of get_channel().send
        print(message)

        channel = self.get_channel(LOG_CHANNEL)

        if not channel:
            raise RuntimeError("could not retrieve log channel")

        await channel.send(message)  # type: ignore -- channel is assumed to support send

    async def report(self, message):
        await self.log(f"<@{MOTHCOLADA_ID}> " + str(message))

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
        await bot.start(os.environ["NOUGAT_TOKEN"])


if __name__ == "__main__":
    asyncio.run(main())
