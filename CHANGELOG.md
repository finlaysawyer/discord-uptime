# Changelog

## [1.5.0] - 2023-03-12

`v1.5.0` will be the last release in the v1 cycle. v2 is in development and will contain several improvements
over v1, such as the addition of slash commands, supporting the 'ping' check without root via icmplib, and more. Future
improvements such as persistent tracking of uptime/downtime in SQLite is also planned, but will likely come
after the initial v2 release.

### Added
- `pre-commit-ci` has been configured to autofix PRs that do not pass formatting checks
- **[BREAKING]** Python 3.7 has been dropped, as upstream Discord.py no longer supports it
- The message content intent has been added, which is a requirement from Discord to run the bot (thanks @dotneko)
- A Dockerfile has been added as an alternative way to run the bot (thanks @alsoGAMER)
- A workflow has been added that automatically pushes new image releases to [GHCR](https://github.com/finlaysawyer/discord-uptime/pkgs/container/discord-uptime)

### Changed
- Discord.py has been bumped to the latest 2.x version (thanks @dotneko)
- Modifications for newer async/await syntax (thanks @dotneko)
- Various typing, logging and spelling tweaks
- `aioping` is now used instead of `ping3` for the ping check

### Fixed
- IP addresses are now censored correctly when a port is added at the end

## [1.4.0] - 2021-09-25

### Added
- **[BREAKING]** Support for retrying status checks before sending an alert (thanks @tferreira!)

### Changed
- If multiple servers are down, the notification role will now only be mentioned once (thanks @ColdUnwanted!)
- `KeyError` will now be raised for config related errors

## [1.3.0] - 2021-06-24

### Added
- Support for tcp monitoring (thanks @tferreira!)
- Added a pre-commit config and flake8

### Changed
- Added support for building the bot against multiple Python versions in CI
- Minor documentation & typing tweaks

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
[1.3.0]: https://github.com/finlaysawyer/discord-uptime/compare/v1.2.1...v1.3.0
[1.4.0]: https://github.com/finlaysawyer/discord-uptime/compare/v1.3.0...v1.4.0
[1.5.0]: https://github.com/finlaysawyer/discord-uptime/compare/v1.4.0...v1.5.0
