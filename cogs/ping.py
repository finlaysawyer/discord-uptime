import asyncio

import aiohttp
from discord import Interaction, app_commands
from discord.ext import commands
from discord.utils import escape_mentions
from icmplib import ICMPLibError

from checks.ping import ping
from utils.config import get_config
from utils.embeds import CheckType, Status, generate_status_embed


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(description="Pings an address")
    async def ping(self, interaction: Interaction, address: str) -> None:
        """
        Pings an address via icmplib
        :param interaction: Discord interaction
        :param address: Address to ping
        :return: Embed message containing status of service
        """
        await interaction.response.send_message("Pinging...")
        address = escape_mentions(address)

        try:
            ping_request = await ping(address)
        except ICMPLibError as err:
            status = Status.DOWN
            embed_fields: list[dict] = [{"name": "Reason", "value": str(err)}]
        else:
            # If no packets could be sent or packet loss was encountered,
            # consider the service down
            if ping_request.packet_loss > 0 or ping_request.packets_sent == 0:
                status = Status.DOWN
            else:
                status = Status.UP

            embed_fields = [
                {
                    "name": "Packets received",
                    "value": f"{ping_request.packets_sent} / {ping_request.packets_received}",
                    "inline": False,
                },
                {
                    "name": "Packet loss",
                    "value": f"{ping_request.packet_loss:.0%}",
                    "inline": False,
                },
                {
                    "name": "Round-trip time",
                    "value": f"Minimum: {ping_request.min_rtt}ms"
                    f"\nAverage: {ping_request.avg_rtt}ms"
                    f"\nMaximum: {ping_request.max_rtt}ms",
                    "inline": False,
                },
            ]

        await interaction.edit_original_response(
            content=None,
            embed=generate_status_embed(
                status,
                CheckType.PING,
                address,
                fields=embed_fields,
            ),
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
