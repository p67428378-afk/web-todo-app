import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

Base = declarative_base()

def get_application_database_url():
    return os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/leave_app_db")

def is_test_environment():
    return os.getenv("TESTING", "False").lower() == "true"

def create_engine_and_session_factory(database_url: str, for_tests: bool = False):
    """
    Creates a SQLAlchemy engine and a sessionmaker factory.
    If for_tests is True, it configures the engine for an in-memory SQLite database.
    """
    if for_tests:
        # For tests, use an in-memory SQLite database with StaticPool
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        # For production, use the specified database URL
        engine = create_engine(database_url)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal

# This is the default dependency function.
# It will be overridden by the application's specific session factory
# and by test-specific session factories.
def get_db():
    """
    Placeholder for the database session dependency.
    This function should always be overridden in actual application setup or tests.
    """
    raise NotImplementedError("get_db dependency must be overridden.")
