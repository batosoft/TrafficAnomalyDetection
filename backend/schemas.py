from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class AnomalyBase(BaseModel):
    location: str
    anomaly_type: str
    severity: float
    description: str

class AnomalyCreate(AnomalyBase):
    pass

class Anomaly(AnomalyBase):
    id: int
    timestamp: datetime
    ai_report: str
    status: str
    assigned_to_id: Optional[int]
    resolved_at: Optional[datetime]

    class Config:
        orm_mode = True

class AnomalyActionBase(BaseModel):
    action_type: str
    description: str

class AnomalyActionCreate(AnomalyActionBase):
    anomaly_id: int

class AnomalyAction(AnomalyActionBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class AuditLogBase(BaseModel):
    action: str
    details: str
    ip_address: str

class AuditLog(AuditLogBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True