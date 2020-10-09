from discord import Intents
from discord.ext import commands
from utils import config as cfg
import os

bot = commands.Bot(command_prefix=cfg.config['prefix'])


class DiscordUptime(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=cfg.config['prefix'],
                         description='Bot to monitor uptime of services',
                         reconnect=True,
                         intents=Intents.default())
        self.bot = bot

    async def on_ready(self):
        print(f"Logged in as {self.user}")

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.load_extension(f'cogs.{filename[:-3]}')

    async def on_command_error(self, ctx, error):
        if isinstance(error, (commands.CommandNotFound, commands.BadArgument, commands.MissingRequiredArgument)):
            return await ctx.send(error)
        else:
            return


DiscordUptime().run(cfg.config["token"])
