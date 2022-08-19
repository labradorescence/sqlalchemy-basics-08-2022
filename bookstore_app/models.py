from sqlalchemy import create_engine # new import
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker # new import
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    author = Column(String())
    publisher = Column(String())
    publish_date = Column(DateTime())
    cost = Column(Integer())

    def __repr__(self):
        return f'Book({self.title} by {self.author})'

class Salesperson(Base):
    __tablename__ = 'salespeople'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    birthday = Column(DateTime())
    last_clocked_in = Column(DateTime())
    last_clocked_out = Column(DateTime())

    def __repr__(self):
        return f'Salesperson({self.name})'
