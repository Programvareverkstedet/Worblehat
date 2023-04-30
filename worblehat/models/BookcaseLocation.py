from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .Base import Base
from .mixins import (
    UidMixin,
    UniqueNameMixin,
)
if TYPE_CHECKING:
    from .Bookcase import Bookcase
    from .BookcaseItem import BookcaseItem

class BookcaseLocation(Base, UidMixin, UniqueNameMixin):
    description: Mapped[str | None] = mapped_column(Text)

    fk_bookcase_uid: Mapped[int] = mapped_column(Integer, ForeignKey('Bookcase.uid'))

    bookcase: Mapped[Bookcase] = relationship(back_populates='locations')
    items: Mapped[set[BookcaseItem]] = relationship(back_populates='location')

    def __init__(
        self,
        name: str,
        bookcase: Bookcase,
        description: str | None = None,
    ):
        self.name = name
        self.bookcase = bookcase
        self.description = description