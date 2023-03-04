from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

import aiohttp
import aioping
import discord
from discord.ext import commands, tasks

from utils import embeds
from utils.config import get_config, get_server_name, get_servers

logger = logging.getLogger(__name__)


class Monitor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.retry_count: dict[str, int] = {}
        self.currently_down: dict[str, int] = {}
        self.monitor_uptime.start()
        self.need_to_mention = False
        self.currently_checking = False
        logger.info("Monitor initialized")

    async def cog_unload(self) -> None:
        self.monitor_uptime.cancel()

    def needs_retry(self, server: dict) -> bool:
        retry_count = self.retry_count.get(server["address"], 0)
        if retry_count < get_config("retries"):
            self.retry_count[server["address"]] = retry_count + 1
            return True
        return False

    async def notify_down(
        self, server: dict, channel: discord.TextChannel, reason: str | None
    ) -> None:
        """
        Sends an embed to indicate a service is offline
        :param server: Server object to extract data from
        :param channel: Channel to send the notification to
        :param reason: Reason why the service is down
        """
        if self.needs_retry(server):
            return

        if server["address"] not in self.currently_down:
            logger.info(f'Server {server["address"]} went down')

            self.currently_down.update({server["address"]: 0})
            embed = embeds.Embed(
                title=f"**:red_circle: {get_server_name(server['address'])} is down!**",
                color=16711680,
            )
            embed.add_field(name="Address", value=server["address"], inline=False)
            embed.add_field(name="Type", value=server["type"], inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)

            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                logger.error(
                    "Down notification could not be sent. "
                    "Ensure the bot has permission to sent messages to the specified channel."
                )
            except Exception as e:
                logger.exception(e)

            if self.need_to_mention is False:
                self.need_to_mention = True
        else:
            self.currently_down[server["address"]] = self.currently_down.get(
                server["address"], 0
            ) + get_config("secs_between_ping")

    async def notify_up(self, server: dict, channel: discord.TextChannel) -> None:
        """
        Sends an embed to indicate a service is online
        :param server: Server object to extract data from
        :param channel: Channel to send the notification to
        """
        if server["address"] in self.currently_down:
            logger.info(f'Server {server["address"]} is back online')

            embed = embeds.Embed(
                title=f"**:green_circle: {get_server_name(server['address'])} is up!**",
                color=65287,
            )
            embed.add_field(name="Address", value=server["address"], inline=False)
            embed.add_field(name="Type", value=server["type"], inline=False)
            embed.add_field(
                name="Downtime",
                value=str(timedelta(seconds=self.currently_down[server["address"]])),
                inline=False,
            )

            try:
                await channel.send(embed=embed)
            except discord.Forbidden:
                logger.error(
                    "Up notification could not be sent. "
                    "Ensure the bot has permission to sent messages to the specified channel."
                )
            except Exception as e:
                logger.exception(e)

            if self.need_to_mention is False:
                self.need_to_mention = True

            self.currently_down.pop(server["address"])
            try:
                if self.retry_count is not {}:
                    self.retry_count.pop(server["address"])
            except Exception as e:
                logger.exception(e)
                logger.debug(f"self.retry_count={self.retry_count}")

    @tasks.loop(seconds=get_config("secs_between_ping"))
    async def monitor_uptime(self) -> None:
        """Checks the status of each server and sends up/down notifications"""
        await self.bot.wait_until_ready()

        channel: discord.TextChannel | None = self.bot.get_channel(get_config("notification_channel"))  # type: ignore

        if not channel:
            logger.debug(
                "Skipping scheduled monitoring job, invalid `notification_channel` configured..."
            )
            return

        timeout = get_config("timeout")

        # Make sure the need to mention is set to false everytime this function is ran
        self.need_to_mention = False

        for i in get_servers():
            self.currently_checking = True

            if i["type"] == "ping":
                try:
                    await aioping.ping(i["address"], timeout=timeout)
                except Exception as err:
                    await self.notify_down(i, channel, str(err))
                else:
                    await self.notify_up(i, channel)
            elif i["type"] == "tcp":
                host, port = i["address"].split(":")
                conn = asyncio.open_connection(host, port)
                try:
                    reader, writer = await asyncio.wait_for(conn, timeout)
                    writer.close()
                    await writer.wait_closed()
                except asyncio.TimeoutError:
                    await self.notify_down(i, channel, "Timed out")
                except ConnectionRefusedError:
                    await self.notify_down(i, channel, "Connection failed")
                else:
                    await self.notify_up(i, channel)
            else:
                address = i["address"]

                if not address.startswith("http"):
                    address = f"https://{address}"

                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=timeout)
                ) as session:
                    try:
                        async with session.get(address) as res:
                            if res.ok:
                                await self.notify_up(i, channel)
                            else:
                                await self.notify_down(i, channel, res.reason)
                    except asyncio.TimeoutError:
                        await self.notify_down(i, channel, "Timed out")
                    except aiohttp.ClientError:
                        await self.notify_down(i, channel, "Connection failed")

        self.currently_checking = False
        role_to_mention = get_config("role_to_mention")

        if self.need_to_mention is True and role_to_mention != 0:
            try:
                await channel.send(f"<@&{role_to_mention}>", delete_after=3)
            except discord.Forbidden:
                logger.error(
                    "Mention could not be sent. "
                    "Ensure the bot has permission to sent messages to the specified channel."
                )
            except Exception as e:
                logger.exception(e)

    @commands.command(brief="Checks status of servers being monitored", usage="status")
    async def status(self, ctx: commands.Context) -> None:
        """Make this function asleep if the monitor is currently checking"""
        while self.currently_checking:
            await asyncio.sleep(0.1)

        """Returns an embed showing the status of each monitored server"""
        embed = embeds.Embed(
            title="**Monitor Status**", color=16711680 if self.currently_down else 65287
        )

        for i in get_servers():
            if i["address"] in self.currently_down:
                downtime = str(timedelta(seconds=self.currently_down[i["address"]]))
                embed.add_field(
                    name=f"{i['name']} ({i['type']})",
                    value=f":red_circle: {i['address']} ({downtime})",
                    inline=False,
                )
            else:
                embed.add_field(
                    name=f"{i['name']} ({i['type']})",
                    value=f":green_circle: {i['address']}",
                    inline=False,
                )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Monitor(bot))
