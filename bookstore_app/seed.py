#!/usr/bin/env python3

from random import randint

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from faker import Faker

from models import Book, Salesperson

def seed():
    engine = create_engine('sqlite:///bookstore_app/bookstore.db')
    session = sessionmaker(bind=engine)()

    session.query(Book).delete()
    session.query(Salesperson).delete()

    session.close()

if __name__ == '__main__':
    seed()
