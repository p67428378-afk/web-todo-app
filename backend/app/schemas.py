from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from .models import UserRole, LeaveStatus, LeaveTypeEnum

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Optional[UserRole] = UserRole.EMPLOYEE

class User(UserBase):
    id: int
    role: UserRole

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LeaveTypeBase(BaseModel):
    name: LeaveTypeEnum
    max_days_per_year: Optional[int] = None

class LeaveTypeCreate(LeaveTypeBase):
    pass

class LeaveType(LeaveTypeBase):
    id: int

    class Config:
        orm_mode = True

class LeaveRequestBase(BaseModel):
    leave_type_id: int
    start_date: date
    end_date: date
    reason: str

class LeaveRequestCreate(LeaveRequestBase):
    pass

class LeaveRequestUpdate(BaseModel):
    status: LeaveStatus

class LeaveRequest(LeaveRequestBase):
    id: int
    user_id: int
    status: LeaveStatus
    manager_id: Optional[int] = None

    class Config:
        orm_mode = True

class LeaveBalanceBase(BaseModel):
    leave_type_id: int
    days_remaining: int

class LeaveBalanceCreate(LeaveBalanceBase):
    user_id: int

class LeaveBalance(LeaveBalanceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
