from sqlalchemy import (
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from ..Base import Base
from ..mixins.XrefMixin import XrefMixin

class Item_Author(Base, XrefMixin):
    fk_item_uid: Mapped[int] = mapped_column(ForeignKey('BookcaseItem.uid'), primary_key=True)
    fk_author_uid: Mapped[int] = mapped_column(ForeignKey('Author.uid'), primary_key=True)