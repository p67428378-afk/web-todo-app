import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

Base = declarative_base()

def get_application_database_url():
    return os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/leave_app_db")

# These are placeholders; actual engine and session will be managed by FastAPI app state or tests
engine_instance = None
SessionLocal_instance = None

def get_db():
    if SessionLocal_instance is None:
        raise Exception("Database not initialized. Call init_db_for_app or ensure test setup is correct.")
    db = SessionLocal_instance()
    try:
        yield db
    finally:
        db.close()

def init_db_for_app():
    global engine_instance, SessionLocal_instance
    engine_instance = create_engine(get_application_database_url())
    SessionLocal_instance = sessionmaker(autocommit=False, autoflush=False, bind=engine_instance)

# This function is for tests to create their own engine and session
def create_test_engine_and_session(test_database_url: str):
    test_engine = create_engine(test_database_url, poolclass=StaticPool)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return test_engine, TestSessionLocal
