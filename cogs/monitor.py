import asyncio
from datetime import timedelta

import aiohttp
import discord
from discord.ext import tasks, commands
from ping3 import ping

from utils.config import get_config, get_servers


class Monitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.currently_down = {}
        self.monitor_uptime.start()

    def cog_unload(self):
        self.monitor_uptime.cancel()

    async def notify_down(
        self, server: object, channel: discord.TextChannel, reason: str
    ) -> None:
        """
        Sends an embed to indicate a service is offline
        :param server: Server object to extract data from
        :param channel: Channel to send the notification to
        :param reason: Reason why the service is down
        """
        if server["address"] not in self.currently_down:
            self.currently_down.update({server["address"]: 0})
            embed = discord.Embed(
                title=f"**:red_circle:  {server['address']} is down!**", color=16711680
            )
            embed.add_field(name="Address", value=server["address"], inline=False)
            embed.add_field(name="Type", value=server["type"], inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            await channel.send(embed=embed)
            await channel.send(f"<@&{get_config('role_to_mention')}>", delete_after=3)
        else:
            self.currently_down[server["address"]] = self.currently_down.get(
                server["address"], 0
            ) + get_config("secs_between_ping")

    async def notify_up(self, server: object, channel: discord.TextChannel) -> None:
        """
        Sends an embed to indicate a service is online
        :param server: Server object to extract data from
        :param channel: Channel to send the notification to
        """
        if server["address"] in self.currently_down:
            embed = discord.Embed(
                title=f"**:green_circle:  {server['name']} is up!**", color=65287
            )
            embed.add_field(name="Address", value=server["address"], inline=False)
            embed.add_field(name="Type", value=server["type"], inline=False)
            embed.add_field(
                name="Downtime",
                value=str(timedelta(seconds=self.currently_down[server["address"]])),
                inline=False,
            )
            await channel.send(embed=embed)
            await channel.send(f"<@&{get_config('role_to_mention')}>", delete_after=3)
            self.currently_down.pop(server["address"])

    @tasks.loop(seconds=get_config("secs_between_ping"))
    async def monitor_uptime(self) -> None:
        """Checks the status of each server and sends up/down notifications"""
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(get_config("notification_channel"))

        for i in get_servers():
            if i["type"] == "ping":
                if ping(i["address"]) is False:
                    await self.notify_down(i, channel, "Host unknown")
                elif ping(i["address"]) is None:
                    await self.notify_down(i, channel, "Timed out")
                else:
                    await self.notify_up(i, channel)
            else:
                address = i["address"]
                timeout = get_config("http_timeout")

                if not address.startswith("http"):
                    address = f"http://{address}"

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

    @commands.command(brief="Checks status of servers being monitored", usage="status")
    async def status(self, ctx) -> None:
        """Returns an embed showing the status of each monitored server"""
        embed = discord.Embed(
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


def setup(bot):
    bot.add_cog(Monitor(bot))
