from discord.ext import commands

from main import Nougat


class Dev(commands.Cog):
    def __init__(self, bot: Nougat):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def die(self, ctx: commands.Context):
        await ctx.send("good night")
        await self.bot.close()


async def setup(bot: Nougat):
    await bot.add_cog(Dev(bot))
