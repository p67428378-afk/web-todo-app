import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

def get_application_database_url():
    return os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/leave_app_db")

def create_engine_and_session(database_url: str):
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal

# These will be initialized in main.py or overridden for tests
app_engine = None
AppSessionLocal = None

def get_db():
    db = AppSessionLocal()
    try:
        yield db
    finally:
        db.close()

# This function is for tests to create their own engine and session
def create_test_engine_and_session(test_database_url: str):
    test_engine = create_engine(test_database_url, poolclass=StaticPool)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return test_engine, TestSessionLocal
