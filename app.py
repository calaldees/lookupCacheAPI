import datetime
from pathlib import path
from typing import TYPE_CHECKING

import litestar
import sqlalchemy
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin

from database import Base, JsonObject, LookupItem

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


database_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///lookup.sqlite",
    create_all=True,
    metadata=Base.metadata,
)

README = path("README.md").read_text()


@litestar.get("/")
async def root() -> str:
    return README


async def get(id: str) -> JsonObject:
    raise NotImplementedError()


@litestar.get("/lookup/{id:str}")
async def lookup_item(id, db_session: AsyncSession) -> JsonObject:
    item: LookupItem = await db_session.execute(sqlalchemy.select(LookupItem).where(LookupItem.id == id)).first()
    if item and (item.timestamp > datetime.datetime.now() - datetime.timedelta(minutes=60)):
        return item.payload

    item_payload = await get(id)
    if not item_payload:
        return {}
    async with db_session.begin():
        db_session.add(LookupItem(payload=item_payload))
    return item_payload


app = litestar.Litestar(
    (
        root,
        lookup_item,
    ),
    plugins=(SQLAlchemyPlugin(config=database_config),),
)
