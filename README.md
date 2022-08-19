# SQLAlchemy and Alembic Basics

## Learning Goals

- Create records with seed data.

***

## Key Vocab

- **Persist**: save a schema in a database.
- **Engine**: a Python object that translates SQL to Python and vice-versa.
- **Session**: a Python object that uses an engine to allow us to
  programmatically interact with a database.
- **Transaction**: a strategy for executing database statements such that
  the group succeeds or fails as a unit.
- **Migration**: the process of moving data from one or more databases to one
  or more target databases.

***

## Seed Data

What good is a database without any data? When working with any application
involving a database, it's a good idea to populate your database with some
realistic data when you are working on building new features. SQLAlchemy, and
many other ORMs, refer to the process of adding sample data to the database as
**"seeding"** the database.

We've already seen a scenario by which we can share instructions for
setting up a database with other developers: using SQLAlchemy migrations to
define how the database tables should look. Now, we'll have two kinds of database
instructions we can use:

- Migrations: define how our tables should be set up.
- Seeds: add data to those tables.

***

## Configuring a Seed File

There is much debate about the best location for seed data- if you have a good
plan in place ahead of time, it's wise to make a `seed.py` script inside of your
`migrations/` directory and import it into your first migration. It's a little
late for that for us- we'll keep it in the `bookstore_app` directory instead,
next to the database.

Let's set it up to import the various data models, engine-creators, and
session-makers that it needs to write to our database.

```py
# bookstore_app/seed.py

#!/usr/bin/env python3

from random import randint, choice

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Book, Salesperson

def seed():
    engine = create_engine('sqlite:///bookstore.db')
    session = sessionmaker(bind=engine)()
    
    session.query(Book).delete()
    session.query(Salesperson).delete()

    session.close()

if __name__ == '__main__':
    seed()
```

Now this, of course, does very little. Let's break it down anyway:

- We're importing `create_engine` and `sessionmaker` to build our session.
- The `seed()` function groups our logic into one place. This can be imported
  by other modules if it's ever needed by a migration.
- `seed()` does delete all rows from both tables when the script begins.
  > _We'll miss you, Harold!_
- The if/name/main block runs `seed()` when we call `seed.py` explicitly from
  the command line. Equally importantly, it makes sure the script does not
  execute when `seed()` is imported by other modules.

It's time to get our seed data set up.

***

## Faker

Writing every single record into our database would take forever. It would be
worth it if it were real data, but as real as it looks, it's still just data
that came from asking my wife _"What are some books?"_

Since all fake data is created equal, we are going to use a module called
`Faker`. Faker is used by developers in many languages (including Ruby!) to
generate large amounts of realistic fake data very quickly.

`Faker` is already included in the `Pipfile` for
this application, so we can try it out. Run `python debug.py`, and try
out some Faker methods with our instance `fake`:

```py
fake.name()
# => 'Samantha Taylor'
fake.name()
# => 'Connie Ferguson'
fake.name()
# => 'Christopher Ortega'
```

As you can see, every time we call the `name()` method, we get a new random name.
Faker has a lot of [built-in randomized data generators][faker] that you can use:

```py
fake.email()
# =>'hubbardpatricia@example.com'
fake.color()
# => '#7148af'
fake.profile()
# => {'job': 'Garment/textile technologist', 'company': 'Jones PLC', 'ssn': '768-52-6547', 'residence': '7571 Michael Coves\nNorth Daniel, VA 39350', 'current_location': (Decimal('-30.883927'), Decimal('65.589098')), 'blood_group': 'O-', 'website': ['http://www.grimes.org/', 'http://sanders.net/', 'https://manning-cowan.info/', 'https://www.sims-smith.info/'], 'username': 'julia98', 'name': 'Jillian Morris', 'sex': 'F', 'address': 'USNS Brown\nFPO AA 04021', 'mail': 'james05@yahoo.com', 'birthdate': datetime.date(1990, 6, 20)}
```

