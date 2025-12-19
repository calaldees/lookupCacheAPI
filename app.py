from collections.abc import Sequence
#from typing import TYPE_CHECKING

import litestar
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from sqlalchemy import select

from database import Base, LookupItem

#if TYPE_CHECKING:
from sqlalchemy.ext.asyncio import AsyncSession


database_config = SQLAlchemyAsyncConfig(
    connection_string="sqlite+aiosqlite:///lookup.sqlite",
    create_all=True,
    metadata=Base.metadata,
)


@litestar.get("/")
async def index() -> str:
    return "Hello, world!"


@litestar.get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    return {"book_id": book_id}


@litestar.post("/add")
async def add_item(data: LookupItem, db_session: AsyncSession) -> Sequence[LookupItem]:
    async with db_session.begin():
        db_session.add(data)
    return (await db_session.execute(select(LookupItem))).scalars().all()


app = litestar.Litestar(
    (
        index,
        get_book,
        add_item,
    ),
    plugins=(SQLAlchemyPlugin(config=database_config),),
)
