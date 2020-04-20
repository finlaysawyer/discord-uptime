from discord.ext import commands
from ping3 import ping
import asyncio


class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Pings an address - ping <address> [pings]")
    async def ping(self, ctx, address: str, pings: int = 1):
        """
        :param ctx:
        :param address: Address to ping
        :param pings: Number of pings
        :return: Delay in milliseconds or error
        """
        if ping(address) is False:
            await ctx.send(f"Could not ping {address} - unknown host.")
        elif ping(address) is None:
            await ctx.send(f"Could not ping {address} - timed out.")
        else:
            for i in range(pings):
                await ctx.send(f"Received response from {address} in: {str(int(ping(address, unit='ms')))}ms.")
                await asyncio.sleep(1)


def setup(bot):
    bot.add_cog(Ping(bot))