Let's use Faker to generate 50 random books (we will use the random library to
generate prices). Modify the `seed()` function as follows:

```py
# bookstore_app/seed.py

from faker import Faker

def seed():
    engine = create_engine('sqlite:///bookstore_app/bookstore.db')
    session = sessionmaker(bind=engine)()

    session.query(Book).delete()
    session.query(Salesperson).delete()

    fake = Faker()

    print("Seeding books...")

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
```

Run `python bookstore_app/seed.py` to seed your database. If you open
`bookstore.db` in VSCode's SQLite Viewer, you should see something similar to
the following in the `books` table:

<p align="center">
    <img src="https://curriculum-content.s3.amazonaws.com/python/sqlalchemy_sqlite_books.png"
         alt="sql table of books with titles that are names" />
</p>

> _That's a lot of biographies!_

And in the `salespeople` table:

<p align="center">
    <img src="https://curriculum-content.s3.amazonaws.com/python/sqlalchemy_sqlite_salespeople.png"
         alt="sql table of books with titles that are names" />
</p>

***

## Adding Seed Data to Migrations

This is actually a very simple process! It is important, though, to first think
about where the seeding script belongs. Is it in a first, blank migration? Is it
when a table is created? Is it afterward?

In general, it makes the most sense to update the `upgrade()`
functions in the migration that creates the table of interest. With that in
mind, we would put the `Book` logic (minus cost!) into `0817994fdbf9` and the
`Salesperson` logic (plus book cost!) into `a7323c275f5a`. Here's what that
might look like:

```py
# migrations/versions/0817994fdbf9_create_table_books.py

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.Column('publisher', sa.String(), nullable=True),
    sa.Column('publish_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###

    engine = create_engine('sqlite:///bookstore.db')
    session = sessionmaker(bind=engine)()

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
    session.commit()
    session.close()
```

And in our second migration:

```py
# migrations/versions/a7323c275f5a_add_table_salespeople.py

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('salespeople',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('birthday', sa.DateTime(), nullable=True),
    sa.Column('last_clocked_in', sa.DateTime(), nullable=True),
    sa.Column('last_clocked_out', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('books', sa.Column('cost', sa.Integer(), nullable=True))
    # ### end Alembic commands ###

    engine = create_engine('sqlite:///bookstore.db')
    session = sessionmaker(bind=engine)()

    print("Seeding book costs...")

    for book in session.query(Book):
        book.cost = randint(5, 35)
    
    print("Seeding salespeople...")

    fake = Faker()

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
```

If you're feeling _very brave_, delete your `bookstore.db` file and run the
migrations one by one:

```console
$ alembic upgrade 0817994fdbf9
# => INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
# => INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
# => INFO  [alembic.runtime.migration] Running upgrade  -> 0817994fdbf9, Create table books
# => Seeding books...
$ alembic upgrade head
# => INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
# => INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
# => INFO  [alembic.runtime.migration] Running upgrade 0817994fdbf9 -> a7323c275f5a, Add table salespeople
# => Seeding book costs...
# => Seeding salespeople...
```

Check your new `bookstore.db` file- you won't see the _same_ data (Faker
generates _random_ data, after all), but you should see perfectly reasonable
entries in place of every record we had before.

<p align="center">
    <img src="https://media2.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif?cid=ecf05e47gl403i7brq4crjt2bpyo1scgk0qvkwj6mbtkn0xm&rid=giphy.gif&ct=g"
         alt="the office voguing celebration" />
</p>

***

## Resources

- [SQLAlchemy ORM Documentation][sqlaorm]
- [SQLAlchemy ORM Session Basics](https://docs.sqlalchemy.org/en/14/orm/session_basics.html)
- [SQLAlchemy ORM Column Elements and Expressions][column]
- [SQLAlchemy ORM Querying Guide](https://docs.sqlalchemy.org/en/14/orm/queryguide.html)

[column]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html
[sqlaorm]: https://docs.sqlalchemy.org/en/14/orm/
