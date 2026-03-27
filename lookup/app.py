import datetime
import os
from pathlib import Path
import logging

import litestar
import sqlalchemy
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin

from .database import Base, LookupItem
from .lookup import lookup
from .values import JsonObject

from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)

CACHE_TIMEOUT = datetime.timedelta(
    minutes=int(os.environ.get("CACHE_TIMEOUT_MINUTES", "1"))
)

database_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///lookup.sqlite",
    create_all=True,
    metadata=Base.metadata,
)

README = Path("README.md").read_text()


@litestar.get("/")
async def root() -> str:
    return README


@litestar.get("/lookup/{id:str}")
async def lookup_item(id: str, db_session: AsyncSession) -> JsonObject:
    now = datetime.datetime.now()
    item: LookupItem = (await db_session.scalars(sqlalchemy.select(LookupItem).where(LookupItem.id == id))).first()
    if item and (item.timestamp > now - CACHE_TIMEOUT):
        #log.info(f'cached {id} - remaining {CACHE_TIMEOUT + (item.timestamp - now)}')
        return item.payload

    item_payload = await lookup(id)
    if not item_payload:
        return {}

    if item:
        #log.info(f'update {id}')
        item.payload = item_payload
        item.timestamp = now
    else:
        #log.info(f'new {id}')
        db_session.add(LookupItem(id=id, payload=item_payload, timestamp=now))
    await db_session.commit()
    return item_payload


def create_app() -> litestar.LiteStar:
    return litestar.Litestar(
        (
            root,
            lookup_item,
        ),
        plugins=(SQLAlchemyPlugin(config=database_config),),
    )
