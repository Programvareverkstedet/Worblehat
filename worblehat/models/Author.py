from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
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
from .xref_tables import Item_Author

if TYPE_CHECKING:
    from .BookcaseItem import BookcaseItem

class Author(Base, UidMixin, UniqueNameMixin):
    items: Mapped[set[BookcaseItem]] = relationship(
        secondary = Item_Author.__table__,
        back_populates = 'authors',
    )

    def __init__(
        self,
        name: str,
    ):
        self.name = name