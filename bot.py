import logging
import os
import sys
import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand

from utils.config import get_config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=get_config("prefix"), intents=intents)
logging.basicConfig(
    format="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

class DiscordUptime(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=get_config("prefix"),
            description="Bot to monitor uptime of services",
            reconnect=True,
            intents=intents,
            activity=discord.Activity(
                type=getattr(discord.ActivityType, get_config("activity_type").lower()),
                name=get_config("activity_name"),
            ),
            help_command=DefaultHelpCommand()
            if not get_config("disable_help")
            else None,
        )
        self.bot = bot

    async def on_ready(self):
        logging.info("Logged in as %s", self.user)

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py") and not filename.startswith("__"):
                await self.load_extension(f"cogs.{filename[:-3]}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument)):
            return await ctx.send(error)
        return

async def main():
    await DiscordUptime().start(get_config("token"))

if __name__ == "__main__":
    asyncio.run(main())
