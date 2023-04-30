from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Text
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
    from .BookcaseLocation import BookcaseLocation

class Bookcase(Base, UidMixin, UniqueNameMixin):
    description: Mapped[str | None] = mapped_column(Text)

    locations: Mapped[list[BookcaseLocation]] = relationship(back_populates='bookcase')

    def __init__(
        self,
        name: str,
        description: str | None = None,
    ):
        self.name = name
        self.description = description

