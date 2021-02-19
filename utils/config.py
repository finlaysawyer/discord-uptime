import json
from typing import Iterable, Union


def get_servers() -> Iterable:
    """Reads all specified servers specified in servers.json."""
    with open("servers.json") as file:
        try:
            return json.load(file)
        except json.decoder.JSONDecodeError as err:
            raise Exception(
                f"Couldn't load servers.json: it is formatted incorrectly "
                f"on line {err.lineno} column {err.colno}"
            ) from err


def get_config(item: str) -> Union[str, int]:
    """Retrieves the configuration value specified."""
    with open("config.json") as file:
        try:
            file = json.load(file)
        except json.decoder.JSONDecodeError as err:
            raise Exception(
                f"Couldn't load config.json: it is formatted incorrectly "
                f"on line {err.lineno} column {err.colno}"
            ) from err

        value = file.get(item)

        if value is None:
            raise Exception(f"Your config is out of date! Missing a value for {item}")
        return value
