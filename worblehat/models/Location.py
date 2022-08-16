from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from worblehat.database import Base


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    bookcase_id = Column(Integer, ForeignKey('bookcases.id'), nullable=False)
    bookcase = relationship('Bookcase', back_populates='locations')

    items = relationship('Item', back_populates='location')

    def __repr__(self):
        return '<Location %s %s>' % (self.bookcase.name, self.name)

