import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

def get_application_database_url():
    return os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/leave_app_db")

def create_app_engine():
    return create_engine(get_application_database_url())

def create_app_session_local(engine_instance):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine_instance)

# Global engine and SessionLocal for the application
# These will be initialized once when the module is imported
app_engine = create_app_engine()
AppSessionLocal = create_app_session_local(app_engine)

def get_db():
    db = AppSessionLocal()
    try:
        yield db
    finally:
        db.close()

# This function is for tests to create their own engine and session
def create_test_engine_and_session(test_database_url: str):
    test_engine = create_engine(test_database_url)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return test_engine, TestSessionLocal
