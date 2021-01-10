# Changelog

## [1.0.0] - 2021-01-10

### Added
- **Added support for tracking website uptime in montoring.**
- **Added http command for manual checking of website uptime.**
- Added more type hints and data types for function parameters
- Linting workflow for PRs and master releases
- More annotations for commands
- Added logging

### Changed
- **No longer need to reload the bot to update the config files.**
- Status command moved into the monitor cog.
- Status command and up/down notifications now show monitor type.
- Discord.py upgraded to 1.6 and aiohttp bumped to 3.7.3
- Main file renamed to `bot.py`

[1.0.0]: https://github.com/finlaysawyer/discord-uptime/compare/v0.0.1...v1.0.0