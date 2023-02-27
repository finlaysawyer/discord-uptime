import asyncio

import aiohttp
import aioping
from discord import Interaction, app_commands
from discord.ext import commands
from discord.utils import escape_mentions

from utils.config import get_config


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(description="Pings an address")
    async def ping(self, interaction: Interaction, address: str) -> None:
        """
        Pings an address once or multiple times
        :param interaction: Discord Interaction
        :param address: Address to ping
        :return: Delay in milliseconds or error
        """
        timeout = get_config("timeout")
        address = escape_mentions(address)

        try:
            ping_request = await aioping.ping(address, timeout=timeout)
        except Exception as err:
            await interaction.response.send_message(
                f"Could not ping {address} - {str(err)}"
            )
        else:
            await interaction.response.send_message(
                f"Received response from {address} in: {ping_request}s."
            )

    @app_commands.command(description="Checks a TCP port")
    async def tcp(self, interaction: Interaction, address: str, port: int) -> None:
        """
        Checks if a TCP port on a remote host is open for connections
        :param interaction: Discord Interaction
        :param address: Address of host
        :param port: Port to connect to
        :return: Delay in milliseconds or error
        """
        timeout = get_config("timeout")
        address = escape_mentions(address)

        conn = asyncio.open_connection(address, port)
        try:
            reader, writer = await asyncio.wait_for(conn, timeout)
            await interaction.response.send_message(
                f"Connection established on {address}:{port}"
            )
            writer.close()
            await writer.wait_closed()
        except asyncio.TimeoutError:
            await interaction.response.send_message(
                f"Request timed out after {timeout} seconds"
            )
        except ConnectionRefusedError:
            await interaction.response.send_message(
                f"Could not establish a connection to {address}:{port}"
            )

    @app_commands.command(description="Performs an HTTP request")
    async def http(self, interaction: Interaction, address: str) -> None:
        """
        Performs an HTTP request to the specified address
        :param interaction: Discord Interaction
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
                    await interaction.response.send_message(
                        f"Received response code: {res.status} ({res.reason})"
                    )
            except asyncio.TimeoutError:
                await interaction.response.send_message(
                    f"Request timed out after {timeout} seconds"
                )
            except aiohttp.ClientError:
                await interaction.response.send_message(
                    f"Could not establish a connection to {address}"
                )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ping(bot))
