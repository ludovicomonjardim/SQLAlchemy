from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from models.base import Base
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:admin@localhost:5432/cinema")

# Creating the engine
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)

# Session configuration
Session = sessionmaker(bind=engine)

# Function to initialize the database
def initialize_database():
    """Creates all tables in the database based on the models."""
    Base.metadata.create_all(engine)
    print("Tables successfully created!")

@contextmanager
def get_connection():
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()
