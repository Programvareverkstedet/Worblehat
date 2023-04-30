from typing_extensions import Self

from sqlalchemy import Text
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from worblehat.database import db

class UniqueNameMixin(object):
    name: Mapped[str] = mapped_column(Text, unique=True, index=True)

    @classmethod
    def get_by_name(cls, name: str) -> Self | None:
        """
        NOTE:
        This is a flask_sqlalchemy specific method.
        It will not work outside of a request context.
        """
        return db.session.query(cls).where(cls.name == name).one_or_none()

    @classmethod
    def get_by_uid_or_404(cls, name: str) -> Self:
        """
        NOTE:
        This is a flask_sqlalchemy specific method.
        It will not work outside of a request context.
        """
        return db.session.query(cls).where(cls.name == name).one_or_404()