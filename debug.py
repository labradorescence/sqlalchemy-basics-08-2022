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
