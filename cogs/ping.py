import asyncio

import aiohttp
from discord.ext import commands
from ping3 import ping


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Pings an address", usage="ping <address> [pings]")
    async def ping(self, ctx, address: str, pings: int = 1) -> None:
        """
        Pings an address once or multiple times
        :param ctx: commands.Context
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
                await ctx.send(
                    f"Received response from {address} in: {str(int(ping(address, unit='ms')))}ms."
                )
                await asyncio.sleep(1)

    @commands.command(brief="Performs a HTTP request", usage="http <address>")
    async def http(self, ctx, address: str) -> None:
        """
        Performs a HTTP request to the specified address
        :param ctx: commands.Context
        :param address: Address to make request to
        :return: HTTP status code
        """
        if not address.startswith('http'):
            address = f'http://{address}'

        async with aiohttp.ClientSession() as session:
            async with session.get(address) as res:
                await ctx.send(f"Recieved response code: {res.status} ({res.reason})")


def setup(bot):
    bot.add_cog(Ping(bot))
