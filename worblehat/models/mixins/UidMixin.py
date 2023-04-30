from typing_extensions import Self

from sqlalchemy import Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from worblehat.database import db

class UidMixin(object):
    uid: Mapped[int] = mapped_column(Integer, primary_key=True)

    @classmethod
    def get_by_uid(cls, uid: int) -> Self | None:
        """
        NOTE:
        This is a flask_sqlalchemy specific method.
        It will not work outside of a request context.
        """
        return db.session.query(cls).where(cls.uid == uid).one_or_none()

    @classmethod
    def get_by_uid_or_404(cls, uid: int) -> Self:
        """
        NOTE:
        This is a flask_sqlalchemy specific method.
        It will not work outside of a request context.
        """
        return db.session.query(cls).where(cls.uid == uid).one_or_404()