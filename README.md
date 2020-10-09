# discord-uptime
Discord bot to monitor uptime and ping addresses

Built using discord.py 1.5.x and ping3 libraries

## Installation
**Requires Python 3.6+**

Install dependencies: 

`pip install -r requirements.txt`

Bot setup (Rename config.example.json and edit the default values):
* `token` - Discord bot token
* `notification_channel` - Channel ID where down/up notifications will be sent
* `role_to_mention` - Role ID which will be tagged in down/up notifications
* `secs_between_ping` - How many seconds between each uptime check

No privileged intents are currently needed to run the bot.

Servers setup:

To add more servers to ping, simply add a new object and specify the `name` and `address` in servers.json

## Commands
> Default Prefix: >

* `ping <address> [pings]` - Pings an address once, or for the amount specified via pings
* `status` - Displays the status of all servers

## Screenshots
> Status Command

![status](https://i.gyazo.com/aafabf21cadfa133caa974dad1a489d4.png)
> Uptime & Downtime Notifications

![uptime](https://i.gyazo.com/e81570754dfdb59f6f648946a504877f.png)