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

class Item_Category(Base, XrefMixin):
    fk_item_uid: Mapped[int] = mapped_column(ForeignKey('BookcaseItem.uid'), primary_key=True)
    fk_category_uid: Mapped[int] = mapped_column(ForeignKey('Category.uid'), primary_key=True)