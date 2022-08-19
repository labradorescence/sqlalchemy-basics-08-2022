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

***

## Resources

- [SQLAlchemy ORM Documentation][sqlaorm]
- [SQLAlchemy ORM Session Basics](https://docs.sqlalchemy.org/en/14/orm/session_basics.html)
- [SQLAlchemy ORM Column Elements and Expressions][column]
- [SQLAlchemy ORM Querying Guide](https://docs.sqlalchemy.org/en/14/orm/queryguide.html)

[column]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html
[sqlaorm]: https://docs.sqlalchemy.org/en/14/orm/
