from sqlalchemy.orm import sessionmaker
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Table definition
class Beauty(Base):
    __tablename__ = 'beauty'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
       }

# Item defintions
class BeautyItem(Base):
    __tablename__ = 'beauty_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    beauty_id = Column(Integer, ForeignKey('beauty.id'))
    product = relationship(Beauty)
    price = Column(String(8))
    description = Column(String(250))
    feature = Column(String(250))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
           'price'         : self.price,
           'feature'         : self.feature,
       }


engine = create_engine('sqlite:///beautyitems.db')
Base.metadata.create_all(engine)
