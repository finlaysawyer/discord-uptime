from datetime import timedelta

import discord
from discord.ext import commands

from cogs import monitor
from utils import config as cfg


class Status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Checks status of servers - status")
    async def status(self, ctx):
        """
        :param ctx:
        :return: Embed of the status of each server
        """
        embed = discord.Embed(title="**Monitor Status**", color=16711680 if monitor.currently_down else 65287)

        for i in cfg.servers:
            if i['address'] in monitor.currently_down:
                downtime = str(timedelta(seconds=monitor.currently_down[i['address']]))
                embed.add_field(name=i['name'], value=f":red_circle: {i['address']} ({downtime})", inline=False)
            else:
                embed.add_field(name=i['name'], value=f":green_circle: {i['address']}", inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Status(bot))
