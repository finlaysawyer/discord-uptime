# Changelog

## [1.2.1] - 2021-03-22

### Changed
- User commands like `ping` will now escape mentions, preventing the bot from using tagging roles.

## [1.2.0] - 2021-03-20

### Added
- Option to hide IP addresses in commands and notifications (`hide_ips`) (#23).

### Changed
- `http_timeout` has been renamed to `timeout` and now also applies to ping requests.
- Up and down notifications will now use the server name in the Embed title instead of the address.

### Fixed
- `activity_name` now reads from the config correctly.
- `disable_help` now reads a boolean instead of a string.

## [1.1.0] - 2021-02-19

### Added
- Bandit for security linting
- User-friendly errors when a config is formatted incorrectly or missing values
- Configurable bot status in `config.json`:
  - `activity_type` - one of `playing, streaming, listening, watching`
  - `activity_name` - any string
- Default help command can now be disabled by setting `disable_help` to 'true'

### Changed
- Replaced flake8 with pylint and did some minor refactoring

## [1.0.1] - 2021-01-10

### Changed
- Updated the default config to reflect new `http_timeout` option

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
[1.0.1]: https://github.com/finlaysawyer/discord-uptime/compare/v1.0.0...v1.0.1
[1.1.0]: https://github.com/finlaysawyer/discord-uptime/compare/v1.0.1...v1.1.0
[1.2.0]: https://github.com/finlaysawyer/discord-uptime/compare/v1.1.1...v1.2.0
[1.2.1]: https://github.com/finlaysawyer/discord-uptime/compare/v1.2.0...v1.2.1