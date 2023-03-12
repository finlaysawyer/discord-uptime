from __future__ import annotations

import asyncio
import logging
import sys

import discord
from discord.ext import commands

from utils.config import get_config

logging.basicConfig(
    format="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True

COGS = (
    "ping",
    # "tcp",
    # "http",
    # "monitor",
)


class DiscordUptime(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=get_config("prefix"),
            description="Bot to monitor uptime of services",
            reconnect=True,
            intents=intents,
            activity=discord.Activity(
                type=getattr(discord.ActivityType, get_config("activity_type").lower()),
                name=get_config("activity_name"),
            ),
            help_command=commands.DefaultHelpCommand()
            if not get_config("disable_help")
            else None,
        )

    async def setup_hook(self) -> None:
        for cog in COGS:
            await self.load_extension(f"cogs.{cog}")

        guild = discord.Object(id=get_config("guild_id"))
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

    async def on_ready(self) -> None:
        logger.info(f"Logged in as {self.user}")

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        if isinstance(error, (commands.BadArgument, commands.MissingRequiredArgument)):
            await ctx.send(str(error))
        return None


async def main() -> None:
    await DiscordUptime().start(get_config("token"))


if __name__ == "__main__":
    asyncio.run(main())
