from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Any

import discord

from utils.config import GREEN, RED, get_config


def hide_ips(var: str) -> str:
    """Replaces IP addresses and ports in a given string"""
    return re.sub(r"[0-9]+(?:\.[0-9]+){3}(:[0-9]+)?", "*hidden*", str(var))


class Embed(discord.Embed):
    def add_field(self, *, name: Any, value: Any, inline: bool = True) -> Embed:
        """Override the add_field method in the original embed to hide addresses"""

        if get_config("hide_ips"):
            name = hide_ips(name)
            value = hide_ips(value)

        field = {"inline": inline, "name": str(name), "value": str(value)}

        try:
            self._fields.append(field)
        except AttributeError:
            self._fields = [field]

        return self


class Status(Enum):
    UP = 1
    DOWN = 2


class CheckType(Enum):
    PING = 1
    HTTP = 2
    TCP = 3


def generate_status_embed(
    status: Status,
    check_type: CheckType,
    request_address: str,
    fields: list[dict] | None = None,
) -> Embed:
    """
    Generates an embed for a request.
    :param status: Indicates whether the request was successful or failed
    :param check_type: The type of request made
    :param request_address: The address the request was mde to
    :param fields: A list of embed fields in the form of dictionaries
    :return: Generated embed
    """
    colour = GREEN if status == Status.UP else RED
    emoji = ":green_circle:" if status == Status.UP else ":red_circle:"
    status_text = "succeeded" if status == Status.UP else "failed"

    embed = Embed(
        title=f"**{emoji} {check_type.name.capitalize()} request to {request_address.lower()} {status_text}**",
        timestamp=datetime.now(),
        colour=colour,
    )

    if fields:
        for field in fields:
            embed.add_field(**field)

    return embed
