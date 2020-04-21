from discord.ext import commands
from utils import config as cfg
import os

bot = commands.Bot(command_prefix=cfg.config['prefix'], description='Bot to monitor uptime of services')


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.CommandNotFound, commands.BadArgument, commands.MissingRequiredArgument)):
        return await ctx.send(error)
    else:
        return

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(cfg.config['token'])
