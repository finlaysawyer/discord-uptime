import asyncio

import aiohttp
import aioping
from discord.ext import commands
from discord.utils import escape_mentions

from utils.config import get_config


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(brief="Pings an address", usage="ping <address> [pings]")
    async def ping(self, ctx: commands.Context, address: str, pings: int = 1) -> None:
        """
        Pings an address once or multiple times
        :param ctx: commands.Context
        :param address: Address to ping
        :param pings: Number of pings
        :return: Delay in milliseconds or error
        """
        timeout = get_config("timeout")
        address = escape_mentions(address)

        for _ in range(pings):
            try:
                ping_request = await aioping.ping(address, timeout=timeout)
            except Exception as err:
                await ctx.send(f"Could not ping {address} - {str(err)}")
            else:
                await ctx.send(f"Received response from {address} in: {ping_request}s.")
            await asyncio.sleep(1)

    @commands.command(brief="Checks a TCP port", usage="tcp <address> <port>")
    async def tcp(self, ctx: commands.Context, address: str, port: int) -> None:
        """
        Checks if a TCP port on a remote host is open for connections
        :param ctx: commands.Context
        :param address: Address of host
        :param port: Port to connect to
        :return: Delay in milliseconds or error
        """
        timeout = get_config("timeout")
        address = escape_mentions(address)

        conn = asyncio.open_connection(address, port)
        try:
            reader, writer = await asyncio.wait_for(conn, timeout)
            await ctx.send(f"Connection established on {address}:{port}")
            writer.close()
            await writer.wait_closed()
        except asyncio.TimeoutError:
            await ctx.send(f"Request timed out after {timeout} seconds")
        except ConnectionRefusedError:
            await ctx.send(f"Could not establish a connection to {address}:{port}")

    @commands.command(brief="Performs an HTTP request", usage="http <address>")
    async def http(self, ctx: commands.Context, address: str) -> None:
        """
        Performs an HTTP request to the specified address
        :param ctx: commands.Context
        :param address: Address to make request to
        :return: HTTP status code
        """
        if not address.startswith("http"):
            address = f"https://{address}"

        timeout = get_config("timeout")
        address = escape_mentions(address)

        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout)
        ) as session:
            try:
                async with session.get(address) as res:
                    await ctx.send(
                        f"Received response code: {res.status} ({res.reason})"
                    )
            except asyncio.TimeoutError:
                await ctx.send(f"Request timed out after {timeout} seconds")
            except aiohttp.ClientError:
                await ctx.send(f"Could not establish a connection to {address}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
