#!/usr/bin/env python3

from random import randint, choice

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Book, Salesperson

def seed():
    engine = create_engine('sqlite:///bookstore_app/bookstore.db')
    session = sessionmaker(bind=engine)()

    session.query(Book).delete()
    session.query(Salesperson).delete()

    print("Seeding books...")

    fake = Faker()

    books = [
        Book(
            title=fake.name(),
            author=fake.name(),
            publisher=fake.name(),
            publish_date=fake.date_time().date(),
            cost=randint(5, 35)
        )
    for i in range(50)]

    session.bulk_save_objects(books)

    print("Seeding salespeople...")

    salespeople = [
        Salesperson(
            name=fake.name(),
            birthday=fake.date_time().date(),
            last_clocked_in=fake.date_time(),
            last_clocked_out=fake.date_time()
        )
    for i in range(20)]

    session.bulk_save_objects(salespeople)

    session.commit()
    session.close()

if __name__ == '__main__':
    seed()
