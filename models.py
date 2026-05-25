import uuid
from typing import Optional, List
from enum import Enum
from sqlalchemy import String, Enum as SQLEnum, Uuid, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


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


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4, index=True
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100))
    school: Mapped[Institute] = mapped_column(
        SQLEnum(
            Institute,
            values_callable=lambda institutes: [i.value for i in institutes],
        ),
        server_default=Institute.IITM.value,
    )

    jobs: Mapped[List["Job"]] = relationship(back_populates="company")

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', school='{self.school}')>"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(500), nullable=False)
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

    company: Mapped["User"] = relationship(back_populates="jobs")

    def __repr__(self):
        return f"<User(title='{self.title}', mode='{self.mode}', job_type='{self.job_type}, description='{len(self.description)}')>"


# class Practice(Base):
#     __tablename__ = "practice"
#     x: Mapped[int] = mapped_column()
#     y: Mapped[int] = mapped_column()
