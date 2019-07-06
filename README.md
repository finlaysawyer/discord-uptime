# discord-uptime
Discord bot to monitor uptime (soon) and ping addresses

Built using discord.py and ping3 libraries

## Installation
**Install dependencies:** `pip install -r requirements.txt`

**Bot setup:**
Edit the default values in config.json:
* `token` - Bot token
* `notification_channel` - Channel ID where down/up notifications will be sent
* `role_to_mention` - Role ID which will be tagged in down/up notifications
* `secs_between_ping` - How many seconds between pings

**Servers setup:**
To add more servers to ping, simply add a new object and specify the `name` and `address` in servers.json

## Commands
> Default Prefix: >

`status <address>` - Pings an address once

`status_multi <address> <num pings>` - Pings an address each second for the number of pings specified
