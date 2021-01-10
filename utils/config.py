import json
from typing import Iterable, Union


def get_servers() -> Iterable:
    """Reads all specified servers specified in servers.json."""
    with open("servers.json") as f:
        return json.load(f)


def get_config(item: str) -> Union[str, int]:
    """Retrieves the configuration value specified."""
    with open("config.json") as f:
        return json.load(f)[item]
