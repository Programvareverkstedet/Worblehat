from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from worblehat.database import Base

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)

    title = Column(String(255), nullable=False)
    owner = Column(String(255))
    isbn = Column(String(255))

    media_id = Column(Integer, ForeignKey('media_types.id'), nullable=False)
    media = relationship('MediaType', back_populates='items')

    def __repr__(self):
        return '<Item %r / %r>' % (self.media.name, self.title)

