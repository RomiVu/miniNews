import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


DATABASE_URL = os.getenv('DATABASE_URL', None)

if DATABASE_URL is None:
    raise Exception(f'DATABASE_URL not found in os.getenv')

# for sqlite3
# check_same_thread = False if DATABASE_URL.startswith('sqlite') else True
# Engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": check_same_thread}
# )

Engine = create_engine(
    DATABASE_URL
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
