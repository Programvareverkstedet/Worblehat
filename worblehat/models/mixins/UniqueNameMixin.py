from typing_extensions import Self

from sqlalchemy import Text
from sqlalchemy.orm import (
    Mapped,
    Session,
    mapped_column,
)

from worblehat.flaskapp.database import db

class UniqueNameMixin(object):
    name: Mapped[str] = mapped_column(Text, unique=True, index=True)

    @classmethod
    def get_by_name(cls, name: str, sql_session: Session = db.session) -> Self | None:
        """
        NOTE:
        This method defaults to using the flask_sqlalchemy session.
        It will not work outside of a request context, unless another session is provided.
        """
        return sql_session.query(cls).where(cls.name == name).one_or_none()

    @classmethod
    def get_by_uid_or_404(cls, name: str, sql_session: Session = db.session) -> Self:
        """
        NOTE:
        This method defaults to using the flask_sqlalchemy session.
        It will not work outside of a request context, unless another session is provided.
        """
        return sql_session.query(cls).where(cls.name == name).one_or_404()