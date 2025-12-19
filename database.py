# https://docs.litestar.dev/2/usage/databases/sqlalchemy/plugins/sqlalchemy_plugin.html#example

from typing import TYPE_CHECKING

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class Base(DeclarativeBase): ...

class LookupItem(Base):
    __tablename__ = "lookup_item"
    id: Mapped[str] = mapped_column(primary_key=True)
    payload: Mapped[bool]
