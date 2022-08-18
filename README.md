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

## Defining Tables via SQLAlchemy ORM

Creating tables with SQLAlchemy ORM requires classes with four key traits:

1. Inheritance from a `declarative_base` object.
2. A `__tablename__` class attribute.
3. One or more `Column`s as class attributes.
4. A `Column` specified to be the table's primary key.

Let's take a look at a class to define a `books` table. Inside of the
`bookstore_app/` directory, create a file called `models.py`.

```py
# bookstore_app/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer(), primary_key=True)
    title = Column(String())
    author = Column(String())
    publisher = Column(String())
    publish_date = Column(DateTime())
```

The `declarative_base` combines a container for table metadata as well as a
group of methods that act as mappers between Python and our SQL database.
Inheritance from `Base`, a `declarative_base` object, allows us to avoid
rewriting code.

The `__tablename__` attribute will eventually be used as the name of our SQL
database table. The table's columns are identified using `Column` objects as
attributes- the optional `primary_key` argument tells SQLAlchemy that
`id` will be the primary key for the `books` table.

This type of class is called a **data model**, or **model**.

***

## Persisting the Schema

We have all of the data we need to generate a database table, but it won't
happen as soon as we save our module. We need to execute a series of Python
statements to do **persist** our schema. You can do this from the Python shell,
but we will be using **Alembic**, a migrations manager, to handle it.

First, navigate to the `bookstore_app/` directory and run
`alembic init migrations`:

```console
$ alembic init migrations
# =>   Creating directory /sqlalchemy-basics-08-2022/bookstore_app/migrations ...  done
# =>   Creating directory /sqlalchemy-basics-08-2022/bookstore_app/migrations/versions ...  done
# =>   Generating /sqlalchemy-basics-08-2022/bookstore_app/migrations/script.py.mako ...  done
# =>   Generating /sqlalchemy-basics-08-2022/bookstore_app/migrations/env.py ...  done
# =>   Generating /sqlalchemy-basics-08-2022/bookstore_app/migrations/README ...  done
# =>   Generating /sqlalchemy-basics-08-2022/bookstore_app/alembic.ini ...  done
# =>   Please edit configuration/connection/logging settings in '/sqlalchemy-basics-08-2022/bookstore_app/alembic.ini' before proceeding.
```

Let's also follow those instructions and update `bookstore_app/alembic.ini`
before proceeding. This file handles the basic configurations for your
database. The only thing we absolutely _need_ to change is `sqlalchemy.url` on
line 58:

```ini
sqlalchemy.url = sqlite:///bookstore.db
```

Additionally, we need to point `bookstore_app/migrations/env.py` to our
models' metadata:

```py
# bookstore_app/migrations/env.py
# line 21
from models import Base
target_metadata = Base.metadata
```

Next, we can generate our first migration and persist the schema in a file
called `bookstore.db`:

```console
$ alembic revision --autogenerate -m 'Create table books'
# => INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
# => INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
# => INFO  [alembic.autogenerate.compare] Detected added table 'books'
# =>  Generating /sqlalchemy-basics-08-2022/bookstore_app/migrations/versions/39cd11f7545b_create_table_books.py ...  done
```

This generates a database for us in `bookstore_app/bookstore.db`, but it doesn't
create our tables. To do that, we need to run `alembic upgrade head`. This will
sync the database with all of our migrations up to the most recent.

```console
$ alembic upgrade head
# => INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
# => INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
# => INFO  [alembic.runtime.migration] Running upgrade  -> 39cd11f7545b, Create table books
```

Now if you open up the database with the SQLite Explorer extension, you should
see two tables:

1. `alembic_version`: the ID of the currently synced migration.
2. `books`: the table we defined in `models.py`!

***

## Breakout Rooms

Let's take three minutes to go into breakout rooms, discuss, and debug. When
we come back, we'll explore CRUD methods in SQLAlchemy.

***

## Resources

- [SQLAlchemy ORM Documentation][sqlaorm]
- [SQLAlchemy ORM Session Basics](https://docs.sqlalchemy.org/en/14/orm/session_basics.html)
- [SQLAlchemy ORM Column Elements and Expressions][column]
- [SQLAlchemy ORM Querying Guide](https://docs.sqlalchemy.org/en/14/orm/queryguide.html)

[column]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html
[sqlaorm]: https://docs.sqlalchemy.org/en/14/orm/
