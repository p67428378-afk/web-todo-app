from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class UserRole(str, enum.Enum):
    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"

class LeaveStatus(str, enum.Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

class LeaveTypeEnum(str, enum.Enum):
    CASUAL = "Casual Leave"
    SICK = "Sick Leave"
    EARNED = "Earned Leave"
    FLEXI = "Flexi Holiday"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)

    submitted_leave_requests = relationship("LeaveRequest", foreign_keys="[LeaveRequest.user_id]", back_populates="employee")
    managed_leave_requests = relationship("LeaveRequest", foreign_keys="[LeaveRequest.manager_id]", back_populates="manager")
    leave_balances = relationship("LeaveBalance", back_populates="user")

class LeaveType(Base):
    __tablename__ = "leave_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(LeaveTypeEnum), unique=True, index=True)
    max_days_per_year = Column(Integer, nullable=True) # For Flexi Holiday

    leave_requests = relationship("LeaveRequest", back_populates="leave_type")
    leave_balances = relationship("LeaveBalance", back_populates="leave_type")

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(String)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True) # For manager approval

    employee = relationship("User", foreign_keys=[user_id], back_populates="submitted_leave_requests")
    leave_type = relationship("LeaveType", back_populates="leave_type")
    manager = relationship("User", foreign_keys=[manager_id], back_populates="managed_leave_requests")

class LeaveBalance(Base):
    __tablename__ = "leave_balances"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    leave_type_id = Column(Integer, ForeignKey("leave_types.id"))
    days_remaining = Column(Integer)

    user = relationship("User", back_populates="leave_balances")
    leave_type = relationship("LeaveType", back_populates="leave_balances")
