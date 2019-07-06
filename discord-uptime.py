from ping3 import ping
from discord.ext import commands
import discord
import asyncio
import json


bot = commands.Bot(command_prefix='>', description='Bot to monitor uptime of services')


with open('servers.json') as f:
    servers = json.load(f)

with open('config.json') as f:
    config = json.load(f)


@bot.event
async def on_ready():
    print('Logged in as {0}'.format(bot.user))
    print('---------------------------------')
    await bot.change_presence(activity=discord.Game('{0} guilds'.format(len(list(bot.guilds)))))


async def monitor_uptime():
    await bot.wait_until_ready()
    channel = bot.get_channel(config['notification_channel'])

    while not bot.is_closed():
        for i in servers:
            if ping(i["address"]) is None:
                embed = discord.Embed(
                    title='**{0} is down!**'.format(i['name']),
                    description='Error pinging {0} <@&{1}>'.format(i['address'], config['role_to_mention']),
                    color=discord.Color.red()
                )
                await channel.send(embed=embed)
            else:
                await channel.send('Received response from {0} in: '.format(i['address']) + str(int(ping(i['address'], unit='ms'))) + 'ms')
        await asyncio.sleep(config['secs_between_ping'])


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
        await asyncio.sleep(1)

bot.loop.create_task(monitor_uptime())
bot.run(config['token'])
