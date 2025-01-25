from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import Anomaly, AnomalyAction, User
from .auth import get_current_user

router = APIRouter()

@router.post("/", response_model=dict)
async def create_anomaly(
    location: str,
    anomaly_type: str,
    severity: float,
    description: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Create new anomaly
    anomaly = Anomaly(
        location=location,
        anomaly_type=anomaly_type,
        severity=severity,
        description=description,
        status="detected",
        assigned_to_id=current_user.id
    )
    
    db.add(anomaly)
    db.commit()
    db.refresh(anomaly)
    
    # Create action log
    action = AnomalyAction(
        anomaly_id=anomaly.id,
        action_type="created",
        description=f"Anomaly detected and created by {current_user.username}"
    )
    
    db.add(action)
    db.commit()
    
    return {"message": "Anomaly created successfully", "anomaly_id": anomaly.id}

@router.get("/", response_model=List[dict])
async def get_anomalies(
    status: Optional[str] = None,
    severity_min: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Anomaly)
    
    # Apply filters
    if status:
        query = query.filter(Anomaly.status == status)
    if severity_min is not None:
        query = query.filter(Anomaly.severity >= severity_min)
    
    # Get results
    anomalies = query.all()
    return [
        {
            "id": a.id,
            "timestamp": a.timestamp,
            "location": a.location,
            "anomaly_type": a.anomaly_type,
            "severity": a.severity,
            "description": a.description,
            "status": a.status,
            "assigned_to": a.assigned_to.username if a.assigned_to else None
        }
        for a in anomalies
    ]

@router.get("/{anomaly_id}", response_model=dict)
async def get_anomaly(
    anomaly_id: int,
    db: Session = Depends(get_db)
):
    anomaly = db.query(Anomaly).filter(Anomaly.id == anomaly_id).first()
    if not anomaly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anomaly not found"
        )
    
    return {
        "id": anomaly.id,
        "timestamp": anomaly.timestamp,
        "location": anomaly.location,
        "anomaly_type": anomaly.anomaly_type,
        "severity": anomaly.severity,
        "description": anomaly.description,
        "ai_report": anomaly.ai_report,
        "status": anomaly.status,
        "assigned_to": anomaly.assigned_to.username if anomaly.assigned_to else None,
        "resolved_at": anomaly.resolved_at
    }

@router.put("/{anomaly_id}/status", response_model=dict)
async def update_anomaly_status(
    anomaly_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    anomaly = db.query(Anomaly).filter(Anomaly.id == anomaly_id).first()
    if not anomaly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anomaly not found"
        )
    
    # Update status
    anomaly.status = status
    if status == "resolved":
        anomaly.resolved_at = datetime.utcnow()
    
    # Create action log
    action = AnomalyAction(
        anomaly_id=anomaly.id,
        action_type="status_changed",
        description=f"Status updated to {status} by {current_user.username}"
    )
    
    db.add(action)
    db.commit()
    
    return {"message": "Anomaly status updated successfully"}

@router.post("/{anomaly_id}/assign", response_model=dict)
async def assign_anomaly(
    anomaly_id: int,
    assigned_to_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can assign anomalies"
        )
    
    anomaly = db.query(Anomaly).filter(Anomaly.id == anomaly_id).first()
    if not anomaly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anomaly not found"
        )
    
    # Update assigned user
    assigned_user = db.query(User).filter(User.id == assigned_to_id).first()
    if not assigned_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assigned user not found"
        )
    
    anomaly.assigned_to_id = assigned_to_id
    
    # Create action log
    action = AnomalyAction(
        anomaly_id=anomaly.id,
        action_type="assigned",
        description=f"Assigned to {assigned_user.username} by {current_user.username}"
    )
    
    db.add(action)
    db.commit()
    
    return {"message": "Anomaly assigned successfully"}