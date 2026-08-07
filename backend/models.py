from decimal import Decimal
from typing import Optional, List
from enum import Enum
from sqlalchemy import String, Enum as SQLEnum, Text, ForeignKey, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from datetime import datetime

class UserRole(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    COMPANY = "company"

class Timestamp:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

class User(Timestamp, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(
            UserRole,
            values_callable=lambda roles: [r.value for r in roles],
            name="user_role",
        ),
        server_default=UserRole.STUDENT.value,
    )

    student_profile: Mapped[Optional["StudentProfile"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    company_profile: Mapped[Optional["CompanyProfile"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"""
        User
        username='{self.username}' 
        email='{self.email}' 
        role='{self.role}'"""


class StudentStatus(Enum):
    ACTIVE="active"
    BLACKLISTED = "blacklisted"

class StudentProfile(Timestamp, Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    school: Mapped[str] = mapped_column(String(500))
    cgpa: Mapped[Decimal] = mapped_column(Numeric(precision=3, scale=1))
    status: Mapped[StudentStatus] = mapped_column(SQLEnum(
            StudentStatus,
            values_callable=lambda students: [s.value for s in students],
            name="student_status",
        ),server_default=StudentStatus.ACTIVE.value,
        )
    resume_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    user: Mapped["User"] = relationship(back_populates="student_profile")
    applications: Mapped[List["Application"]] = relationship(back_populates="student")
    def __repr__(self):
        return f"""
        StudentProfile 
        user_id='{self.user_id}' 
        first_name='{self.first_name}' 
        last_name='{self.last_name}' 
        school='{self.school}' 
        cgpa='{self.cgpa}'"""

class CompanyStatus(Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"
    BLACKLISTED = "blacklisted"

class CompanyProfile(Timestamp, Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    website: Mapped[str] = mapped_column(String(200))
    about: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String(500))
    status: Mapped[CompanyStatus] = mapped_column(
        SQLEnum(
            CompanyStatus,
            values_callable=lambda companies: [c.value for c in companies],
            name="company_status",
        ),
        server_default=CompanyStatus.PENDING.value,
    )

    user: Mapped["User"] = relationship(back_populates="company_profile")
    jobs: Mapped[List["Job"]] = relationship(
        back_populates="company",passive_deletes=True
    )

    def __repr__(self):
        return f"""
        CompanyProfile 
        user_id='{self.user_id}' 
        name='{self.name}' 
        website='{self.website}' 
        about='{self.about}' 
        location='{self.location}'"""

class JobStatus(Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "reject"
    CLOSED = "closed"
    
class JobMode(Enum):
    ON_SITE = "on-site"
    REMOTE = "remote"
    HYBRID = "hybrid"

class JobType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"

class Job(Timestamp, Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="SET NULL")
    ,nullable=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(500))
    mode: Mapped[JobMode] = mapped_column(
        SQLEnum(
            JobMode,
            values_callable=lambda job_modes: [m.value for m in job_modes],
            name="job_mode",
        ),
        server_default=JobMode.ON_SITE.value,
    )
    job_type: Mapped[JobType] = mapped_column(
        SQLEnum(
            JobType,
            values_callable=lambda job_types: [t.value for t in job_types],
            name="job_type",
        ),
        server_default=JobType.FULL_TIME.value,
    )
    job_status: Mapped[JobStatus] = mapped_column(
        SQLEnum(JobStatus, values_callable=lambda job_status: [s.value for s in job_status],name="job_status"),
        server_default=JobStatus.PENDING.value
    )
    description: Mapped[str] = mapped_column(Text)
    required_cgpa: Mapped[Optional[Decimal]] = mapped_column(Numeric(precision=3, scale=1), nullable=True)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    company: Mapped[Optional["CompanyProfile"]] = relationship(
        back_populates="jobs",
    )

    applications: Mapped[List["Application"]] = relationship(
        back_populates="job", passive_deletes=True
    )

    def __repr__(self):
        return f"""
        Job 
        title='{self.title}' 
        location='{self.location}' 
        mode='{self.mode}' 
        job_type='{self.job_type}'
        job_status='{self.job_status}'
        description='{len(self.description)}'"""

class ApplicationStatus(Enum):
    PENDING = "pending"
    SHORTLISTED = "shortlisted"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(Timestamp, Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    
    job_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True
    )

    status: Mapped[ApplicationStatus] = mapped_column(
        SQLEnum(
            ApplicationStatus,
            values_callable=lambda statuses: [s.value for s in statuses],
            name="application_status",
        ),
        server_default=ApplicationStatus.PENDING.value,
        nullable=False,
    )
    applied_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.now(),
        nullable=False
    )
    student: Mapped["StudentProfile"] = relationship(
        back_populates="applications"
    )
    job: Mapped[Optional["Job"]] = relationship(
        back_populates="applications"
    )
    def __repr__(self):
        return f"""Application
        id={self.id} 
        student_id={self.student_id} 
        job_id={self.job_id} 
        status='{self.status.value}'>"""