from discord.ext import tasks, commands
from ping3 import ping
from utils import config as cfg
import discord

currently_down = []


async def notify_down(name, address, channel, reason):
    if address not in currently_down:
        currently_down.append(address)
        embed = discord.Embed(
            title=f"**{name} is down!**",
            color=discord.Color.red()
        )
        embed.add_field(name="Address", value=address, inline=False)
        embed.add_field(name="Reason", value=reason, inline=False)
        await channel.send(embed=embed)
        await channel.send(f"<@&{cfg.config['role_to_mention']}>", delete_after=3)


async def notify_up(name, address, channel):
    if address in currently_down:
        embed = discord.Embed(
            title=f"**{name} is up!**",
            color=discord.Color.green()
        )
        embed.add_field(name="Address", value=address, inline=False)
        await channel.send(embed=embed)
        await channel.send(f"<@&{cfg.config['role_to_mention']}>", delete_after=3)
        currently_down.remove(address)


class Monitor(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.monitor_uptime.start()

    def cog_unload(self):
        self.monitor_uptime.cancel()

    @tasks.loop(seconds=cfg.config['secs_between_ping'])
    async def monitor_uptime(self):
        await self.bot.wait_until_ready()

        channel = self.bot.get_channel(cfg.config['notification_channel'])

        for i in cfg.servers:
            if ping(i["address"]) is False:
                await notify_down(i['name'], i["address"], channel, "Host unknown")
            elif ping(i["address"]) is None:
                await notify_down(i['name'], i["address"], channel, "Timed out")
            else:
                await notify_up(i['name'], i["address"], channel)


def setup(bot):
    bot.add_cog(Monitor(bot))
