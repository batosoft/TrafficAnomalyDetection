from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String)  # admin, analyst, user
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    anomalies = relationship("Anomaly", back_populates="assigned_to")
    audit_logs = relationship("AuditLog", back_populates="user")

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    location = Column(String)
    anomaly_type = Column(String)
    severity = Column(Float)
    description = Column(Text)
    ai_report = Column(Text)
    status = Column(String)  # detected, investigating, resolved
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    resolved_at = Column(DateTime, nullable=True)

    assigned_to = relationship("User", back_populates="anomalies")
    actions = relationship("AnomalyAction", back_populates="anomaly")

class AnomalyAction(Base):
    __tablename__ = "anomaly_actions"

    id = Column(Integer, primary_key=True, index=True)
    anomaly_id = Column(Integer, ForeignKey("anomalies.id"))
    action_type = Column(String)  # notification_sent, status_changed, comment_added
    description = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    anomaly = relationship("Anomaly", back_populates="actions")

class TrafficData(Base):
    __tablename__ = "traffic_data"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_count = Column(Integer)
    average_speed = Column(Float)
    congestion_level = Column(Float)
    time_of_day = Column(Integer)
    timestamp = Column(DateTime)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String)

    user = relationship("User", back_populates="audit_logs")