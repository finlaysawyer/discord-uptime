# discord-uptime
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Discord Uptime is a Discord bot that allows you to monitor the uptime of services using ICMP ping, tcp and http requests.
There are also commands available to make manual requests. Built using discord.py, aioping and aiohttp.

## Installation
**Requires Python 3.8+**

Install dependencies:

`pip install -r requirements.txt`

Bot setup (Rename config.example.json and edit the default values):
* `token` - Discord bot token
* `prefix` - Discord bot prefix
* `activity_type` - Activity type for bot status (must be one of `playing, streaming, listening, watching`)
* `activity_name` - Text for bot status
* `disable_help` - If true, the default help command will be disabled
* `hide_ips` - If true, any IP addresses in notifications or the status command will be hidden
* `notification_channel` - Channel ID where down/up notifications will be sent
* `retries` - How many retries to complete before flagging a server with down status
* `role_to_mention` - Role ID which will be tagged in down/up notifications
* `secs_between_ping` - How many seconds between each uptime check
* `timeout` - How many seconds before a ping or HTTP request should timeout

**NOTE: You must enable the [Message Content intent](https://support-dev.discord.com/hc/en-us/articles/4404772028055) in order to run v2.0+**.

## Running the bot

The bot can be run via the `bot.py` entrypoint, e.g. `python -m bot`.

## Docker Image
You can also run the Bot via Docker, simply run:

```bash
docker run --name discord-uptime -d -v $PWD/config.json:/app/config.json:ro -v $PWD/servers.json:/app/servers.json:ro --restart=on-failure ghcr.io/finlaysawyer/discord-uptime:master
```
You can also use a release tag (e.g. `v2.0.0`) instead of `master`.
With this configuration you still need to manually create `config.json` and `servers.json` for the Bot to start, please refer to the appropriate instructions if unsure.

## Servers Configuration
Servers should be setup similar to the examples already in `server.json`:
* There are three supported types: `http`, `tcp` and `ping`
```json
[
    {
      "name": "Google",
      "type": "http",
      "address": "google.com"
    },
    {
      "name": "Gmail SMTP",
      "type": "tcp",
      "address": "smtp.gmail.com:465",
    },
    {
      "name": "Cloudflare",
      "type": "ping",
      "address": "1.1.1.1"
    }
]
```

## Commands
> Default Prefix: >

* `ping <address> [pings]` - Pings an address once, or for the amount specified via pings and returns the delay in ms
* `http <address>` - Performs a HTTP request to the specified address and returns the response code
* `status` - Displays the status of all servers setup in `servers.json`

## Screenshots
> Status Command

![status](https://i.gyazo.com/6d5e0c4fbdb5ff52619d86eef827e369.png)

> Uptime & Downtime Notifications

![uptime](https://i.gyazo.com/803aebfcb3833ac8de7bd38e18378a29.png)

> Hide IP addresses

![hideips](https://i.gyazo.com/8596a75d33aa85716ba86f7e01621bb1.png)

## Contributing

Contributions are welcome. I use flake8 & black for linting and there is a [pre-commit](https://pre-commit.com/) config in the repo to run these tools against local commits.
