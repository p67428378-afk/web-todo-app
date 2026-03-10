from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import crud, schemas, auth, models
from ..database import get_db

router = APIRouter(
    prefix="/leave",
    tags=["leave"],
)

@router.post("/apply", response_model=schemas.LeaveRequest)
async def apply_for_leave(
    leave_request: schemas.LeaveRequestCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    leave_type = crud.get_leave_type_by_id(db, leave_request.leave_type_id)
    if not leave_type:
        raise HTTPException(status_code=404, detail="Leave type not found")

    # Validate Flexi Holiday specific rules
    if leave_type.name == models.LeaveTypeEnum.FLEXI:
        if (leave_request.end_date - leave_request.start_date).days + 1 > 2:
            raise HTTPException(status_code=400, detail="Flexi Holiday cannot be more than 2 days")
        # TODO: Add logic to check if user has already taken 2 flexi holidays in the year

    # Determine initial status based on leave type
    if leave_type.name in [models.LeaveTypeEnum.FLEXI, models.LeaveTypeEnum.SICK]:
        initial_status = models.LeaveStatus.APPROVED
        manager_id = None
    else:
        initial_status = models.LeaveStatus.PENDING
        # In a real system, manager_id would be looked up based on current_user's hierarchy
        # For now, we'll assume a default manager or leave it null for pending approval
        manager_id = None # TODO: Implement manager lookup logic

    db_leave_request = crud.create_leave_request(
        db=db,
        leave_request=leave_request,
        user_id=current_user.id,
        status=initial_status,
        manager_id=manager_id
    )

    # If auto-approved, update leave balance
    if initial_status == models.LeaveStatus.APPROVED:
        days_taken = (leave_request.end_date - leave_request.start_date).days + 1
        current_balance = crud.get_leave_balance(db, current_user.id, leave_request.leave_type_id)
        if current_balance and current_balance.days_remaining >= days_taken:
            crud.update_leave_balance(db, current_user.id, leave_request.leave_type_id, current_balance.days_remaining - days_taken)
        else:
            # This should ideally be caught earlier with client-side validation or a more robust balance check
            raise HTTPException(status_code=400, detail="Insufficient leave balance")

    return db_leave_request

@router.get("/status", response_model=List[schemas.LeaveRequest])
async def get_leave_status(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_leave_requests(db, user_id=current_user.id)

@router.get("/balance", response_model=List[schemas.LeaveBalance])
async def get_leave_balance(
    current_user: models.User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    return crud.get_user_leave_balances(db, user_id=current_user.id)

@router.put("/{request_id}/approve", response_model=schemas.LeaveRequest)
async def approve_leave_request(
    request_id: int,
    current_user: models.User = Depends(auth.get_current_manager_user),
    db: Session = Depends(get_db)
):
    db_request = crud.get_leave_request(db, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if db_request.status != models.LeaveStatus.PENDING:
        raise HTTPException(status_code=400, detail="Leave request is not pending approval")

    # TODO: Verify if current_user is the actual manager of db_request.employee

    updated_request = crud.update_leave_request_status(db, request_id, models.LeaveStatus.APPROVED)

    # Update leave balance for approved requests
    days_taken = (updated_request.end_date - updated_request.start_date).days + 1
    current_balance = crud.get_leave_balance(db, updated_request.user_id, updated_request.leave_type_id)
    if current_balance and current_balance.days_remaining >= days_taken:
        crud.update_leave_balance(db, updated_request.user_id, updated_request.leave_type_id, current_balance.days_remaining - days_taken)
    else:
        # This scenario indicates a data inconsistency or race condition if balance was sufficient at application time
        raise HTTPException(status_code=500, detail="Failed to update leave balance after approval")

    return updated_request

@router.put("/{request_id}/reject", response_model=schemas.LeaveRequest)
async def reject_leave_request(
    request_id: int,
    current_user: models.User = Depends(auth.get_current_manager_user),
    db: Session = Depends(get_db)
):
    db_request = crud.get_leave_request(db, request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if db_request.status != models.LeaveStatus.PENDING:
        raise HTTPException(status_code=400, detail="Leave request is not pending approval")

    # TODO: Verify if current_user is the actual manager of db_request.employee

    return crud.update_leave_request_status(db, request_id, models.LeaveStatus.REJECTED)
