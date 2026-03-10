from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, leave
from . import models, crud, schemas
from sqlalchemy.orm import Session
from .database import get_db
from fastapi import Depends

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(leave.router)

@app.on_event("startup")
async def startup_event():
    # Initialize default leave types if they don't exist
    db: Session = next(get_db())
    for leave_type_name in models.LeaveTypeEnum:
        if not crud.get_leave_type_by_name(db, leave_type_name):
            max_days = None
            if leave_type_name == models.LeaveTypeEnum.FLEXI:
                max_days = 2 # As per HLD, 2 days per year for Flexi Holiday
            crud.create_leave_type(db, schemas.LeaveTypeCreate(name=leave_type_name, max_days_per_year=max_days))
    db.close()

@app.get("/")
async def root():
    return {"message": "Welcome to the Employee Leave Application API"}
