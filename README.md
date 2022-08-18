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

## The Session

SQLAlchemy interacts with the database through **sessions**. These wrap
**engine** objects, which we create using a database address and SQLAlchemy's
`create_engine` method. The session contains an **identity map**, which is
similar to an empty dictionary with keys for the table name, columns, and
primary keys. When the session pulls data from `bookstore.db`, it fills the
identity map and uses it to populate a `Book` object with specific attribute
values. When it commits data to the database, it fills the identity map in the
same fashion but unpacks it into a `books` row instead.

### `sessionmaker`

To create a session, we need to use SQLAlchemy's `sessionmaker` class. This
ensures that there is a consistent identity map for the duration of our session.

Let's create a session in `debug.py` so that we can start executing
statements in `bookstore.db`:

```py
#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bookstore_app.models import Book

if __name__ == '__main__':
    
    # Connect to the database
    engine = create_engine('sqlite:///bookstore_app/bookstore.db')

    # Create a session
    session = sessionmaker(bind=engine)()

    import ipdb; ipdb.set_trace()
```

Run `python models.py` to create a session and enter `ipdb`.

***

## Creating Records

To create a new book record in our database, we need to create an object
using the `Book` class. This syntax is the same as with instantiating any
other Python class.

> **Note**: while we can enter the data in order without argument names, we
> are going to use them consistently in class constructors when using
> SQLAlchemy. This is because it makes our code much more readable when working
> with tables with many columns.

```console
ipdb> leonardo_da_vinci = Book(
    title="Leonardo da Vinci",
    author="Walter Isaacson",
    publisher="Simon and Schuester",
    publish_date=datetime(year=2017, month=10, day=17)
)
ipdb> session.add(leonardo_da_vinci)
ipdb> session.commit()
```

After we create our `Book` instance, we need to add it to the session and
commit the transaction. If we want to save multiple books, we can do so with
`session.bulk_save_objects(list)`:

```console
ipdb> a_game_of_thrones = Book(
    title="A Game of Thrones",
    author="George R. R. Martin",
    publisher="Bantam Spectra",
    publish_date=datetime(1996, 8, 1)
)
ipdb> harold_and_the_purple_crayon = Book(
    title="Harold and the Purple Crayon",
    author="Crockett Johnson",
    publisher="Harper Collins",
    publish_date=datetime(1955, 1, 1)
)
ipdb> session.bulk_save_objects([a_game_of_thrones, harold_and_the_purple_crayon])
ipdb> session.commit()
```

***

## Reading Records

SQLAlchemy provides us many options for queries. You've probably noticed already
if you've gone through the new SQLAlchemy module!

SQLAlchemy uses queries that return `query` objects. Each of these objects
possesses the same methods; this means that queries can be chained to great
lengths. The only methods that do not allow chaining are those that return
single records, like `first()`.

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
