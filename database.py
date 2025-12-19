# https://docs.litestar.dev/2/usage/databases/sqlalchemy/plugins/sqlalchemy_plugin.html#example

from typing import TYPE_CHECKING
import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import JSON, TIMESTAMP

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class Base(DeclarativeBase): ...

class LookupItem(Base):
    __tablename__ = "lookup_item"
    id: Mapped[str] = mapped_column(primary_key=True)
    payload: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
