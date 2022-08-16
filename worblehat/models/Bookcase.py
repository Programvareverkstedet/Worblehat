from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from worblehat.database import Base


class Bookcase(Base):
    __tablename__ = 'bookcases'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    description = Column(String(255))

    locations = relationship('Location', back_populates='bookcase')

    def __repr__(self):
        return '<Bookcase %r>' % self.name

