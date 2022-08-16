from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from worblehat.database import Base

category_association = Table('category_association', Base.metadata,
    Column('category_id', Integer, ForeignKey('categories.id')),
    Column('item_id', Integer, ForeignKey('items.id'))
)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))

    items = relationship('Item', secondary=category_association, back_populates='categories')
    def __repr__(self):
        return '<Category %r>' % self.name
