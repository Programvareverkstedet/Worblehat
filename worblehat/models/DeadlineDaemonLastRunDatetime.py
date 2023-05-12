from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .Base import Base

class DeadlineDaemonLastRunDatetime(Base):
    __table_args__ = (
        CheckConstraint(
            'uid = true',
            name = 'single_row_only',
        ),
    )
    uid: Mapped[bool] = mapped_column(Boolean, primary_key=True, default=True)
    time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())