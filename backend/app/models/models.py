import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserRole(str, PyEnum):
    ADMIN = "admin"
    SECURITY_ENGINEER = "security_engineer"
    VIEWER = "viewer"

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    users = relationship("User", back_populates="organization")
    scans = relationship("Scan", back_populates="organization")

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.SECURITY_ENGINEER, nullable=False)
    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    organization = relationship("Organization", back_populates="users")
    scans = relationship("Scan", back_populates="user")

class ScanStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ScanSeverity(str, PyEnum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    PASS = "PASS"

class Scan(Base):
    __tablename__ = "scans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    input_type = Column(String(50), nullable=False) # 'text', 'file', 'github_repo'
    file_name = Column(String(255), nullable=True)
    status = Column(Enum(ScanStatus), default=ScanStatus.COMPLETED, nullable=False)
    
    risk_score = Column(Integer, default=0, nullable=False) # 0 to 100
    severity = Column(Enum(ScanSeverity), default=ScanSeverity.PASS, nullable=False)
    
    findings_json = Column(JSON, default=list, nullable=False)
    rewrites_json = Column(JSON, default=dict, nullable=False)
    metrics_json = Column(JSON, default=dict, nullable=False)
    raw_content = Column(Text, nullable=True)

    org_id = Column(String(36), ForeignKey("organizations.id"), nullable=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    organization = relationship("Organization", back_populates="scans")
    user = relationship("User", back_populates="scans")

class Rule(Base):
    __tablename__ = "rules"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rule_id = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False) # 'signatures', 'secrets', 'shell', 'obfuscation', 'classifier'
    severity = Column(Enum(ScanSeverity), nullable=False)
    description = Column(Text, nullable=False)
    pattern = Column(Text, nullable=True)
    enabled = Column(Integer, default=1, nullable=False)
