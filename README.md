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

## Resources

- [SQLAlchemy ORM Documentation][sqlaorm]
- [SQLAlchemy ORM Session Basics](https://docs.sqlalchemy.org/en/14/orm/session_basics.html)
- [SQLAlchemy ORM Column Elements and Expressions][column]
- [SQLAlchemy ORM Querying Guide](https://docs.sqlalchemy.org/en/14/orm/queryguide.html)

[column]: https://docs.sqlalchemy.org/en/14/core/sqlelement.html
[sqlaorm]: https://docs.sqlalchemy.org/en/14/orm/
