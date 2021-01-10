from datetime import timedelta

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
        self, name: str, address: str, channel: discord.TextChannel, reason: str
    ) -> None:
        """
        Sends an embed to indicate a service is offline
        :param name: User-friendly name of the service
        :param address: Address of the service
        :param channel: Channel to send the notification to
        :param reason: Reason why the service is down
        """
        if address not in self.currently_down:
            self.currently_down.update({address: 0})
            embed = discord.Embed(
                title=f"**:red_circle:  {name} is down!**", color=16711680
            )
            embed.add_field(name="Address", value=address, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            await channel.send(embed=embed)
            await channel.send(f"<@&{get_config('role_to_mention')}>", delete_after=3)
        else:
            self.currently_down[address] = self.currently_down.get(
                address, 0
            ) + get_config("secs_between_ping")

    async def notify_up(
        self, name: str, address: str, channel: discord.TextChannel
    ) -> None:
        """
        Sends an embed to indicate a service is online
        :param name: User-friendly name of the service
        :param address: Address of the service
        :param channel: Channel to send the notification to
        """
        if address in self.currently_down:
            embed = discord.Embed(
                title=f"**:green_circle:  {name} is up!**", color=65287
            )
            embed.add_field(name="Address", value=address, inline=False)
            embed.add_field(
                name="Downtime",
                value=str(timedelta(seconds=self.currently_down[address])),
                inline=False,
            )
            await channel.send(embed=embed)
            await channel.send(f"<@&{get_config('role_to_mention')}>", delete_after=3)
            self.currently_down.pop(address)

    @tasks.loop(seconds=get_config("secs_between_ping"))
    async def monitor_uptime(self) -> None:
        """Checks the status of each server and sends up/down notifications"""
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(get_config("notification_channel"))

        for i in get_servers():
            if ping(i["address"]) is False:
                await self.notify_down(i["name"], i["address"], channel, "Host unknown")
            elif ping(i["address"]) is None:
                await self.notify_down(i["name"], i["address"], channel, "Timed out")
            else:
                await self.notify_up(i["name"], i["address"], channel)

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
                    name=i["name"],
                    value=f":red_circle: {i['address']} ({downtime})",
                    inline=False,
                )
            else:
                embed.add_field(
                    name=i["name"], value=f":green_circle: {i['address']}", inline=False
                )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Monitor(bot))
