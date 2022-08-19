# SQLAlchemy and Alembic Basics

## Learning Goals

- Create and persist a schema.
- Create and save your first data model.
- Manage changes to models with Alembic.
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

## Introduction

This session is designed to be a **code-along**. There is a GitHub repo to clone
down with branches to match different checkpoints along the way. If you run into
errors before we move from one section to the next, please checkout the next
checkpoint, but share those issues with me or another member of the curriculum
team and we can address them after the session ends.

Clone that repo down now and run `pipenv install && pipenv shell` to start up
your virtual environment.

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

## What is Alembic?

Alembic is a library for handling schema changes that uses SQLAlchemy to
perform the migrations in a standardized way. Since SQLAlchemy only creates
missing tables when we use the `Base.metadata.create_all()` method, it doesn’t
update the tables to match any changes we made to the columns or keys. Alembic
provides us with classes and methods that will manage schema changes over the
course of development. Because Alembic builds upon the functionality of
SQLAlchemy, it can be used with a wide range of databases and web frameworks.

***

## Creating a Migration Environment

Earlier, we ran `alembic init migrations` command to create a
migration environment in the `migrations/` directory. This process created our
migration environment as well as an `alembic.ini` file with configuration
options for the environment. If you run `tree` in `bookstore_app/` now, you should
see this structure:

```console
.
├── alembic.ini
├── bookstore.db
├── migrations
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── 0817994fdbf9_create_table_books.py
└── models.py
```

The `versions/` directory holds our migration scripts. `env.py` defines and
instantiates a SQLAlchemy engine, connects to that engine, starts a transaction,
and calls the migration engine. `script.py.mako` is a template that is used when
creating a migration- it defines the basic structure of a migration. We won't
need to touch that file.

***

## Generating Migrations

After we ran `alembic revision --autogenerate -m "Create table books"` earlier,
a file popped up in the `migrations/versions/` directory. Here's what you should
see inside:

```py
"""Create table books

Revision ID: 0817994fdbf9
Revises: 
Create Date: 2022-08-18 16:04:51.060065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0817994fdbf9'
down_revision = None
branch_labels = None
depends_on = None


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


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books')
    # ### end Alembic commands ###
```

This file starts off with the message that we included with our `alembic`
command. It is important to treat these messages as you would commit messages
in Git so that other developers know when certain tables, columns, keys, and
so on were added to the database.

The `upgrade()` method includes the code that would be needed to perform
changes to the database based on this migration. Similarly, the `downgrade()`
method includes any code that would be needed to undo this migration and return
to the previous state.

After generating our migration earlier, we ran:

```console
$ alembic upgrade head
# => INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
# => INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
# => INFO  [alembic.runtime.migration] Running upgrade  -> 0817994fdbf9, Create table books
```

This upgraded the database to the `head`, or most recent revision.

When we make changes to data models, we can usually use Alembic
to automatically generate migrations for us and upgrade the database
accordingly.

***

## Generating a New Migration

We have a new model set up in `models.py`: `Salesperson`. (This is a book
_store_, after all.) Let's use Alembic to autogenerate a new migration:

```console
$ alembic revision --autogenerate -m 'Add table salespeople'
```

You should now see a new table for salespeople in `bookstore.db`. We also
added a `cost` column for `books`. You can do a lot in one migration!

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
