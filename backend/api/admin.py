from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta

from database import get_db
from models import User, Anomaly, AuditLog
from .auth import get_current_user

router = APIRouter()

@router.get("/dashboard", response_model=dict)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access dashboard stats"
        )
    
    # Get total counts
    total_users = db.query(User).count()
    total_anomalies = db.query(Anomaly).count()
    active_anomalies = db.query(Anomaly).filter(Anomaly.status != "resolved").count()
    
    # Get recent anomalies
    recent_anomalies = db.query(Anomaly)\
        .order_by(Anomaly.timestamp.desc())\
        .limit(5)\
        .all()
    
    # Get user activity
    recent_activity = db.query(AuditLog)\
        .order_by(AuditLog.timestamp.desc())\
        .limit(10)\
        .all()
    
    return {
        "stats": {
            "total_users": total_users,
            "total_anomalies": total_anomalies,
            "active_anomalies": active_anomalies
        },
        "recent_anomalies": [
            {
                "id": a.id,
                "timestamp": a.timestamp,
                "location": a.location,
                "severity": a.severity,
                "status": a.status
            }
            for a in recent_anomalies
        ],
        "recent_activity": [
            {
                "id": log.id,
                "user": log.user.username,
                "action": log.action,
                "timestamp": log.timestamp
            }
            for log in recent_activity
        ]
    }

@router.get("/audit-logs", response_model=List[dict])
async def get_audit_logs(
    start_date: datetime = None,
    end_date: datetime = None,
    user_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view audit logs"
        )
    
    query = db.query(AuditLog)
    
    # Apply filters
    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    
    logs = query.order_by(AuditLog.timestamp.desc()).all()
    
    return [
        {
            "id": log.id,
            "user": log.user.username,
            "action": log.action,
            "details": log.details,
            "timestamp": log.timestamp,
            "ip_address": log.ip_address
        }
        for log in logs
    ]

@router.get("/system-health", response_model=dict)
async def get_system_health(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if user has admin role
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view system health"
        )
    
    # Get anomaly detection stats for last 24 hours
    last_24h = datetime.utcnow() - timedelta(hours=24)
    anomalies_24h = db.query(Anomaly)\
        .filter(Anomaly.timestamp >= last_24h)\
        .count()
    
    # Get active users in last 24 hours
    active_users = db.query(AuditLog)\
        .filter(AuditLog.timestamp >= last_24h)\
        .distinct(AuditLog.user_id)\
        .count()
    
    return {
        "status": "healthy",
        "last_24h_stats": {
            "anomalies_detected": anomalies_24h,
            "active_users": active_users
        },
        "system_info": {
            "version": "1.0.0",
            "last_updated": datetime.utcnow()
        }
    }