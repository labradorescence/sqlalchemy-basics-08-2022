#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Book, Salesperson

def seed():
    engine = create_engine('sqlite:///bookstore.db')
    session = sessionmaker(bind=engine)()

if __name__ == '__main__':
    seed()
