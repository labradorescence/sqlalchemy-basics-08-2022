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

`query` objects, in addition to supporting chaining, are iterable objects. This
means that you can loop through them or extract their data with a list
interpretation.

Let's add a `__repr__` to `Book` before moving on so we can inspect the returned
objects a bit easier:

```py
# bookstore_app/models.py

# imports, table metadata

    def __repr__(self):
        return f'Book({self.title} by {self.author})'
```

### Getting Everything

Let's start by getting all of the data from a table:

```console
ipdb> books = session.query(Book)
ipdb> print([book for book in books])

# => [
        Book(Leonardo da Vinci by Walter Isaacson),
        Book(A Game of Thrones by George R. R. Martin),
        Book(Harold and the Purple Crayon by Crockett Johnson)
    ]
```

> Aren't you glad we added that `__repr__`?

We would see the same output using the `all()` instance method:

```console
ipdb> students = session.query(Student).all()
ipdb> print(students)

# => [
        Book(Leonardo da Vinci by Walter Isaacson),
        Book(A Game of Thrones by George R. R. Martin),
        Book(Harold and the Purple Crayon by Crockett Johnson)
    ]
```

The former strategy is considered best practice, as it accesses the returned
objects one at a time and is thus more memory-efficient.

### Selecting Only Certain Columns

By default, the `query()` method returns complete records from the data model
passed in as an argument. If we're only looking for certain fields, we can
specify this in the arguments we pass to `query()`. Here's how we would retrieve
all of the students' names:

```console
ipdb> book_titles = [title for title in session.query(Book.title)]
ipdb> print(book_titles)

# => [('Leonardo da Vinci',), ('A Game of Thrones',), ('Harold and the Purple Crayon',)]
```

### Ordering

By default, results from any database query are ordered by their primary key.
The `order_by()` method allows us to sort by any column:

```console
ipdb> books_by_title = [title for title in session.query(Book.title).order_by(Book.title)]
ipdb> print(books_by_title)

# => [('A Game of Thrones',), ('Harold and the Purple Crayon',), ('Leonardo da Vinci',)]
```

### Limiting

To limit your result set to the first `x` records, you can use the `limit()`
method:

```console
ipdb> oldest_book = session.query(Book.title).order_by(Book.publish_date).limit(1)[0]
ipdb> print(oldest_book)
# => ('Harold and the Purple Crayon',)
```

The `first()` method is a quick and easy way to execute a `limit(1)` statement
and does not require indexing or list interpretation:

```console
ipdb> oldest_book = session.query(Book.title).order_by(Book.publish_date).first()
ipdb> print(oldest_book)
# => ('Harold and the Purple Crayon',)
```

### Filtering

Retrieving specific records requires use of the `filter()` method. A typical
`filter()` statement has a column, a standard operator, and a value. It is
possible to chain multiple `filter()` statements together, though it is
typically easier to read with comma-separated clauses inside of one `filter()`
statement.

```console
ipdb> last_30_years = [book for book in session.query(Book).filter(Book.publish_date >= datetime(1992, 8, 19))]
ipdb> print(last_30_years)
# => [Book(Leonardo da Vinci by Walter Isaacson), Book(A Game of Thrones by George R. R. Martin)]
```

<p align="center">
<img src="https://media2.giphy.com/media/26FxsQwgJyU4me9ig/giphy.gif?cid=ecf05e47fpygu4wqi59tizlq2wgpxhp4ay3t0jbhdn7hdan6&rid=giphy.gif&ct=g"
     alt="tituss burgess phew" />
</p>

***

## Updating Records

There are two main strategies for updating records with SQLAlchemy:

1. Modify an object, then add it to the session and commit.
2. Use the `update()` method to modify all records in a queryset.

The former strategy works exactly how it sounds. Let's modify the record for
"Harold and the Purple Crayon," as "Crockett Johnson" was just a pen name for
the cartoonist David Johnson Leisk.

```console
ipdb> harold = session.query(Book).filter(Book.title == "Harold and the Purple Crayon").first()
ipdb> harold.author = "David Johnson Leisk"
ipdb> session.add(harold)
ipdb> session.commit()
```

Now when we search for the same book, we see:

```console
ipdb> session.query(Book).filter(Book.title == "Harold and the Purple Crayon").first().author
# => 'David Johnson Leisk'
```

The `update()` syntax is a bit odd for Python: it takes a dictionary with a
column object as a key and an action as a value. Let's respect the author's
wishes and change his record back to reflect his pen name:

```console
ipdb> session.query(Book).filter(Book.title == "Harold and the Purple Crayon").update({Book.author: "Crockett Johnson"})
# => 1
ipdb> session.query(Book).filter(Book.title == "Harold and the Purple Crayon").first().author
# => 'Crockett Johnson'

```

***

## Deleting Records

Deletion is handled similarly to updating (though the syntax is a bit easier).
There are two main strategies:

1. Delete a record using an instance and the session object.
2. Delete all records matching a queryset using the `query.delete()` method.

I won't be executing any deletions here (we only have three records!) but here
are the two options, respectively:

```console
# deleting harold and the purple crayon
ipdb> harold = session.query(Book).filter(Book.title == "Harold and the Purple Crayon").first()
ipdb> session.delete(harold)
ipdb> session.commit()
```

```console
# deleting everything in the books table
ipdb> session.query(Book).delete()
```

***

## Breakout Rooms

Let's take three minutes to go into breakout rooms, discuss, and debug. When
we come back, we'll dive deeper into migrations with Alembic.

***

## Resources

- [SQLAlchemy ORM Documentation][sqlaorm]
- [SQLAlchemy ORM Session Basics](https://docs.sqlalchemy.org/en/14/orm/session_basics.html)
- [SQLAlchemy ORM Column Elements and Expressions][column]
- [SQLAlchemy ORM Querying Guide](https://docs.sqlalchemy.org/en/14/orm/queryguide.html)

[column]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html
[sqlaorm]: https://docs.sqlalchemy.org/en/14/orm/
