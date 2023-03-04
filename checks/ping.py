from icmplib import Host, async_ping

from utils.config import get_config

TIMEOUT = get_config("timeout")


async def ping(address: str) -> Host:
    request: Host = await async_ping(address, timeout=TIMEOUT, privileged=False)
    return request
