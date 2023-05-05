from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    ForeignKey,
    SmallInteger,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .Base import Base
from .mixins import UidMixin
if TYPE_CHECKING:
    from .Bookcase import Bookcase
    from .BookcaseItem import BookcaseItem

# NOTE: Booshelfs are 0 indexed for both rows and columns,
#       where cell 0-0 is placed in the lower right corner.

class BookcaseShelf(Base, UidMixin):
    __table_args__ = (
        UniqueConstraint(
            'column',
            'fk_bookcase_uid',
            'row',
        ),
    )
    description: Mapped[str | None] = mapped_column(Text)
    row: Mapped[int] = mapped_column(SmallInteger)
    column: Mapped[int] = mapped_column(SmallInteger)

    fk_bookcase_uid: Mapped[int] = mapped_column(Integer, ForeignKey('Bookcase.uid'))

    bookcase: Mapped[Bookcase] = relationship(back_populates='shelfs')
    items: Mapped[set[BookcaseItem]] = relationship(back_populates='shelf')

    def __init__(
        self,
        row: int,
        column: int,
        bookcase: Bookcase,
        description: str | None = None,
    ):
        self.row = row
        self.column = column
        self.bookcase = bookcase
        self.description = description