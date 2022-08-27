from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from worblehat.database import Base

class Language(Base):
    __tablename__ = 'languages'
    id = Column(Integer, primary_key=True)

    name = Column(String(32), nullable=False)
    shortname = Column(String(2), nullable=False)
    flag = Column(String(3))

    items = relationship('Item', back_populates='language')

    def __repr__(self):
        return '<Language %r>' % self.name
