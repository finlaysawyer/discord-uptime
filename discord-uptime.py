from ping3 import ping
import discord
from discord.ext import commands
import time
import bot_cfg

bot = commands.Bot(command_prefix='>', description='Bot to monitor uptime of services')


@bot.event
async def on_ready():
    print('Logged in as {0}'.format(bot.user))
    print('---------------------------------')
    await bot.change_presence(activity=discord.Game('{0} guilds'.format(len(list(bot.guilds)))))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.CommandNotFound, commands.BadArgument, commands.MissingRequiredArgument)):
        return await ctx.send(error)
    else:
        return


@bot.command()
async def joined(ctx, member: discord.Member):
    """
    :param ctx: Context
    :param member: Discord tag
    :return: Date when a member joined
    """
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))


@bot.command()
async def status(ctx, address: str):
    """
    :param ctx: Context
    :param address: Address to ping
    :return: Delay in milliseconds
    """
    await ctx.send('Received response from {0} in: '.format(address) + str(int(ping(address, unit='ms'))) + 'ms')


@bot.command()
async def status_multi(ctx, address: str, pings: int):
    """
    :param ctx: Context
    :param address: Address to ping
    :param pings: Number of pings
    :return: Delay in milliseconds for amount of pings specified
    """
    await ctx.send('Pinging {0} {1} times'.format(address, pings))
    for num in range(pings):
        await ctx.send('Received response from {0} in: '.format(address) + str(int(ping(address, unit='ms'))) + 'ms')
        time.sleep(1)

bot.run(bot_cfg.token)
