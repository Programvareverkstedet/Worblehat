# from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
# from sqlalchemy.orm import relationship

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


from .Base import Base
from .mixins import UidMixin, UniqueNameMixin

class Language(Base, UidMixin, UniqueNameMixin):
    iso639_1_code: Mapped[str] = mapped_column(String(2), unique=True, index=True)

    def __init__(
        self,
        name: str,
        iso639_1_code: str,
    ):
        self.name = name
        self.iso639_1_code = iso639_1_code
