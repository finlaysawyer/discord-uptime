from __future__ import annotations

import ipaddress
from typing import Any

import discord

from utils.config import get_config


class Embed(discord.Embed):
    @staticmethod
    def hide_ips(var: str) -> str:
        words = var.split(" ")

        for index, word in enumerate(words):
            try:
                ipaddress.ip_address(word)
                words[index] = "*hidden*"
            except ValueError:
                pass

        return " ".join(words)

    def add_field(self, *, name: Any, value: Any, inline: bool = True) -> Embed:
        """Override the add_field method in the original embed to hide addresses"""

        if get_config("hide_ips"):
            name = self.hide_ips(name)
            value = self.hide_ips(value)

        field = {"inline": inline, "name": str(name), "value": str(value)}

        try:
            self._fields.append(field)
        except AttributeError:
            self._fields = [field]

        return self
