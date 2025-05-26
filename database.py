import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

 # Load environment variables from .env file (if it exists)
load_dotenv()


# --- Database URL Configuration ---
 # Get database URL from environment variable. Default to SQLite file in current directory.
 # For SQLite, 'sqlite:///./sql_app.db' means a file named sql_app.db in the project root.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

  # --- SQLAlchemy Engine ---
   
 # The engine is responsible for communicating with the database.
# 'connect_args' is specific to SQLite: 'check_same_thread': False
# is crucial because SQLite works with a single thread per connection,
# and FastAPI's default async nature (multiple threads) would cause issues otherwise.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )


  # --- Database Session ---
    # SessionLocal is a session factory. Each instance of SessionLocal will be a database session.
    # We will use this in our path operations to get a database session for each request.
    # 'autocommit=False' means changes won't be saved automatically; we need to call .commit().
    # 'autoflush=False' means changes won't be flushed to DB until .commit() or .refresh().
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # --- SQLAlchemy Base Class ---
    # Base is used to define our SQLAlchemy ORM models.
    # All of our SQLAlchemy models (which represent database tables) will inherit from this Base.
Base = declarative_base()

    # --- Utility to create tables ---
    # This function will be called once at application startup to create database tables
    # based on the SQLAlchemy models defined from Base.
def create_db_and_tables():
        Base.metadata.create_all(bind=engine)