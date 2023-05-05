from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import (
  Integer,
  SmallInteger,
  String,
  ForeignKey,
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
from .xref_tables import (
    Item_Category,
    Item_Author,
)
if TYPE_CHECKING:
    from .Author import Author
    from .BookcaseItemBorrowing import BookcaseItemBorrowing
    from .BookcaseItemBorrowingQueue import BookcaseItemBorrowingQueue
    from .BookcaseShelf import BookcaseShelf
    from .Category import Category
    from .Language import Language
    from .MediaType import MediaType

class BookcaseItem(Base, UidMixin, UniqueNameMixin):
    isbn: Mapped[int] = mapped_column(String, unique=True, index=True)
    owner: Mapped[str] = mapped_column(String, default='PVV')
    amount: Mapped[int] = mapped_column(SmallInteger, default=1)

    fk_media_type_uid: Mapped[int] = mapped_column(Integer, ForeignKey('MediaType.uid'))
    fk_bookcase_shelf_uid: Mapped[int | None] = mapped_column(Integer, ForeignKey('BookcaseShelf.uid'))
    fk_language_uid: Mapped[int] = mapped_column(Integer, ForeignKey('Language.uid'))

    media_type: Mapped[MediaType] = relationship(back_populates='items')
    shelf: Mapped[BookcaseShelf] = relationship(back_populates='items')
    language: Mapped[Language] = relationship()
    borrowings: Mapped[BookcaseItemBorrowing] = relationship(back_populates='item')
    borrowing_queue: Mapped[BookcaseItemBorrowingQueue] = relationship(back_populates='item')

    categories: Mapped[set[Category]] = relationship(
        secondary = Item_Category.__table__,
        back_populates = 'items',
    )
    authors: Mapped[set[Author]] = relationship(
        secondary = Item_Author.__table__,
        back_populates = 'items',
    )

    def __init__(
        self,
        name: str,
        isbn: int | None = None,
        owner: str = 'PVV',
    ):
        self.name = name
        self.isbn = isbn
        self.owner = owner