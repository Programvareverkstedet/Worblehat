from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from worblehat.database import Base
from .Language import Language

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)

    title = Column(String(255), nullable=False)
    owner = Column(String(255))
    isbn = Column(String(255))

    media_id = Column(Integer, ForeignKey('media_types.id'), nullable=False)
    media = relationship('MediaType', back_populates='items')

    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    location = relationship('Location', back_populates='items')

    language_id = Column(Integer, ForeignKey('languages.id'), nullable=False)
    language = relationship('Language', back_populates='items')
    
    categories = relationship('Category', secondary='category_association', back_populates='items')

    def __repr__(self):
        return '<Item %r / %r>' % (self.media.name, self.title)

