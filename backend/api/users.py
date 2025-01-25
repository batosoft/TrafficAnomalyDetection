from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, AuditLog
from .auth import get_current_user

router = APIRouter()

@router.get("/me", response_model=dict)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role
    }

@router.put("/me", response_model=dict)
async def update_user_profile(
    full_name: str,
    email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Update user profile
    current_user.full_name = full_name
    current_user.email = email
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action="profile_updated",
        details=f"Profile updated by user"
    )
    
    db.add(audit_log)
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Profile updated successfully"}

@router.get("/list", response_model=List[dict])
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view user list"
        )
    
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active
        }
        for user in users
    ]

@router.put("/{user_id}/role", response_model=dict)
async def update_user_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update user roles"
        )
    
    # Get user to update
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update role
    user.role = role
    
    # Create audit log
    audit_log = AuditLog(
        user_id=current_user.id,
        action="role_updated",
        details=f"Updated role of user {user.username} to {role}"
    )
    
    db.add(audit_log)
    db.commit()
    
    return {"message": "User role updated successfully"}

@router.put("/{user_id}/status", response_model=dict)
async def update_user_status(
    user_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update user status"
        )
    
    # Get user to update
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update status
    user.is_active = is_active
    
    # Create audit log
    status_str = "activated" if is_active else "deactivated"
    audit_log = AuditLog(
        user_id=current_user.id,
        action="status_updated",
        details=f"User {user.username} {status_str}"
    )
    
    db.add(audit_log)
    db.commit()
    
    return {"message": "User status updated successfully"}