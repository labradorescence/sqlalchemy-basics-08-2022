# SQLAlchemy and Alembic Basics

## Learning Goals

- Create and persist a schema.
- Create and save your first data model.

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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Book, Salesperson

def seed():
    engine = create_engine('sqlite:///bookstore.db')
    session = sessionmaker(bind=engine)()

if __name__ == '__main__':
    seed()
```

Now this, of course, does nothing. Let's break it down anyway:

- We're importing `create_engine` and `sessionmaker` to build our session.
- The `seed()` function groups our logic into one place. This can be imported
  by other modules if it's ever needed by a migration.
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
out some Faker methods:

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
generate prices). Replace the data after our data deletion in the `seed.py`
file with the following code:

***

## Resources

- [SQLAlchemy ORM Documentation][sqlaorm]
- [SQLAlchemy ORM Session Basics](https://docs.sqlalchemy.org/en/14/orm/session_basics.html)
- [SQLAlchemy ORM Column Elements and Expressions][column]
- [SQLAlchemy ORM Querying Guide](https://docs.sqlalchemy.org/en/14/orm/queryguide.html)

[column]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html
[sqlaorm]: https://docs.sqlalchemy.org/en/14/orm/
