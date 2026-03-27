import logging

from .values import JsonObject

log = logging.getLogger(__name__)


async def lookup(id: str) -> JsonObject:
    # raise NotImplementedError()
    log.info('performing lookup')
    return {"test": "data"}
