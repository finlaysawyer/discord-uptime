import json
from typing import Any, Iterable


def load_config_file(file: str) -> dict:
    """Attempts to load a json config file"""
    with open(file) as config:
        try:
            return json.load(config)
        except json.decoder.JSONDecodeError as err:
            raise KeyError(
                f"Couldn't load {config}: it is formatted incorrectly "
                f"on line {err.lineno} column {err.colno}"
            ) from err


def get_servers() -> Iterable:
    """Reads all specified servers specified in servers.json."""
    return load_config_file("servers.json")


def get_server_name(address: str) -> str:
    """Retrieves a stored server name from an address."""
    file = load_config_file("servers.json")

    for server in file:
        if server["address"] == address:
            return server["name"]

    raise KeyError(f"Could not fetch a server name from {address}")


def get_config(item: str) -> Any:
    """Retrieves the configuration value specified."""
    file = load_config_file("config.json")

    value = file.get(item)

    if value is None:
        raise KeyError(f"Your config is out of date! Missing a value for {item}")
    return value
