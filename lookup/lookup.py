import textwrap
import logging

import aiohttp

from .values import JsonObject

log = logging.getLogger(__name__)


async def lookup(session: aiohttp.ClientSession, id: str) -> JsonObject:
    log.info(f'lookup: {id}')
    async with session.post(
        "https://athena.diginf.musicradio.com/graphql",
        json=dict(
            query=textwrap.dedent("""
                query track($playoutId: String!) {
                    track(playoutId: $playoutId) {
                        id
                        title
                        artist
                        artwork {
                            url(width:225)
                        }
                    }
                }
            """),
            variables=dict(playoutId=id),
        ),
    ) as response:
        return (await response.json())["data"]["track"]
    return {}
