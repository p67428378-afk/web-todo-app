import logging
import os # Import os
from fastapi import FastAPI, Depends
from .database import Base, get_db, get_application_database_url, create_engine_and_session_factory, is_test_environment
from .routers import auth, leave
from . import models, crud, schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Override get_db to use the app's session local
def get_app_db():
    # Ensure app.state.AppSessionLocal is initialized before use
    if not hasattr(app.state, 'AppSessionLocal'):
        raise RuntimeError("Database session not initialized. Ensure startup_event has run.")
    db = app.state.AppSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = get_app_db

# Include routers
app.include_router(auth.router)
app.include_router(leave.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Running startup event...")
    
    test_env = is_test_environment()
    
    # Explicitly set database_url for test environment to ensure in-memory SQLite
    if test_env:
        database_url = "sqlite:///:memory:"
    else:
        database_url = get_application_database_url() # Use the original logic for non-test environments
    
    logger.info(f"Database URL: {database_url}, Test Environment: {test_env}")

    app.state.app_engine, app.state.AppSessionLocal = create_engine_and_session_factory(
        database_url
    )

    # Create database tables
    Base.metadata.create_all(bind=app.state.app_engine)
    logger.info("Database tables created/checked.")

    # Only initialize default leave types if not in a test environment
    if not test_env:
        db_gen = app.dependency_overrides[get_db]()
        db = next(db_gen)
        try:
            # Initialize default leave types if they don't exist
            for leave_type_name in models.LeaveTypeEnum:
                if not crud.get_leave_type_by_name(db, leave_type_name):
                    max_days = None
                    if leave_type_name == models.LeaveTypeEnum.FLEXI:
                        max_days = 2 # As per HLD, 2 days per year for Flexi Holiday
                    crud.create_leave_type(db, schemas.LeaveTypeCreate(name=leave_type_name, max_days_per_year=max_days)))
            logger.info("Default leave types initialized successfully.")
        except OperationalError as e:
            logger.warning(f"Database connection failed during startup event: {e}. Skipping default data initialization. This might be expected in a test environment if the test setup doesn't fully mock the DB for startup.")
        except Exception as e:
            logger.error(f"An unexpected error occurred during startup event: {e}")
        finally:
            # Ensure the session is closed
            try:
                next(db_gen, None) # Close the session if it hasn't been already
            except StopIteration:
                pass
    else:
        logger.info("Skipping default leave type initialization in test environment.")


@app.get("/")
async def root():
    return {"message": "Welcome to the Employee Leave Application API"}
