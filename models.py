import uuid
from decimal import Decimal
from typing import Optional, List
from enum import Enum
from sqlalchemy import String, Enum as SQLEnum, Uuid, Text, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class UserRole(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    COMPANY = "company"


class Institute(Enum):
    IITM = "INDIAN INSTITUTE OF TECHNOLOGY MADRAS"
    IITR = "INDIAN INSTITUTE OF TECHNOLOGY ROPAR"
    IITMANDI = "INDIAN INSTITUTE OF TECHNOLOGY MANDI"
    IITB = "INDIAN INSTITUTE OF TECHNOLOGY BOMBAY"
    IITD = "INDIAN INSTITUTE OF TECHNOLOGY DELHI"


class JobMode(Enum):
    ON_SITE = "on-site"
    REMOTE = "remote"
    HYBRID = "hybrid"


class JobType(Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"


class CompanyStatus(Enum):
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4, index=True
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
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


class StudentProfile(Base):
    __tablename__ = "students"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    school: Mapped[str] = mapped_column(String(500))
    cgpa: Mapped[Decimal] = mapped_column(Numeric(precision=3, scale=1))

    user: Mapped["User"] = relationship(back_populates="student_profile")

    def __repr__(self):
        return f"""
        StudentProfile 
        user_id='{self.user_id}' 
        first_name='{self.first_name}' 
        last_name='{self.last_name}' 
        school='{self.school}' 
        cgpa='{self.cgpa}'"""


class CompanyProfile(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
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
        back_populates="company", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"""
        CompanyProfile 
        user_id='{self.user_id}' 
        name='{self.name}' 
        website='{self.website}' 
        about='{self.about}' 
        location='{self.location}'"""


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("companies.id", ondelete="CASCADE")
    )
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
    description: Mapped[str] = mapped_column(Text)

    company: Mapped["CompanyProfile"] = relationship(
        back_populates="jobs",
    )

    def __repr__(self):
        return f"""
        Job 
        title='{self.title}' 
        location='{self.location}' 
        mode='{self.mode}' 
        job_type='{self.job_type}' 
        description='{len(self.description)}'"""