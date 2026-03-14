from sqlalchemy.orm import Session
from . import models, schemas
from datetime import date
from typing import List, Optional

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_leave_type_by_name(db: Session, name: models.LeaveTypeEnum):
    return db.query(models.LeaveType).filter(models.LeaveType.name == name).first()

def get_leave_type_by_id(db: Session, leave_type_id: int):
    return db.query(models.LeaveType).filter(models.LeaveType.id == leave_type_id).first()

def create_leave_type(db: Session, leave_type: schemas.LeaveTypeCreate):
    db_leave_type = models.LeaveType(name=leave_type.name, max_days_per_year=leave_type.max_days_per_year)
    db.add(db_leave_type)
    db.commit()
    db.refresh(db_leave_type)
    return db_leave_type

def get_leave_request(db: Session, request_id: int):
    return db.query(models.LeaveRequest).filter(models.LeaveRequest.id == request_id).first()

def get_user_leave_requests(db: Session, user_id: int):
    return db.query(models.LeaveRequest).filter(models.LeaveRequest.user_id == user_id).all()

def create_leave_request(db: Session, leave_request: schemas.LeaveRequestCreate, user_id: int, status: models.LeaveStatus, manager_id: Optional[int] = None):
    db_leave_request = models.LeaveRequest(
        **leave_request.dict(),
        user_id=user_id,
        status=status,
        manager_id=manager_id
    )
    db.add(db_leave_request)
    db.commit()
    db.refresh(db_leave_request)
    return db_leave_request

def update_leave_request_status(db: Session, request_id: int, status: models.LeaveStatus):
    db_request = db.query(models.LeaveRequest).filter(models.LeaveRequest.id == request_id).first()
    if db_request:
        db_request.status = status
        db.commit()
        db.refresh(db_request)
    return db_request

def get_leave_balance(db: Session, user_id: int, leave_type_id: int):
    return db.query(models.LeaveBalance).filter(
        models.LeaveBalance.user_id == user_id,
        models.LeaveBalance.leave_type_id == leave_type_id
    ).first()

def get_user_leave_balances(db: Session, user_id: int) -> List[models.LeaveBalance]:
    return db.query(models.LeaveBalance).filter(models.LeaveBalance.user_id == user_id).all()

def create_leave_balance(db: Session, leave_balance: schemas.LeaveBalanceCreate):
    db_leave_balance = models.LeaveBalance(**leave_balance.dict())
    db.add(db_leave_balance)
    db.commit()
    db.refresh(db_leave_balance)
    return db_leave_balance

def update_leave_balance(db: Session, user_id: int, leave_type_id: int, days_remaining: int):
    db_balance = get_leave_balance(db, user_id, leave_type_id)
    if db_balance:
        db_balance.days_remaining = days_remaining
        db.commit()
        db.refresh(db_balance)
    return db_balance
