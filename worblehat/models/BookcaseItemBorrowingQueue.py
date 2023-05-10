from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .Base import Base
from .mixins import UidMixin
if TYPE_CHECKING:
    from .BookcaseItem import BookcaseItem

class BookcaseItemBorrowingQueue(Base, UidMixin):
    username: Mapped[str] = mapped_column(String)
    entered_queue_time = mapped_column(DateTime, default=datetime.now())
    should_notify_user = mapped_column(Boolean, default=False)

    fk_bookcase_item_uid: Mapped[int] = mapped_column(ForeignKey('BookcaseItem.uid'), index=True)

    item: Mapped[BookcaseItem] = relationship(back_populates='borrowing_queue')

    def __init__(
        self,
        username: str,
        item: BookcaseItem,
    ):
        self.username = username
        self.item = item
        self.entered_queue_time = datetime.now()