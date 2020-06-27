# discord-uptime
Discord bot to monitor uptime and ping addresses

Built using discord.py and ping3 libraries

## Installation
**Requires Python 3.6+, tested with 3.7**

Install dependencies: 

`pip install -r requirements.txt`

Bot setup (Rename config.example.json and edit the default values):
* `token` - Discord bot token
* `notification_channel` - Channel ID where down/up notifications will be sent
* `role_to_mention` - Role ID which will be tagged in down/up notifications
* `secs_between_ping` - How many seconds between each uptime check

Servers setup:

To add more servers to ping, simply add a new object and specify the `name` and `address` in servers.json

## Commands
> Default Prefix: >

* `ping <address> [pings]` - Pings an address once, or for the amount specified via pings
* `status` - Displays the status of all servers

## Screenshots
> Status Command

![status](https://i.gyazo.com/493df5abce9b54aa51f8870cad7260a4.png)
> Uptime & Downtime Notifications

![uptime](https://i.gyazo.com/d69fdebe3a2e0acc82f4be52a12c2b5c.png)