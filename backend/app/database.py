import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

Base = declarative_base()

# Global variables to hold the engine and session, initialized dynamically
_app_engine = None
_AppSessionLocal = None

def get_application_database_url():
    return os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/leave_app_db")

def init_app_db():
    global _app_engine, _AppSessionLocal
    _app_engine = create_engine(get_application_database_url())
    _AppSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_app_engine)

def get_db():
    if _AppSessionLocal is None:
        raise Exception("Database not initialized. Call init_app_db() or ensure test setup is correct.")
    db = _AppSessionLocal()
    try:
        yield db
    finally:
        db.close()

# This function is for tests to create their own engine and session
def create_test_engine_and_session(test_database_url: str):
    test_engine = create_engine(test_database_url, poolclass=StaticPool)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return test_engine, TestSessionLocal
