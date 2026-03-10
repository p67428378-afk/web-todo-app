import logging
from fastapi import FastAPI
from .database import app_engine, Base, get_db
from .routers import auth, leave
from . import models, crud, schemas
from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.exc import OperationalError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=app_engine)

# Include routers
app.include_router(auth.router)
app.include_router(leave.router)

@app.on_event("startup")
async def startup_event():
    try:
        # Initialize default leave types if they don't exist
        db: Session = next(get_db())
        for leave_type_name in models.LeaveTypeEnum:
            if not crud.get_leave_type_by_name(db, leave_type_name):
                max_days = None
                if leave_type_name == models.LeaveTypeEnum.FLEXI:
                    max_days = 2 # As per HLD, 2 days per year for Flexi Holiday
                crud.create_leave_type(db, schemas.LeaveTypeCreate(name=leave_type_name, max_days_per_year=max_days))
        db.close()
        logger.info("Default leave types initialized successfully.")
    except OperationalError as e:
        logger.warning(f"Database connection failed during startup event: {e}. Skipping default data initialization. This might be expected in a test environment.")
    except Exception as e:
        logger.error(f"An unexpected error occurred during startup event: {e}")


@app.get("/")
async def root():
    return {"message": "Welcome to the Employee Leave Application API"}
